"""Reusable painting recipes shared by the Midnight Mischief skins."""

import numpy as np

from skinlib import noise

SIDES = ("north", "south", "east", "west")


def cloth(face, base, seed, var=0.09, fold=0.06, freq=1.3, mask=None):
    """Fabric: base colour, per-texel value noise and soft horizontal folds."""
    old = face.rgba.copy()
    face.fill(base)
    face.shade(noise((face.h, face.w), seed, var))
    face.shade(1 + fold * np.sin(face.row * freq + face.col * 0.35 + seed))
    if mask is not None:
        face.rgba = np.where(mask[..., None], face.rgba, old)


def hair(face, base, dark, light, seed, mask=None, vertical=True, shine=None):
    """Clumped, gently wavy strands: lanes 1-3 texels wide in dark/base/light,
    a soft wave running down each lane, and optional shine highlights."""
    old = face.rgba.copy()
    rs = np.random.RandomState(seed)
    n = face.w if vertical else face.h
    lane_of, tone, phase = np.zeros(n, int), [], []
    i = 0
    while i < n:
        w = rs.choice([1, 2, 2, 3])
        lane_of[i:i + w] = len(tone)
        tone.append(rs.choice([0, 1, 1, 2]) if not tone or tone[-1] != 0 else rs.choice([1, 2]))
        phase.append(rs.rand() * 6.28)
        i += w
    tone, phase = np.array(tone), np.array(phase)
    along = face.row if vertical else face.col
    lane = lane_of[face.col] if vertical else lane_of[face.row]
    pal = np.array([dark, base, light], float)
    face.rgba[..., :3] = pal[tone[lane]]
    face.rgba[..., 3] = 255
    wave = np.sin(along * 0.85 + phase[lane])
    face.shade(1 + 0.1 * wave)
    if shine is not None:
        face.fill(shine, (wave > 0.92) & (tone[lane] == 2))
    face.shade(noise((face.h, face.w), seed + 1, 0.025))
    if mask is not None:
        face.rgba = np.where(mask[..., None], face.rgba, old)


def skin_tone(face, base, seed, var=0.03):
    face.fill(base)
    face.shade(noise((face.h, face.w), seed, var))


def rows(face, r0, r1, color, mask=None):
    m = (face.row >= r0) & (face.row <= r1)
    if mask is not None:
        m &= mask
    face.fill(color, m)


def box(face, r0, c0, r1, c1):
    return (face.row >= r0) & (face.row <= r1) & (face.col >= c0) & (face.col <= c1)


def copy_layer(skin, src, dst):
    for f in SIDES + ("up", "down"):
        if (src, f) in skin.faces and (dst, f) in skin.faces:
            skin.face(dst, f).rgba = skin.face(src, f).rgba.copy()


def sides(skin, name):
    return [skin.face(name, f) for f in SIDES]


# ------------------------------------------------------------- footwear
def add_footwear(skin, height=3.0, length=6.0, toe=1.5, tongue=True, width=4.5):
    """Chunky 3D shoes/boots on both leg bones (+ optional raised tongues)."""
    z0 = -2 - toe
    for side, x0 in (("right", -width), ("left", 0.0)):
        skin.acc(f"{side}Shoe", f"{side}Leg", [x0, 0, z0], [width, height, length],
                 lowres=("up", "down"))
        if tongue:
            cx = -2.25 if side == "right" else 2.25
            skin.acc(f"{side}Tongue", f"{side}Leg", [cx - 1, height, -3.25], [2, 1, 1])
    return height


