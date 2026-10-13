"""Pumpkin Prankster: oversized jack-o'-lantern head, open black jacket with
orange trim, maroon hoodie, ripped charcoal jeans and chunky orange sneakers.
"""

import numpy as np

from skinlib import (Cube, Face, Skin, add_standard_body, noise, packed_rects,
                     rgb)

ID = "geometry.MidnightMischief.PumpkinPrankster"
TEXTURE = "pumpkin_prankster.png"
NAME = "Pumpkin Prankster"
LOC = "PumpkinPrankster"
DETAILS = [
    ("face", "Jack-o'-lantern head (3D)", {"yaw": 22, "pitch": 10, "dist": 40, "target": 27, "fov": 30}),
    ("top", "Pumpkin top + stem", {"yaw": 25, "pitch": 55, "dist": 100}),
    ("shoes", "3D sneakers + tongues", {"yaw": 35, "pitch": 18, "dist": 34, "target": 4, "fov": 30}),
]
REF_BOX = (190, 95, 410, 535)  # crop of reference/midnight_mischief_lineup.webp

# ------------------------------------------------------------------ palette
PUMP = (234, 100, 16)
PUMP_HI = (252, 134, 30)
PUMP_GROOVE = (150, 42, 4)
PUMP_DEEP = (104, 26, 2)
GLOW_CORE = (255, 240, 120)
GLOW = (255, 216, 62)
GLOW_RIM = (252, 176, 36)
GLOW_WALL = (214, 104, 14)
STEM = (74, 46, 22)
STEM_HI = (104, 70, 30)

JK = (44, 32, 40)          # jacket black (warm purple tint like the art)
JK_DARK = (30, 22, 28)
JK_HI = (60, 46, 56)
TRIM = (248, 116, 22)
TRIM_HI = (255, 150, 44)
TRIM_DARK = (204, 74, 6)

SHIRT = (92, 36, 38)
SHIRT_DARK = (58, 22, 28)
SHIRT_HI = (114, 48, 50)
PRINT = (140, 86, 98)
PRINT_DARK = (118, 68, 82)
STRING = (176, 128, 120)

PANTS = (46, 38, 52)
PANTS_DARK = (34, 28, 40)
PANTS_HI = (62, 54, 70)
PANTS_WORN = (78, 70, 86)
STITCH = (240, 104, 20)

SKIN = (196, 126, 86)
SKIN_DARK = (170, 102, 66)
SKIN_HI = (212, 146, 104)

SHOE = (242, 110, 20)
SHOE_HI = (255, 140, 40)
SHOE_DARK = (196, 70, 8)
LACE = (250, 244, 236)
LACE_DARK = (214, 204, 196)
SOLE = (246, 230, 210)
SOLE_DARK = (210, 192, 174)


def build():
    skin = Skin(ID)
    add_standard_body(skin, head=False)

    # Oversized pumpkin replaces the vanilla head; slightly inflated so it
    # encloses a worn helmet instead of z-fighting with it.
    skin.add(Cube("pumpkin", "head", [-5, 24, -5], [10, 8, 10], packed_rects(
        [10, 8, 10], {"east": (0, 0), "north": (20, 0), "west": (40, 0),
                      "south": (60, 0), "up": (80, 0), "down": (100, 0)}),
        inflate=0.25))

    # Chunky sneakers + raised tongues, riding on the leg bones so they walk.
    for side, x0, u0 in (("right", -4.5, 0), ("left", 0.0, 40)):
        skin.add(Cube(f"{side}Shoe", f"{side}Leg", [x0, 0, -3.5], [4.5, 3, 6],
                      packed_rects([4.5, 3, 6], {
                          "up": (u0, 20), "down": (u0 + 9, 20),
                          "east": (u0 + 18, 20), "west": (u0 + 18, 26),
                          "north": (u0 + 30, 20), "south": (u0 + 30, 26)})))
    for side, x0, v0 in (("right", -3.25, 20), ("left", 1.25, 22)):
        skin.add(Cube(f"{side}Tongue", f"{side}Leg", [x0, 3, -3.25], [2, 1, 1],
                      packed_rects([2, 1, 1], {
                          "north": (80, v0), "south": (84, v0),
                          "east": (88, v0), "west": (90, v0),
                          "up": (92, v0), "down": (96, v0)})))

    paint_pumpkin(skin)
    paint_torso(skin)
    paint_arms(skin)
    paint_legs(skin)
    paint_shoes(skin)
    return skin


