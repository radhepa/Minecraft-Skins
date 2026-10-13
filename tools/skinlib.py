"""Shared helpers for building HD 3D Bedrock skins.

A skin is a set of cubes on the standard Bedrock player rig. Every cube uses
per-face UVs on a 128x128 texture at 2 texels per model unit (HD density), so
the standard body parts sit exactly where a regular 128x128 HD skin has them,
and 3D accessories are packed into the space the vanilla head/hat would use.

Face canvases are painted in a "natural" orientation:
  north (front)  col: x+   row: y-      (seen from the front)
  south (back)   col: x-   row: y-      (seen from behind)
  east  (-x side, the character's right)  col: z- (back -> front)  row: y-
  west  (+x side, the character's left)   col: z+ (front -> back)  row: y-
  up / down      col: x+   row: z- (row 0 = back edge, last row = front edge)

Those match how Bedrock (and Blockbench) map per-face UVs, including the
vertically flipped "down" face that box UV produces.
"""

import json

import numpy as np
from PIL import Image

PX = 2  # texels per model unit
TEX = 128
FACES = ("north", "south", "east", "west", "up", "down")


def rgb(c, a=255):
    return np.array([c[0], c[1], c[2], a], dtype=np.float64)


class Cube:
    def __init__(self, name, bone, origin, size, rects, inflate=0.0, rotation=None,
                 pivot=None, like=None):
        self.name = name
        self.bone = bone
        self.origin = list(origin)
        self.size = list(size)
        self.inflate = inflate
        # optional per-cube rotation (degrees) about `pivot`, as in Bedrock 1.12.0
        self.rotation = list(rotation) if rotation else None
        self.pivot = list(pivot) if pivot else None
        # a clone reuses another cube's UVs (and so its painted texels)
        self.like = like
        # face -> (u, v, uw, vh); negative sizes flip that axis
        self.rects = rects


def box_rects(u, v, size, px=PX):
    """Per-face rects equivalent to Bedrock box UV at (u, v) in model units."""
    w, h, d = (s * px for s in size)
    u, v = u * px, v * px
    return {
        "east": (u, v + d, d, h),
        "north": (u + d, v + d, w, h),
        "west": (u + d + w, v + d, d, h),
        "south": (u + d + w + d, v + d, w, h),
        "up": (u + d, v, w, d),
        "down": (u + d + w, v + d, w, -d),
    }


def packed_rects(size, slots, px=PX):
    """Rects from explicit top-left texel positions per face.

    slots: face -> (u, v) in texels. Sizes come from the cube size.
    """
    w, h, d = (max(1, int(round(s * px))) for s in size)
    dims = {
        "north": (w, h), "south": (w, h),
        "east": (d, h), "west": (d, h),
        "up": (w, d), "down": (w, d),
    }
    rects = {}
    for f, (u, v) in slots.items():
        fw, fh = dims[f]
        if f == "down":  # same orientation as box UV's down face
            rects[f] = (u, v + fh, fw, -fh)
        else:
            rects[f] = (u, v, fw, fh)
    return rects


