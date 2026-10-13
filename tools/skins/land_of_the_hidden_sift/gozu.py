"""Gozu the Carapace Brute: the Soul-Infused muscle, armoured in shell torn
from the Carapace. Ash-grey skin, glowing amber eyes under a heavy scowl, a
scar across one eye, a horned chitin helmet, chitin pauldrons, chest plate
and gauntlets veined with soul-glow, his slashed headband knotted round one
arm, dark trousers and heavy boots.
"""

import numpy as np

from paintkit import (SIDES, add_footwear, box, clear_under_shoes, cloth, gradient, paint_boots,
                      rows, skin_tone)
from skinlib import Skin, add_standard_body, noise

from .shinobi import (BAND, BAND_D, BAND_L, ETCH, SLASH, STEEL, STEEL_D, STEEL_L, hair_head,
                      hair_painter, male_face)

ID = "geometry.LandOfTheHiddenSift.Gozu"
TEXTURE = "gozu.png"
NAME = "Gozu the Carapace Brute"
LOC = "Gozu"
DETAILS = [
    ("face", "Horned chitin helmet", {"yaw": 22, "pitch": 6, "dist": 60, "target": 28, "fov": 30}),
    ("armour", "Chitin armour + gauntlets", {"yaw": -35, "pitch": 6, "dist": 80, "target": 17, "fov": 30}),
    ("arm", "Slashed headband on his arm", {"yaw": 80, "pitch": 4, "dist": 56, "target": 19, "fov": 30}),
]

SKIN = (150, 142, 152)
SKIN_D = (120, 112, 124)
SCAR = (110, 96, 108)
HAIR = (36, 30, 34)
HAIR_D = (18, 14, 18)
HAIR_L = (60, 52, 58)
BROW = (30, 24, 28)
LASH = (20, 14, 18)
EYE_D = (190, 92, 18)
EYE = (255, 160, 40)
EYE_L = (255, 222, 130)
MOUTH = (96, 74, 84)
CHITIN = (136, 56, 40)
CHITIN_D = (68, 24, 20)
CHITIN_L = (204, 116, 78)
SHEEN = (244, 182, 136)
SOUL = (80, 236, 214)
SOUL_D = (30, 150, 150)
HORN = (232, 214, 184)
HORN_D = (170, 146, 112)
PANTS = (40, 34, 40)
BOOTS = {"upper": (58, 44, 40), "hi": (84, 64, 56), "dark": (38, 28, 26), "strap": CHITIN,
         "strap_dark": CHITIN_D, "sole": (30, 24, 24), "sole_dark": (18, 14, 14)}


def build():
    skin = Skin(ID)
    add_standard_body(skin)
    # horns: a base and a curved-up tip on each side of the helmet
    for side, x, s in (("R", -4.6, -1), ("L", 4.6, 1)):
        kw = dict(like="hornR") if side == "L" else dict(lowres=("up", "down"))
        kwt = dict(like="hornTipR") if side == "L" else dict(lowres=("down",))
        skin.acc(f"horn{side}", "head", [x - 1.0 if s > 0 else x - 1.5, 29.5, -1.0], [2.5, 1.75, 1.75],
                 rotation=[0, 0, 20 * s], pivot=[x, 30.4, -0.1], **kw)
        skin.acc(f"hornTip{side}", "head", [x + (1.0 if s > 0 else -2.25), 30.5, -0.75], [1.25, 2.5, 1.25],
                 rotation=[0, 0, -25 * s], pivot=[x + 1.6 * s, 30.8, -0.1], **kwt)
    # chitin armour
    skin.acc("chest", "body", [-4.0, 15.5, -2.85], [8, 7.5, 0.75], lowres=("up", "down", "east", "west"))
    skin.acc("pauldronR", "rightArm", [-9.0, 21.0, -2.75], [5.25, 3.5, 5.5], rotation=[0, 0, 12],
             pivot=[-6.0, 23.0, 0], lowres=("down",))
    skin.acc("pauldronL", "leftArm", [3.75, 21.0, -2.75], [5.25, 3.5, 5.5], like="pauldronR",
             rotation=[0, 0, -12], pivot=[6.0, 23.0, 0])
    skin.acc("gauntR", "rightArm", [-8.5, 11.75, -2.5], [5, 5, 5], lowres=("up", "down", "south", "west"))
    skin.acc("gauntL", "leftArm", [3.5, 11.75, -2.5], [5, 5, 5], like="gauntR")
    h = add_footwear(skin, height=3.5, length=6.0, toe=1.5, tongue=False, width=4.75)
    paint_head(skin)
    paint_armour(skin)
    paint_body(skin)
    paint_arms(skin)
    paint_legs(skin, h)
    paint_boots(skin, BOOTS, 16900, straps=(1,))
    return skin


def chitin(face, seed, plates=True):
    """Glossy beetle shell: dark at the edges, a broad sheen across it and
    a seam between plates every few rows."""
    gradient(face, [(0, CHITIN_L), (0.4, CHITIN), (1, CHITIN_D)])
    face.shade(noise((face.h, face.w), seed, 0.02))
    diag = (face.col - face.row * 0.8) % max(face.w, 6)
    face.fill(SHEEN, (diag >= 1) & (diag < 2) & (face.row < face.h * 0.6))
    if plates and face.h >= 6:
        seam = face.row % 6 == 5
        face.fill(CHITIN_D, seam)
        face.fill(CHITIN_L, np.roll(seam, 1, axis=0) & (face.row > 0))
    face.fill(CHITIN_D, (face.col == 0) | (face.col == face.w - 1))


