"""Saturna: lavender ringed-planet alien with big amber eyes, a butterscotch
bob banded like Saturn's clouds, pointed ears, a tilted 3D ring (with its
Cassini gap and a tiny moon riding on it), a starry indigo dress with a
flared 3D skirt, cream opera gloves and tall platform boots.
"""

import numpy as np

from paintkit import (SIDES, add_footwear, box, clear_under_shoes, cloth,
                      gradient, hair, rows, skin_tone, starfield)
from skinlib import Skin, add_standard_body, noise

ID = "geometry.SolarSystem.Saturna"
TEXTURE = "saturna.png"
NAME = "Saturna"
LOC = "Saturna"
DETAILS = [
    ("face", "Amber eyes + pointed ears", {"yaw": 22, "pitch": 6, "dist": 48, "target": 27, "fov": 30}),
    ("ring", "Tilted 3D ring + moon", {"yaw": 35, "pitch": 32, "dist": 70, "target": 25, "fov": 30}),
    ("skirt", "Flared starry skirt", {"yaw": -30, "pitch": 8, "dist": 64, "target": 14, "fov": 30}),
]

SKIN = (214, 196, 242)
SKIN_D = (188, 166, 226)
SKIN_S = (170, 146, 212)
BLUSH = (246, 168, 206)
CREAM = (250, 234, 194)
BUTTER = (238, 200, 124)
CARAMEL = (206, 150, 80)
TAN = (172, 116, 60)
TAN_D = (130, 82, 40)
AMBER = (230, 150, 30)
AMBER_L = (255, 206, 90)
LASH = (52, 30, 62)
INDIGO = (44, 36, 104)
INDIGO_D = (30, 24, 74)
INDIGO_H = (66, 56, 140)
GOLD = (246, 196, 72)
GOLD_D = (190, 136, 40)
STAR = (255, 240, 180)
RING_A = (255, 244, 214)
RING_A2 = (240, 222, 178)
RING_B = (255, 206, 120)
RING_B2 = (236, 176, 90)
RING_C = (196, 150, 110)
MOON = (226, 150, 70)

# the ring: a 16-sided band round the head, in its own tilted bone
RY = 29.5
R_IN, R_OUT, SEG = 6.6, 9.6, 4.0
PX_RING = 3


def build():
    skin = Skin(ID, slim=True)
    add_standard_body(skin)
    skin.bone("ring", "head", [0, RY, 0], rotation=[-12, 0, 20])
    depth = R_OUT - R_IN
    for k in range(16):
        # odd segments sit a hair higher so the overlapping corners don't flicker
        y = RY - 0.25 + (0.02 if k % 2 else 0)
        kw = dict(pivot=[0, RY, 0], rotation=[0, 22.5 * k, 0]) if k else {}
        if k == 0:
            skin.acc("ringSeg", "ring", [-SEG / 2, y, -R_OUT], [SEG, 0.5, depth], px=PX_RING,
                     lowres=("east", "west", "north", "south"))
        else:
            skin.acc(f"ringSeg{k}", "ring", [-SEG / 2, y, -R_OUT], [SEG, 0.5, depth], like="ringSeg", **kw)
    skin.acc("moon", "ring", [5.5, RY + 0.25, -5.8], [1.5, 1.5, 1.5], px=2)
    for side, x0 in (("Right", -5.0), ("Left", 4.0)):
        skin.acc(f"ear{side}", "head", [x0, 26.5, -0.5], [1, 2, 1.5], lowres=("up", "down"))
        tip_x = x0 - 0.5 if side == "Right" else x0 + 1
        skin.acc(f"earTip{side}", "head", [tip_x, 28, 0], [0.5, 1, 1], lowres=("up", "down", "north", "south"))
    # two space buns, banded like little gas giants
    skin.acc("bunRight", "head", [-4.75, 32.25, -0.5], [3, 2.5, 3])
    skin.acc("bunLeft", "head", [1.75, 32.25, -0.5], [3, 2.5, 3], like="bunRight")
    skin.acc("bunCapRight", "head", [-4.25, 34.75, 0], [2, 0.5, 2], lowres=("north", "south", "east", "west"))
    skin.acc("bunCapLeft", "head", [2.25, 34.75, 0], [2, 0.5, 2], like="bunCapRight")
    skin.acc("skirt", "body", [-4.5, 10.5, -2.5], [9, 3.5, 5], lowres=("up", "down"))
    h = add_footwear(skin, height=3.0, length=5.0, toe=1.0, tongue=False, width=4.25)
    paint_head(skin)
    paint_ring(skin)
    paint_body(skin)
    paint_arms(skin)
    paint_legs(skin, h)
    paint_boots(skin)
    return skin