# ================================================================== pumpkin
GROOVES = {0: 0.62, 19: 0.62, 3: 0.74, 16: 0.74, 7: 0.76, 12: 0.76}


def rib_factor(col):
    """Brightness across a 20px pumpkin face: compressed outer ribs."""
    if col in GROOVES:
        return GROOVES[col]
    seg = [(1, 2), (4, 6), (8, 11), (13, 15), (17, 18)]
    for a, b in seg:
        if a <= col <= b:
            mid = (a + b) / 2
            half = (b - a) / 2 + 0.5
            t = 1 - abs(col - mid) / half
            base = 0.92 if (a, b) in ((1, 2), (17, 18)) else 1.0
            return base * (0.9 + 0.2 * t)
    return 1.0


def pumpkin_side(face, seed):
    face.fill(PUMP)
    prof = np.array([rib_factor(c) for c in range(face.w)])[None, :]
    vert = np.ones(face.h)
    vert[:2] = [0.78, 0.9]
    vert[-3:] = [0.94, 0.86, 0.76]
    face.shade(prof * vert[:, None] * noise((face.h, face.w), seed, 0.05))
    # deep groove texels get a redder, darker hue
    for c, f in GROOVES.items():
        if f < 0.7:
            continue
        col = face.rgba[:, c, :3]
        face.rgba[:, c, :3] = col * [0.92, 0.8, 0.6]


EYE = [
    "YY....",
    "YYYY..",
    "YYYYYY",
    "YYYYYY",
    ".YYYYY",
    "..YYY.",
]
MOUTH_LEFT = [  # left half of the grin (cols 0-9), mirrored for the right
    ".Y........",
    ".YYY.YYYY.",
    "..YYYYYYYY",
    "..YYYYYYYY",
    "...YYY.YYY",
]


def carve(face, mask):
    """Glowing cut-out: bright core, rim, and a lit inner wall on top."""
    h, w = mask.shape
    pad = np.pad(mask, 1)
    # distance-ish: count lit neighbours to find the core
    neigh = sum(np.roll(np.roll(pad, dy, 0), dx, 1)
                for dy in (-1, 0, 1) for dx in (-1, 0, 1))[1:-1, 1:-1]
    above = np.pad(mask, ((1, 0), (0, 0)))[:-1]   # texel above is cut too?
    left = np.pad(mask, ((0, 0), (1, 0)))[:, :-1]
    for r in range(h):
        for c in range(w):
            if not mask[r, c]:
                continue
            if not above[r, c]:
                col = GLOW_WALL          # the carved wall under the top lip
            elif not left[r, c]:
                col = GLOW_RIM
            elif neigh[r, c] >= 9:
                col = GLOW_CORE
            else:
                col = GLOW
            face.set(r, c, col)
    # warm light spilling onto the skin right around the cuts
    grown = np.zeros_like(mask)
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            grown |= np.roll(np.roll(mask, dy, 0), dx, 1)
    spill = grown & ~mask
    face.rgba[spill, :3] = face.rgba[spill, :3] * 0.6 + np.array(PUMP_HI) * 0.4