class Face:
    """A paintable face canvas in natural orientation with model coordinates."""

    def __init__(self, cube, face):
        self.cube, self.face = cube, face
        u, v, uw, vh = cube.rects[face]
        self.w, self.h = abs(int(uw)), abs(int(vh))
        self.rgba = np.zeros((self.h, self.w, 4))
        ox, oy, oz = cube.origin
        sx, sy, sz = cube.size
        cols = (np.arange(self.w) + 0.5) / self.w
        rows = (np.arange(self.h) + 0.5) / self.h
        C, R = np.meshgrid(cols, rows)
        x0, x1, y0, y1, z0, z1 = ox, ox + sx, oy, oy + sy, oz, oz + sz
        if face == "north":
            X, Y, Z = x0 + C * sx, y1 - R * sy, np.full_like(C, z0)
        elif face == "south":
            X, Y, Z = x1 - C * sx, y1 - R * sy, np.full_like(C, z1)
        elif face == "east":
            X, Y, Z = np.full_like(C, x0), y1 - R * sy, z1 - C * sz
        elif face == "west":
            X, Y, Z = np.full_like(C, x1), y1 - R * sy, z0 + C * sz
        elif face == "up":
            X, Y, Z = x0 + C * sx, np.full_like(C, y1), z1 - R * sz
        else:
            X, Y, Z = x0 + C * sx, np.full_like(C, y0), z1 - R * sz
        self.X, self.Y, self.Z = X, Y, Z
        # integer texel indices, handy for pixel-precise work
        self.col = np.arange(self.w)[None, :].repeat(self.h, 0)
        self.row = np.arange(self.h)[:, None].repeat(self.w, 1)

    def fill(self, color, mask=None):
        c = rgb(color) if len(color) == 3 else np.array(color, float)
        if mask is None:
            self.rgba[:] = c
        else:
            self.rgba[mask] = c

    def set(self, r, c, color):
        if 0 <= r < self.h and 0 <= c < self.w:
            self.rgba[r, c] = rgb(color) if len(color) == 3 else color

    def shade(self, factor, mask=None):
        f = np.asarray(factor, float)
        if f.ndim == 2:
            f = f[..., None]
        if mask is None:
            self.rgba[..., :3] *= f
        else:
            sub = self.rgba[..., :3] * f
            self.rgba[..., :3] = np.where(mask[..., None], sub, self.rgba[..., :3])

    def clear(self, mask=None):
        if mask is None:
            self.rgba[:] = 0
        else:
            self.rgba[mask] = 0

    def stamp(self, rows, palette, top=0, left=0, mirror=False):
        """Draw a character grid; '.' or ' ' is skipped."""
        for r, line in enumerate(rows):
            if mirror:
                line = line[::-1]
            for c, ch in enumerate(line):
                if ch in palette:
                    self.set(top + r, left + c, palette[ch])