HAIR = (150, 88, 48)
HAIR_D = (112, 60, 34)
HAIR_L = (186, 120, 64)
BAND_COLORS = [HAIR, HAIR_L, (226, 168, 92), HAIR_L, HAIR, HAIR_D]


def banded_hair(face, seed, mask=None, period=2):
    """Hair strands tinted in horizontal bands like Saturn's cloud belts."""
    old = face.rgba.copy()
    hair(face, HAIR, HAIR_D, HAIR_L, seed)
    strand = face.rgba[..., :3] / np.array(HAIR, float)
    y = np.round((face.Y - 24) * 2).astype(int)        # band by height on the model
    band = np.array(BAND_COLORS, float)[(y // period) % len(BAND_COLORS)]
    face.rgba[..., :3] = np.clip(band * strand, 0, 255)
    if mask is not None:
        face.rgba = np.where(mask[..., None], face.rgba, old)


BANGS = [5, 5, 4, 4, 5, 5, 4, 3, 3, 4, 5, 5, 4, 4, 5, 5]


def paint_head(skin):
    front = skin.face("head", "north")
    skin_tone(front, SKIN, 600, var=0.02)
    bangs = front.row <= np.array(BANGS)[front.col]
    sides = (front.col <= 0) | (front.col >= 15)
    banded_hair(front, 601, mask=bangs | (sides & (front.row <= 12)))
    front.shade(np.where((front.row == np.array(BANGS)[front.col] + 1) & ~bangs, 0.9, 1.0))
    # big glossy amber eyes
    eye = [
        "LLLL.",
        "WAAAL",
        "AHAAL",
        "AAYY.",
        ".YYY.",
    ]
    pal = {"L": LASH, "W": (255, 255, 255), "A": AMBER, "H": (255, 250, 230), "Y": AMBER_L}
    front.stamp(eye, pal, top=6, left=2)
    front.stamp(eye, pal, top=6, left=9, mirror=True)
    front.set(5, 1, LASH)
    front.set(5, 14, LASH)
    for c in (2, 3, 12, 13):
        front.set(11, c, BLUSH)
    # tiny ringed-planet freckle under one eye
    front.set(11, 11, SKIN_S)
    front.stamp(["M..M", ".MM."], {"M": (150, 70, 120)}, top=12, left=6)
    for f in ("east", "west", "south", "up"):
        face = skin.face("head", f)
        skin_tone(face, SKIN, 610 + len(f))
        if f in ("south", "up"):
            banded_hair(face, 620 + len(f))
        else:
            # hair to the jaw, except a gap where the ear pokes out
            near_front = face.col >= 13 if f == "east" else face.col <= 2
            ear = (face.row >= 7) & (face.row <= 10) & (face.col >= 6) & (face.col <= 9)
            banded_hair(face, 630 + len(f), mask=~near_front & ~ear | (face.row <= 3))
    skin_tone(skin.face("head", "down"), SKIN_D, 640)

    # hat layer: a fuller bob that flips out at the ends
    for f in SIDES + ("up", "down"):
        skin.face("hat", f).clear()
    hat_front = skin.face("hat", "north")
    banded_hair(hat_front, 650, mask=(hat_front.row <= np.array(BANGS)[hat_front.col] - 1))
    hat_front.clear((hat_front.col >= 6) & (hat_front.col <= 9) & (hat_front.row >= 2))
    for f in ("east", "west", "south"):
        face = skin.face("hat", f)
        banded_hair(face, 660 + len(f))
        if f != "south":
            near_front = face.col >= 13 if f == "east" else face.col <= 2
            face.clear(near_front & (face.row >= 3))
            face.clear((face.row >= 6) & (face.row <= 11) & (face.col >= 5) & (face.col <= 10))
        face.clear(face.row >= 14)
        face.clear((face.row == 13) & (face.col % 3 == 0))
    banded_hair(skin.face("hat", "up"), 670)

    for face in skin.each("bunRight"):
        banded_hair(face, 690 + face.w + len(face.face))
    for f in SIDES:
        face = skin.face("bunRight", f)
        face.shade(np.where((face.col == 0) | (face.col == face.w - 1), 0.85, 1.0))
        face.fill(GOLD, face.row == face.h - 1)         # gold hair tie
    for face in skin.each("bunCapRight"):
        banded_hair(face, 695 + face.w)
    for side in ("Right", "Left"):
        for name in (f"ear{side}", f"earTip{side}"):
            for face in skin.each(name):
                skin_tone(face, SKIN, 680 + face.w)
        inner = skin.face(f"ear{side}", "north")
        inner.fill(BLUSH, box(inner, 1, 0, 2, 0))


def paint_ring(skin):
    top = skin.face("ringSeg", "up")
    # rows run from the inner edge (row 0) to the outer edge (last row)
    bands = [RING_C, RING_C, RING_B2, RING_B, RING_B, RING_B2, None, RING_A2, RING_A]
    for r, col in enumerate(bands):
        if col is None:
            top.clear(top.row == r)                  # Cassini division
        else:
            top.fill(col, top.row == r)
    top.shade(noise((top.h, top.w), 700, 0.03))
    top.shade(1 + 0.05 * np.sin(top.col * 1.3))
    under = skin.face("ringSeg", "down")
    under.rgba = top.rgba[::-1].copy()
    for f in ("north", "south", "east", "west"):
        face = skin.face("ringSeg", f)
        face.fill(RING_B2)
    for face in skin.each("moon"):
        face.fill(MOON)
        face.shade(noise((face.h, face.w), 710 + face.w, 0.06))
        face.set(0, 0, (196, 120, 50))
        face.set(1, 2 % face.w, (196, 120, 50))
    skin.face("moon", "up").fill((240, 176, 100))


def dress(face, seed):
    cloth(face, INDIGO, seed, var=0.05, fold=0.04)
    starfield(face, seed + 1, density=0.05, colors=(STAR, (200, 200, 255)), twinkle=False)


def paint_body(skin):
    front = skin.face("body", "north")
    dress(front, 800)
    # sweetheart neckline
    neck = (front.row <= 2) | ((front.row == 3) & (front.col >= 3) & (front.col <= 12))
    neck &= ~((front.row == 3) & ((front.col == 7) | (front.col == 8)))
    tmp = front.rgba.copy()
    skin_tone(front, SKIN, 801)
    front.rgba = np.where(neck[..., None], front.rgba, tmp)
    rows(front, 4, 4, GOLD, ~neck & (front.col >= 2) & (front.col <= 13))
    for f in ("east", "west", "south"):
        face = skin.face("body", f)
        dress(face, 810 + len(f))
        rows(face, 0, 2, SKIN)
        rows(face, 3, 3, GOLD)
    # gold belt with a ringed-planet buckle
    for f in SIDES:
        face = skin.face("body", f)
        rows(face, 17, 18, GOLD)
        rows(face, 18, 18, GOLD_D)
    planet = [
        "..BBB..",
        "GGGGGGG",
        "..BBB..",
    ]
    front.stamp(planet, {"B": BUTTER, "G": (255, 240, 170)}, top=16, left=4)
    back = skin.face("body", "south")
    for r in range(6, 16, 3):
        back.set(r, 7, GOLD)
        back.set(r, 8, GOLD)
        back.set(r + 1, 6, GOLD_D)
        back.set(r + 1, 9, GOLD_D)
    skin_tone(skin.face("body", "up"), SKIN, 820)
    cloth(skin.face("body", "down"), INDIGO_D, 821)
    for face in skin.each("jacket"):
        face.clear()
    # ring-striped sash from shoulder to hip, tilted like the ring
    for f, sign in (("north", 1), ("south", -1)):
        jk = skin.face("jacket", f)
        d = jk.row - (4 + sign * (jk.col - 7.5) * 0.9)
        jk.fill(RING_A, (d >= 0) & (d < 1) & (jk.row >= 4) & (jk.row <= 16))
        jk.fill(RING_B, (d >= 1) & (d < 2.2) & (jk.row >= 4) & (jk.row <= 16))
        jk.fill(RING_B2, (d >= 2.2) & (d < 3) & (jk.row >= 4) & (jk.row <= 16))

    # flared skirt: indigo with stars, a gold hem and a ring-band trim
    for face in skin.each("skirt"):
        dress(face, 830 + face.w + face.h)
    for f in SIDES:
        face = skin.face("skirt", f)
        face.shade(1 + 0.12 * np.sin(face.col * 1.2))
        rows(face, face.h - 2, face.h - 2, RING_B)
        rows(face, face.h - 1, face.h - 1, GOLD)
        rows(face, 0, 0, INDIGO_H)
    skin.face("skirt", "up").fill(INDIGO_D)
    skin.face("skirt", "down").fill(INDIGO_D)


def paint_arms(skin):
    for arm, slv, seed in (("rightArm", "rightSleeve", 900), ("leftArm", "leftSleeve", 910)):
        for f in SIDES + ("up", "down"):
            face = skin.face(arm, f)
            skin_tone(face, SKIN, seed + len(f))
            # cream opera gloves past the elbow, gold band at the top
            glove = face.row >= 12
            face.fill(CREAM, glove)
            face.shade(noise((face.h, face.w), seed + 5, 0.03), glove)
            rows(face, 12, 12, GOLD)
            rows(face, 0, 3, INDIGO)
        skin.face(arm, "down").fill(CREAM)
        skin.face(arm, "up").fill(INDIGO)
        for face in skin.each(slv):
            face.clear()
        # little puffed sleeve caps
        for f in SIDES:
            face = skin.face(slv, f)
            dress(face, seed + 20 + len(f))
            face.clear(face.row >= 5)
            rows(face, 4, 4, GOLD)
        up = skin.face(slv, "up")
        dress(up, seed + 30)


def paint_legs(skin, boot_h):
    for leg, pants, seed in (("rightLeg", "rightPants", 1000), ("leftLeg", "leftPants", 1010)):
        for f in SIDES:
            face = skin.face(leg, f)
            skin_tone(face, SKIN, seed + len(f))
            # tall cream boot shafts up past the knee
            shaft = face.row >= 8
            gradient(face, [(0, CREAM), (1, (232, 214, 172))], mask=shaft)
            rows(face, 8, 8, GOLD)
            rows(face, 9, 9, GOLD_D)
            if f == "north":
                face.fill(GOLD, (face.row >= 11) & (face.row % 3 == 2) & (face.col >= 3) & (face.col <= 4))
        skin.face(leg, "up").fill(INDIGO_D)
        skin.face(leg, "down").fill(CREAM)
        for face in skin.each(pants):
            face.clear()
    clear_under_shoes(skin, boot_h)


def paint_boots(skin):
    for side in ("right", "left"):
        shoe = f"{side}Shoe"
        for face in skin.each(shoe):
            gradient(face, [(0, CREAM), (1, (226, 206, 160))])
            face.shade(noise((face.h, face.w), 1100 + face.w, 0.03))
        for f in SIDES:
            face = skin.face(shoe, f)
            rows(face, face.h - 3, face.h - 3, GOLD)
            rows(face, face.h - 2, face.h - 1, INDIGO)
            rows(face, face.h - 1, face.h - 1, INDIGO_D)
        toe = skin.face(shoe, "north")
        toe.stamp(["GGG"], {"G": GOLD}, top=1, left=toe.w // 2 - 1)
        skin.face(shoe, "down").fill(INDIGO_D)