def paint_pumpkin(skin):
    for i, f in enumerate(("east", "north", "west", "south")):
        pumpkin_side(skin.face("pumpkin", f), 10 + i)

    front = skin.face("pumpkin", "north")
    mask = np.zeros((front.h, front.w), bool)
    for r, line in enumerate(EYE):
        for c, ch in enumerate(line):
            if ch == "Y":
                mask[4 + r, 2 + c] = True
                mask[4 + r, 17 - c] = True
    for r, line in enumerate(MOUTH_LEFT):
        for c, ch in enumerate(line):
            if ch == "Y":
                mask[10 + r, c] = True
                mask[10 + r, 19 - c] = True
    carve(front, mask)

    # stitched scar on the character's right side, near the front corner
    side = skin.face("pumpkin", "east")
    for r in range(2, 14):
        side.set(r, 15, PUMP_DEEP)
    for r in (4, 7, 10):
        for c in (14, 16):
            side.set(r, c, PUMP_DEEP)
        side.set(r - 1, 14, PUMP_GROOVE)
    # a couple of blemishes so the sides are not identical
    for f, spots in (("west", [(6, 9), (10, 5), (12, 14)]),
                     ("south", [(4, 11), (9, 4), (12, 15)])):
        face = skin.face("pumpkin", f)
        for r, c in spots:
            face.rgba[r, c, :3] *= 0.86

    # top: ribs radiate from a stem scar
    top = skin.face("pumpkin", "up")
    top.fill(PUMP)
    yy, xx = np.mgrid[0:20, 0:20]
    dx, dz = xx - 9.5, yy - 9.5
    rad = np.maximum(abs(dx), abs(dz)) / 9.5
    fac = 0.84 + 0.22 * np.clip(rad * 1.5, 0, 1)        # dips toward the stem
    fac = np.where(rad > 0.95, fac * 0.86, fac)          # rolls off the edges
    # grooves run from the stem out to where the side grooves meet the rim
    groove = np.zeros((20, 20), bool)
    rim = [(9.5, 0), (9.5, 19), (0, 9.5), (19, 9.5),
           (0, 0), (19, 0), (0, 19), (19, 19)]
    for ex, ez in rim:
        for t in np.linspace(0.25, 1, 40):
            c = int(round(9.5 + (ex - 9.5) * t))
            r = int(round(9.5 + (ez - 9.5) * t))
            groove[min(max(r, 0), 19), min(max(c, 0), 19)] = True
    fac = np.where(groove, fac * 0.8, fac)
    top.shade(fac * noise((top.h, top.w), 21, 0.035))
    stem = [
        ".SS.",
        "SHSS",
        "SSHS",
        ".SS.",
    ]
    top.stamp(stem, {"S": STEM, "H": STEM_HI}, top=8, left=8)

    bottom = skin.face("pumpkin", "down")
    bottom.fill(PUMP)
    yy, xx = np.mgrid[0:20, 0:20]
    rad = np.maximum(abs(xx - 9.5), abs(yy - 9.5))
    bottom.shade(0.72 * noise((20, 20), 22, 0.05))
    hole = rad < 5
    bottom.fill((96, 36, 6), hole)
    bottom.fill((150, 60, 10), (rad >= 4) & hole)


# ==================================================================== torso
def jacket_texels(face, seed, hem_rows=(22, 23)):
    face.fill(JK)
    face.shade(noise((face.h, face.w), seed, 0.1))
    # soft vertical folds
    folds = 1 + 0.08 * np.sin(face.col * 1.7 + seed)
    face.shade(folds)
    for r in hem_rows:
        face.fill(TRIM if r == hem_rows[0] else TRIM_DARK, face.row == r)
    face.shade(noise((face.h, face.w), seed + 100, 0.04))