class Skin:
    def __init__(self, identifier, slim=False):
        self.identifier = identifier
        self.slim = slim
        self.bones = [dict(b) for b in (SLIM_BONES if slim else PLAYER_BONES)]
        self.cubes = []
        self.faces = {}
        self.auto = []          # accessory cubes whose UVs get packed later
        self.packed = False

    def add(self, cube):
        self.cubes.append(cube)
        if cube.like is None:
            for f in cube.rects:
                self.faces[(cube.name, f)] = Face(cube, f)
        return cube

    def bone(self, name, parent, pivot, rotation=None):
        """Extra bone (for a group of accessory cubes that share a tilt)."""
        b = {"name": name, "parent": parent, "pivot": list(pivot)}
        if rotation:
            b["rotation"] = list(rotation)
        self.bones.append(b)

    def acc(self, name, bone, origin, size, inflate=0.0, faces=FACES, px=PX, lowres=(),
            rotation=None, pivot=None, like=None, pad=(), first=False, same=None):
        """Add an accessory cube; its face UVs are packed into free texture
        space automatically when the skin is composed. Faces listed in
        `lowres` (plain soles, linings, hidden tops) use 1 texel per unit.
        `like` names an earlier cube of the same size whose UVs (and paint)
        this one reuses, which costs no texture space. Faces listed in `pad`
        keep a clear texel all round so cut-out shapes never pick up a
        neighbour's colour along their edges. `first` packs this cube's faces
        before the rest (for wide faces that need the one wide free strip).
        `same` maps a face to another face of this cube whose texels it
        reuses (e.g. the back of a symmetric plate), at no texture cost."""
        if any(c.name == name for c in self.cubes):
            raise ValueError(f"cube name {name!r} is already used")
        if like is not None:
            src = next(c for c in self.cubes if c.name == like)
            return self.add(Cube(name, bone, origin, size, src.rects, inflate,
                                 rotation, pivot, like=src))
        rects = {}
        for f in faces:
            rects.update(packed_rects(size, {f: (0, 0)}, px=1 if f in lowres else px))
        same = dict(same or {})
        cube = Cube(name, bone, origin, size, {f: r for f, r in rects.items() if f not in same},
                    inflate, rotation, pivot)
        self.add(cube)
        cube.same = same
        cube.pad = tuple(pad)
        cube.first = first
        self.auto.append(cube)
        return cube

    def pack(self):
        if self.packed:
            return
        used = np.zeros((TEX, TEX), bool)
        for c in self.cubes:
            if c in self.auto or c.like is not None:
                continue
            for u, v, uw, vh in c.rects.values():
                u0, v0 = int(min(u, u + uw)), int(min(v, v + vh))
                used[v0:v0 + abs(int(vh)), u0:u0 + abs(int(uw))] = True
        jobs = [(c, f) for c in self.auto for f in c.rects]
        jobs.sort(key=lambda j: (not j[0].first, -abs(j[0].rects[j[1]][3]), -abs(j[0].rects[j[1]][2])))
        for c, f in jobs:
            _, _, uw, vh = c.rects[f]
            p = 1 if f in getattr(c, "pad", ()) else 0
            w, h = abs(int(uw)) + 2 * p, abs(int(vh)) + 2 * p
            spot = None
            for y in range(TEX - h + 1):
                row = used[y:y + h]
                for x in range(TEX - w + 1):
                    if not row[:, x:x + w].any():
                        spot = (x, y)
                        break
                if spot:
                    break
            if spot is None:
                raise ValueError(f"no texture space left for {c.name}.{f}")
            x, y = spot
            used[y:y + h, x:x + w] = True
            x, y, w, h = x + p, y + p, w - 2 * p, h - 2 * p
            c.rects[f] = (x, y + h, w, -h) if f == "down" else (x, y, w, h)
        self.packed = True

    def face(self, cube_name, f):
        return self.faces[(cube_name, f)]

    def each(self, cube_name, faces=FACES):
        return [self.faces[(cube_name, f)] for f in faces if (cube_name, f) in self.faces]

    # ---------------------------------------------------------------- output
    def compose(self):
        self.pack()
        img = np.zeros((TEX, TEX, 4))
        used = np.zeros((TEX, TEX), bool)
        for (name, f), face in self.faces.items():
            u, v, uw, vh = face.cube.rects[f]
            data = face.rgba
            if uw < 0:
                data = data[:, ::-1]
            if vh < 0:
                data = data[::-1]
            u0 = int(min(u, u + uw))
            v0 = int(min(v, v + vh))
            region = used[v0:v0 + face.h, u0:u0 + face.w]
            if region.any():
                raise ValueError(f"UV overlap at {name}.{f}")
            used[v0:v0 + face.h, u0:u0 + face.w] = True
            img[v0:v0 + face.h, u0:u0 + face.w] = data
        out = np.clip(np.round(img), 0, 255).astype(np.uint8)
        # Bedrock skins are alpha-tested: no half-transparent texels.
        a = out[..., 3]
        out[..., 3] = np.where(a >= 128, 255, 0)
        out[out[..., 3] == 0] = 0
        return Image.fromarray(out, "RGBA")

    def geometry(self, bones=None):
        self.pack()
        bones = bones or self.bones
        out_bones = []
        for b in bones:
            entry = {"name": b["name"]}
            if b.get("parent"):
                entry["parent"] = b["parent"]
            entry["pivot"] = b["pivot"]
            if b.get("rotation"):
                entry["rotation"] = b["rotation"]
            if b.get("locators"):
                entry["locators"] = b["locators"]
            cubes = []
            for c in self.cubes:
                if c.bone != b["name"]:
                    continue
                cube = {"origin": c.origin, "size": c.size}
                if c.inflate:
                    cube["inflate"] = c.inflate
                if c.rotation:
                    cube["pivot"] = c.pivot
                    cube["rotation"] = c.rotation
                src = c.like if c.like is not None else c
                rects = dict(src.rects)
                for f, g in getattr(src, "same", {}).items():
                    rects[f] = rects[g]
                cube["uv"] = {
                    f: {"uv": [r[0], r[1]], "uv_size": [r[2], r[3]]}
                    for f, r in rects.items()
                }
                cubes.append(cube)
            if cubes:
                entry["cubes"] = cubes
            out_bones.append(entry)
        return {
            "description": {
                "identifier": self.identifier,
                "texture_width": TEX,
                "texture_height": TEX,
                "visible_bounds_width": 2,
                "visible_bounds_height": 3,
                "visible_bounds_offset": [0, 1.5, 0],
            },
            "bones": out_bones,
        }