def soul_vein(face, cells):
    for i, (r, c) in enumerate(cells):
        face.set(r, c, SOUL if i % 3 else SOUL_D)


def paint_head(skin):
    black = hair_painter(HAIR, HAIR_D, HAIR_L)
    hair_head(skin, black, 16000, SKIN, SKIN_D, [6] * 16, back_bottom=10)
    front = skin.face("head", "north")
    male_face(front, BROW, {"L": LASH, "W": (232, 226, 220), "D": EYE_D, "E": EYE, "H": EYE_L,
                            "G": EYE_L}, MOUTH, slant=True, mouth_cols=(6, 9))
    # a scar across his left eye
    for r in range(6, 13):
        front.set(r, 12 if r % 2 else 11, SCAR)
    # heavy jaw shading
    front.shade(0.9, front.row == 15)
    # the chitin helmet: crown, brow guard and cheek plates on the hat layer
    for f in ("north", "east", "west", "south", "up"):
        face = skin.face("hat", f)
        chitin(face, 16010 + len(f), plates=f != "north")
    hf = skin.face("hat", "north")
    hf.clear(hf.row >= 7)
    hf.fill(CHITIN_D, hf.row == 6)
    hf.fill(CHITIN_L, (hf.row == 3) & (np.abs(hf.col - 7.5) < 3))
    soul_vein(hf, [(1, 7), (2, 8), (3, 8), (4, 7), (5, 7)])
    for f in ("east", "west"):
        face = skin.face("hat", f)
        face.clear((face.row >= 10) | ((face.Z < -1.0) & (face.row >= 7)))
    skin.face("hat", "south").clear(skin.face("hat", "south").row >= 11)
    for name in ("hornR", "hornTipR"):
        for face in skin.each(name):
            gradient(face, [(0, HORN), (1, HORN_D)])
            face.fill(HORN_D, face.row % 3 == 2)
    skin.face("hornTipR", "up").fill(HORN)


def paint_armour(skin):
    for face in skin.each("chest"):
        chitin(face, 16100 + face.w)
    c = skin.face("chest", "north")
    c.fill(CHITIN_D, (c.col == c.w // 2) | (c.col == c.w // 2 - 1))
    soul_vein(c, [(2, 4), (3, 5), (4, 5), (5, 6), (6, 6), (7, 5), (9, 11), (10, 10), (11, 10), (12, 11)])
    for face in skin.each("pauldronR"):
        chitin(face, 16110 + face.w)
    soul_vein(skin.face("pauldronR", "up"), [(1, 2), (2, 3), (3, 4), (4, 4), (5, 5), (6, 6)])
    for face in skin.each("gauntR"):
        chitin(face, 16120 + face.w)
        face.fill(CHITIN_D, face.row == face.h - 1)
    for f in SIDES:
        g = skin.face("gauntR", f)
        g.fill(HORN, (g.row == 1) & (g.col % 3 == 1))       # knuckle spikes


def paint_body(skin):
    for f in SIDES + ("up", "down"):
        cloth(skin.face("body", f), PANTS, 16200 + len(f), var=0.04, fold=0.05)
    for f in SIDES:
        face = skin.face("body", f)
        rows(face, 17, 19, CHITIN_D)
        rows(face, 18, 18, CHITIN)
    for face in skin.each("jacket"):
        face.clear()


def paint_arms(skin):
    for arm, slv, seed in (("rightArm", "rightSleeve", 16300), ("leftArm", "leftSleeve", 16310)):
        for f in SIDES + ("up", "down"):
            skin_tone(skin.face(arm, f), SKIN, seed + len(f), var=0.025)
        for f in SIDES:
            face = skin.face(arm, f)
            face.shade(0.92, face.col == 0)
        for face in skin.each(slv):
            face.clear()
    # the slashed headband knotted round his right bicep
    for f in SIDES:
        band = skin.face("rightSleeve", f)
        rows(band, 7, 10, BAND)
        rows(band, 7, 7, BAND_L)
        rows(band, 10, 10, BAND_D)
    out = skin.face("rightSleeve", "east")
    out.fill(STEEL, box(out, 6, 1, 11, 6))
    out.fill(STEEL_L, box(out, 6, 1, 6, 6))
    out.fill(STEEL_D, box(out, 11, 1, 11, 6))
    out.set(8, 3, ETCH)
    out.set(9, 4, ETCH)
    out.fill(SLASH, box(out, 8, 1, 8, 6))
    back = skin.face("rightSleeve", "west")
    back.fill(BAND_D, box(back, 11, 2, 14, 2) | box(back, 11, 5, 13, 5))   # knot tails


def paint_legs(skin, boot_h):
    for leg, pants, seed in (("rightLeg", "rightPants", 16400), ("leftLeg", "leftPants", 16410)):
        for f in SIDES:
            cloth(skin.face(leg, f), PANTS, seed + len(f), var=0.05, fold=0.07, freq=0.9)
        skin.face(leg, "up").fill(PANTS)
        skin.face(leg, "down").fill(PANTS)
        for face in skin.each(pants):
            face.clear()
        # chitin knee guards
        knee = skin.face(pants, "north")
        knee.fill(CHITIN, box(knee, 8, 1, 12, 6))
        knee.fill(CHITIN_L, box(knee, 8, 1, 8, 6))
        knee.fill(CHITIN_D, box(knee, 12, 1, 12, 6))
    clear_under_shoes(skin, boot_h)