def paint_torso(skin):
    for layer, seed in (("body", 30), ("jacket", 40)):
        front = skin.face(layer, "north")
        jacket_texels(front, seed)
        shirt = (front.col >= 5) & (front.col <= 10)
        # shirt / hoodie seen through the open jacket
        front.fill(SHIRT, shirt)
        g = np.clip(1.05 - front.row / 60, 0.7, 1.1)
        front.shade(np.where(shirt, g * noise(front.rgba.shape[:2], seed + 1, 0.06), 1))
        for r in (0, 1):
            front.fill(SHIRT_DARK if r == 0 else (74, 28, 32), shirt & (front.row == r))
        front.fill(SHIRT_DARK, shirt & (front.row == 23))
        front.fill((74, 28, 32), shirt & (front.row == 22))
        front.fill(SHIRT_DARK, shirt & (front.row == 17))           # fold
        # hood tab + drawstrings with metal tips
        front.stamp(["TT"], {"T": TRIM_DARK}, top=2, left=7)
        for c in (6, 9):
            for r in range(2, 8):
                front.set(r, c, STRING if r % 2 else (156, 110, 104))
            front.set(8, c, (220, 210, 200))
        # chest print
        front.fill(PRINT, (front.row >= 9) & (front.row <= 14)
                   & (front.col >= 6) & (front.col <= 9))
        front.fill(PRINT_DARK, (front.row == 14) & (front.col >= 6) & (front.col <= 9))
        front.fill(PRINT_DARK, (front.col == 9) & (front.row >= 9) & (front.row <= 14))
        front.set(9, 6, (156, 102, 112))
        # orange trim down both jacket edges, bright on the inner edge
        for c, col in ((3, TRIM_DARK), (4, TRIM), (11, TRIM), (12, TRIM_DARK)):
            front.fill(col, front.col == c)
        for c in (4, 11):
            for r in range(0, 24, 5):
                front.set(r, c, TRIM_HI)
        # zip-pocket pulls on each panel
        front.stamp(["T.", "TT", ".T"], {"T": TRIM}, top=16, left=1)
        front.stamp(["T.", "TT", ".T"], {"T": TRIM}, top=16, left=13, mirror=True)
        front.fill(TRIM, (front.row == 22) & ~shirt)
        front.fill(TRIM_DARK, (front.row == 23) & ~shirt)
        if layer == "jacket":
            front.clear(shirt)

        back = skin.face(layer, "south")
        jacket_texels(back, seed + 2)
        back.fill(TRIM, back.row == 0)
        back.fill(TRIM_DARK, back.row == 1)
        # little jack-o'-lantern patch between the shoulders
        patch = [
            "..GG..",
            ".OOOO.",
            "OdOOdO",
            "OOOOOO",
            "OdddOO",
            ".OOOO.",
        ]
        back.stamp(patch, {"O": TRIM, "d": JK_DARK, "G": (92, 120, 40)}, top=6, left=5)
        for f, s in (("east", 4), ("west", 6)):
            side = skin.face(layer, f)
            jacket_texels(side, seed + s)
            if layer == "jacket":
                side.fill(TRIM, side.row == 0)
            # side seam
            side.shade(np.where(side.col == 4, 0.8, 1.0))
        top = skin.face(layer, "up")
        top.fill(JK)
        top.shade(noise((top.h, top.w), seed + 7, 0.1))
        top.fill(TRIM, (top.col == 4) | (top.col == 11))
        bottom = skin.face(layer, "down")
        bottom.fill(JK_DARK)
        bottom.shade(noise((bottom.h, bottom.w), seed + 8, 0.1))
        if layer == "jacket":
            bottom.clear((bottom.col >= 5) & (bottom.col <= 10) & (bottom.row >= 5))
        else:
            bottom.fill(SHIRT_DARK, (bottom.col >= 5) & (bottom.col <= 10))


# ===================================================================== arms
def sleeve_texels(face, seed, outer_cols):
    face.fill(JK)
    face.shade(noise((face.h, face.w), seed, 0.1))
    face.shade(1 + 0.07 * np.sin(face.row * 1.3 + seed))
    face.fill(TRIM, (face.row >= 16) & (face.row <= 17))
    face.fill(TRIM_DARK, face.row == 18)
    face.fill(JK_DARK, (face.row >= 19) & (face.row <= 20))
    face.fill(JK, (face.row == 19) & (face.col % 3 == 0))
    face.fill(SKIN, face.row >= 21)
    face.shade(np.where(face.row == 21, 0.86, 1.0))
    face.fill(SKIN_HI, (face.row == 22) & (face.col % 4 == 1))
    face.shade(noise((face.h, face.w), seed + 50, 0.03))
    for c in outer_cols:
        for r in (16, 17):
            face.set(r, c, TRIM_HI)