# Standard Bedrock player bones (from geometry.humanoid.custom), in the order
# the vanilla rig lists them. Animations and attachables rely on these names.
PLAYER_BONES = [
    {"name": "root", "pivot": [0, 0, 0]},
    {"name": "waist", "parent": "root", "pivot": [0, 12, 0]},
    {"name": "body", "parent": "waist", "pivot": [0, 24, 0]},
    {"name": "jacket", "parent": "body", "pivot": [0, 24, 0]},
    {"name": "cape", "parent": "body", "pivot": [0, 24, 3]},
    {"name": "head", "parent": "body", "pivot": [0, 24, 0]},
    {"name": "hat", "parent": "head", "pivot": [0, 24, 0]},
    {"name": "leftArm", "parent": "body", "pivot": [5, 22, 0]},
    {"name": "leftSleeve", "parent": "leftArm", "pivot": [5, 22, 0]},
    {"name": "leftItem", "parent": "leftArm", "pivot": [6, 15, 1]},
    {"name": "rightArm", "parent": "body", "pivot": [-5, 22, 0]},
    {"name": "rightSleeve", "parent": "rightArm", "pivot": [-5, 22, 0]},
    {"name": "rightItem", "parent": "rightArm", "pivot": [-6, 15, 1],
     "locators": {"lead_hold": [-6, 15, 1]}},
    {"name": "leftLeg", "parent": "root", "pivot": [1.9, 12, 0]},
    {"name": "leftPants", "parent": "leftLeg", "pivot": [1.9, 12, 0]},
    {"name": "rightLeg", "parent": "root", "pivot": [-1.9, 12, 0]},
    {"name": "rightPants", "parent": "rightLeg", "pivot": [-1.9, 12, 0]},
]


SLIM_BONES = [dict(b) for b in PLAYER_BONES]
for _b in SLIM_BONES:
    if _b["name"] in ("leftArm", "leftSleeve"):
        _b["pivot"] = [5, 21.5, 0]
    elif _b["name"] in ("rightArm", "rightSleeve"):
        _b["pivot"] = [-5, 21.5, 0]


def add_standard_body(skin, head=True):
    """Body, arms and legs (+ overlay layers) in the standard HD skin layout.

    Slim skins (skin.slim) get the 3px Alex arms, offset like the vanilla rig.
    """
    if skin.slim:
        rx, lx, ay, aw = -7, 4, 11.5, 3
    else:
        rx, lx, ay, aw = -8, 4, 12, 4
    std = [
        ("body", "body", [-4, 12, -2], [8, 12, 4], (16, 16), 0),
        ("jacket", "jacket", [-4, 12, -2], [8, 12, 4], (16, 32), 0.25),
        ("rightArm", "rightArm", [rx, ay, -2], [aw, 12, 4], (40, 16), 0),
        ("rightSleeve", "rightSleeve", [rx, ay, -2], [aw, 12, 4], (40, 32), 0.25),
        ("leftArm", "leftArm", [lx, ay, -2], [aw, 12, 4], (32, 48), 0),
        ("leftSleeve", "leftSleeve", [lx, ay, -2], [aw, 12, 4], (48, 48), 0.25),
        ("rightLeg", "rightLeg", [-3.9, 0, -2], [4, 12, 4], (0, 16), 0),
        ("rightPants", "rightPants", [-3.9, 0, -2], [4, 12, 4], (0, 32), 0.25),
        ("leftLeg", "leftLeg", [-0.1, 0, -2], [4, 12, 4], (16, 48), 0),
        ("leftPants", "leftPants", [-0.1, 0, -2], [4, 12, 4], (0, 48), 0.25),
    ]
    if head:
        std = [("head", "head", [-4, 24, -4], [8, 8, 8], (0, 0), 0),
               ("hat", "hat", [-4, 24, -4], [8, 8, 8], (32, 0), 0.5)] + std
    for name, bone, origin, size, (u, v), inflate in std:
        skin.add(Cube(name, bone, origin, size, box_rects(u, v, size), inflate))


def noise(shape, seed, amount):
    rs = np.random.RandomState(seed)
    return 1.0 + (rs.rand(*shape) - 0.5) * 2 * amount


def write_geometry(path, geometries):
    data = {"format_version": "1.12.0", "minecraft:geometry": geometries}
    with open(path, "w") as fh:
        json.dump(data, fh, indent=2)
        fh.write("\n")