def paint_sneakers(skin, pal, seed, pal_left=None, stripe=True):
    """pal keys: upper, hi, dark, lace, lace_dark, sole, sole_dark."""
    for side in ("right", "left"):
        p = pal if side == "right" or pal_left is None else pal_left
        shoe = f"{side}Shoe"
        outer = "east" if side == "right" else "west"
        for f in SIDES:
            face = skin.face(shoe, f)
            h = face.h
            face.fill(p["upper"])
            face.shade(noise((h, face.w), seed + len(f), 0.06))
            rows(face, 0, 0, p["hi"])
            rows(face, h - 3, h - 3, p["dark"])
            rows(face, h - 2, h - 2, p["sole"])
            rows(face, h - 1, h - 1, p["sole_dark"])
        toe = skin.face(shoe, "north")
        rows(toe, 1, 1, p["lace"], (toe.col >= 2) & (toe.col <= toe.w - 3))
        for f in ("east", "west"):
            face = skin.face(shoe, f)
            heel_first = f == "east"
            for c in range(face.w):
                k = c if heel_first else face.w - 1 - c
                if stripe and 3 <= k <= face.w - 4:
                    face.set(face.h - 4, c, p["lace"] if f == outer else p["lace_dark"])
                if k <= 1:
                    for r in range(0, face.h - 3):
                        face.set(r, c, p["dark"])
        heel = skin.face(shoe, "south")
        heel.fill(p["dark"], (heel.col >= 3) & (heel.col <= heel.w - 4) & (heel.row <= heel.h - 4))
        heel.set(0, heel.w // 2, p["lace"])
        top = skin.face(shoe, "up")
        top.fill(p["upper"])
        top.shade(noise((top.h, top.w), seed + 9, 0.06))
        top.fill(p["hi"], (top.col == 0) | (top.col == top.w - 1))
        for f in ("north", "up"):
            face = skin.face(shoe, f)
            face.shade(np.where(face.col == (face.w - 1 if side == "right" else 0), 0.72, 1.0))
        sole = skin.face(shoe, "down")
        sole.fill(p["sole_dark"])
        sole.fill(p["sole"], (sole.row + sole.col) % 3 == 0)
        tongue = f"{side}Tongue"
        if (tongue, "north") in skin.faces:
            for f in SIDES:
                skin.face(tongue, f).fill(p["dark"] if f != "north" else p["upper"])
            t_front = skin.face(tongue, "north")
            rows(t_front, 1, 1, p["lace"])
            t_front.set(1, 3, p["lace_dark"])
            skin.face(tongue, "up").fill(p["hi"])
            skin.face(tongue, "down").fill(p["dark"])


def paint_boots(skin, pal, seed, straps=(2, 5)):
    """Taller boots: pal keys upper, hi, dark, strap, strap_dark, sole, sole_dark."""
    for side in ("right", "left"):
        shoe = f"{side}Shoe"
        for f in SIDES:
            face = skin.face(shoe, f)
            h = face.h
            face.fill(pal["upper"])
            face.shade(noise((h, face.w), seed + len(f), 0.08))
            rows(face, 0, 0, pal["hi"])
            rows(face, h - 3, h - 3, pal["dark"])
            rows(face, h - 2, h - 1, pal["sole"])
            rows(face, h - 1, h - 1, pal["sole_dark"])
            for r in straps:
                if f == "north":
                    rows(face, r, r, pal["strap"], (face.col >= 1) & (face.col <= face.w - 2))
                    face.set(r, face.w // 2, pal["strap_dark"])
                elif f in ("east", "west"):
                    front = face.col >= face.w // 2 if f == "east" else face.col < face.w // 2
                    rows(face, r, r, pal["strap"], front)
        top = skin.face(shoe, "up")
        top.fill(pal["upper"])
        top.shade(noise((top.h, top.w), seed + 9, 0.08))
        top.fill(pal["hi"], (top.col == 0) | (top.col == top.w - 1) | (top.row == top.h - 1))
        sole = skin.face(shoe, "down")
        sole.fill(pal["sole_dark"])
        for f in ("north", "up"):
            face = skin.face(shoe, f)
            face.shade(np.where(face.col == (face.w - 1 if side == "right" else 0), 0.72, 1.0))


def clear_under_shoes(skin, height, layers=("rightPants", "leftPants")):
    """Overlay texels hidden inside the shoes would poke out; drop them."""
    cut = 24 - int(round(height * 2))
    for name in layers:
        for face in sides(skin, name):
            face.clear(face.row >= cut)
        skin.face(name, "down").clear()


def eye_glow(face, cells, core, mid, rim):
    """cells: list of (r, c); brightest in the middle, rim on the edge."""
    s = set(cells)
    for r, c in cells:
        n = sum((r + dr, c + dc) in s for dr in (-1, 0, 1) for dc in (-1, 0, 1))
        face.set(r, c, core if n >= 9 else (mid if n >= 6 else rim))