def paint_arms(skin):
    for arm, sleeve, outer, inner, seed in (
            ("rightArm", "rightSleeve", "east", "west", 60),
            ("leftArm", "leftSleeve", "west", "east", 70)):
        for layer, s in ((arm, seed), (sleeve, seed + 5)):
            for f in ("north", "south", "east", "west"):
                face = skin.face(layer, f)
                sleeve_texels(face, s + len(f), outer_cols=[1, 5])
            # shoulder patch on the front, wrapping round the outside
            front = skin.face(layer, "north")
            pc = (0, 1) if arm == "rightArm" else (6, 7)
            for r in (4, 5, 6):
                for c in pc:
                    front.set(r, c, TRIM if r < 6 else TRIM_DARK)
            out = skin.face(layer, outer)
            for r in (4, 5, 6):
                out.set(r, 7, TRIM if r < 6 else TRIM_DARK)
            out.set(11, 3, TRIM)
            out.set(11, 4, TRIM_DARK)
            out.set(12, 3, TRIM_DARK)
            # inner side is in shadow
            skin.face(layer, inner).shade(0.9)
            top = skin.face(layer, "up")
            top.fill(JK)
            top.shade(noise((8, 8), s + 9, 0.1))
            oc = 0 if arm == "rightArm" else 7
            top.fill(TRIM, (top.col == oc) & (top.row >= 2) & (top.row <= 5))
            bottom = skin.face(layer, "down")
            if layer == arm:
                bottom.fill(SKIN_DARK)
                bottom.shade(noise((8, 8), s + 10, 0.04))
            else:
                bottom.clear()
            if layer == sleeve:
                for f in ("north", "south", "east", "west"):
                    face = skin.face(layer, f)
                    face.clear(face.row >= 21)


# ===================================================================== legs
def pants_texels(face, seed):
    face.fill(PANTS)
    face.shade(noise((face.h, face.w), seed, 0.1))
    face.shade(1 + 0.06 * np.sin(face.row * 0.9 + face.col * 0.4 + seed))
    face.shade(np.where(face.row == 17, 0.75, 1.0))              # shoe shadow
    face.fill(SHOE_DARK, face.row >= 18)                          # under shoe


def paint_legs(skin):
    for leg, pants, outer, seed in (("rightLeg", "rightPants", "east", 80),
                                    ("leftLeg", "leftPants", "west", 90)):
        for f in ("north", "south", "east", "west"):
            pants_texels(skin.face(leg, f), seed + len(f))
        front = skin.face(leg, "north")
        # worn knee
        knee = [
            ".ww.",
            "wWWw",
            "wWw.",
            ".w..",
        ]
        front.stamp(knee, {"w": PANTS_HI, "W": PANTS_WORN}, top=9,
                    left=2 if leg == "rightLeg" else 3)
        # frayed rips with orange stitching (inner thigh on the right leg,
        # outer thigh on the left, as in the art)
        if leg == "rightLeg":
            rip = [(2, 6), (3, 6), (3, 5), (4, 5), (5, 4), (6, 4), (6, 3)]
        else:
            rip = [(2, 4), (3, 5), (4, 5), (5, 6), (6, 6), (5, 7)]
        for i, (r, c) in enumerate(rip):
            front.set(r, c, STITCH if i % 2 == 0 else PANTS_WORN)
        back = skin.face(leg, "south")
        back.stamp(["PP", "PP"], {"P": PANTS_HI}, top=3, left=3)    # pocket
        for f in ("east", "west"):
            if f != outer:
                skin.face(leg, f).shade(0.88)
        skin.face(leg, outer).stamp(["w.", ".w", "w."], {"w": PANTS_WORN}, top=7, left=3)
        top = skin.face(leg, "up")
        top.fill(PANTS_DARK)
        bottom = skin.face(leg, "down")
        bottom.fill(SOLE_DARK)

        # overlay: 3D knee patch and rolled cuff only
        for f in ("north", "south", "east", "west"):
            face = skin.face(pants, f)
            pants_texels(face, seed + 30 + len(f))
            keep = np.zeros((face.h, face.w), bool)
            if f == "north":
                kc = 2 if leg == "rightLeg" else 3
                patch = (face.row >= 9) & (face.row <= 12) & \
                    (face.col >= kc) & (face.col <= kc + 3)
                face.fill(PANTS_WORN, patch)
                face.shade(noise((24, 8), seed + 40, 0.06))
                face.fill(PANTS_HI, patch & ((face.row == 9) | (face.row == 12)))
                for r, c in ((9, kc), (12, kc + 3)):
                    face.set(r, c, PANTS_DARK)
                keep |= patch
            face.clear(~keep)
        skin.face(pants, "up").clear()
        skin.face(pants, "down").clear()


# ==================================================================== shoes
def paint_shoes(skin):
    for side, outer in (("right", "east"), ("left", "west")):
        shoe = f"{side}Shoe"
        seed = 120 if side == "right" else 140
        for f in ("north", "south", "east", "west"):
            face = skin.face(shoe, f)
            face.fill(SHOE)
            face.shade(noise((face.h, face.w), seed + len(f), 0.06))
            face.fill(SHOE_DARK, face.row == 3)
            face.fill(SOLE, face.row == 4)
            face.fill(SOLE_DARK, face.row == 5)
            face.fill(SHOE_HI, face.row == 0)
        inner_col = 8 if side == "right" else 0
        for f in ("north", "up"):
            face = skin.face(shoe, f)
            face.shade(np.where(face.col == inner_col, 0.72, 1.0))
        toe = skin.face(shoe, "north")
        toe.fill(LACE, (toe.row == 1) & (toe.col >= 2) & (toe.col <= 6))
        toe.fill(LACE_DARK, (toe.row == 1) & (toe.col == 6))
        for f in ("east", "west"):
            face = skin.face(shoe, f)
            # col 0 is the heel on the outer (east) side of the right shoe;
            # on the west face col 0 is the toe.
            heel_first = f == "east"
            for c in range(face.w):
                k = c if heel_first else face.w - 1 - c
                if 3 <= k <= 8:
                    face.set(2, c, LACE if f == outer else LACE_DARK)
                if k <= 1:
                    for r in (0, 1, 2):
                        face.set(r, c, SHOE_DARK)
        heel = skin.face(shoe, "south")
        heel.fill(SHOE_DARK, (heel.col >= 3) & (heel.col <= 5) & (heel.row <= 2))
        heel.set(0, 4, LACE)
        top = skin.face(shoe, "up")
        top.fill(SHOE)
        top.shade(noise((top.h, top.w), seed + 9, 0.06))
        top.fill(SHOE_HI, (top.col == 0) | (top.col == top.w - 1))
        top.shade(np.where(top.col == inner_col, 0.72, 1.0))
        sole = skin.face(shoe, "down")
        sole.fill(SOLE_DARK)
        sole.fill(SOLE, (sole.row + sole.col) % 3 == 0)

        tongue = f"{side}Tongue"
        for f in ("north", "south", "east", "west"):
            face = skin.face(tongue, f)
            face.fill(SHOE_DARK if f != "north" else SHOE)
        t_front = skin.face(tongue, "north")
        t_front.fill(LACE, t_front.row == 1)
        t_front.set(1, 3, LACE_DARK)
        t_up = skin.face(tongue, "up")
        t_up.fill(SHOE_HI)
        skin.face(tongue, "down").fill(SHOE_DARK)
