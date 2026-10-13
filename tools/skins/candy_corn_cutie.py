"""Candy Corn Cutie: candy-corn hood over long brown hair, orange overalls
with a pumpkin pocket, puffy striped sleeves and mismatched socks/sneakers.
"""

import numpy as np

from paintkit import (SIDES, add_footwear, box, clear_under_shoes, cloth,
                      copy_layer, hair, paint_sneakers, rows, skin_tone)
from skinlib import Skin, add_standard_body, noise

ID = "geometry.MidnightMischief.CandyCornCutie"
TEXTURE = "candy_corn_cutie.png"
NAME = "Candy Corn Cutie"
LOC = "CandyCornCutie"
REF_BOX = (790, 520, 1040, 1000)  # crop of reference/midnight_mischief_lineup.webp
DETAILS = [
    ("face", "Candy-corn hood + 3D hair", {"yaw": 22, "pitch": 8, "dist": 44, "target": 25, "fov": 30}),
    ("back34", "Hood drape + overall straps", {"yaw": 205, "pitch": 12}),
    ("shoes", "Mismatched socks + sneakers", {"yaw": 25, "pitch": 12, "dist": 52, "target": 7, "fov": 30}),
]

SKIN = (222, 168, 128)
SKIN_D = (198, 144, 106)
SKIN_H = (236, 186, 148)
HAIR = (102, 58, 34)
HAIR_D = (72, 38, 22)
HAIR_L = (132, 80, 48)
HAIR_S = (160, 104, 64)
CC_W = (248, 240, 226)
CC_W_D = (226, 214, 198)
CC_O = (242, 126, 30)
CC_O_D = (214, 100, 18)
CC_Y = (252, 194, 46)
CC_Y_D = (230, 164, 30)
SHIRT = (246, 238, 224)
SHIRT_D = (224, 212, 196)
OV = (238, 116, 30)
OV_D = (208, 92, 20)
OV_H = (252, 146, 56)
POCKET = (252, 202, 64)
BROWN = (96, 52, 28)
LILAC = (204, 156, 222)
BLACK = (40, 34, 46)

SHOE_R = {"upper": (246, 238, 224), "hi": (255, 252, 244), "dark": (252, 196, 60),
          "lace": CC_O, "lace_dark": CC_O_D, "sole": (250, 244, 232), "sole_dark": (220, 208, 192)}
SHOE_L = {"upper": (44, 38, 50), "hi": (70, 62, 78), "dark": (28, 24, 32),
          "lace": CC_O, "lace_dark": CC_O_D, "sole": (246, 238, 226), "sole_dark": (214, 202, 188)}


def build():
    skin = Skin(ID, slim=True)
    add_standard_body(skin)
    skin.acc("lockRight", "body", [-4.25, 16, -3.25], [1.5, 8, 1], faces=("north", "east", "west", "down"))
    skin.acc("lockLeft", "body", [2.75, 16.5, -3.25], [1.5, 7.5, 1], faces=("north", "east", "west", "down"))
    skin.acc("hoodDrape", "body", [-3.5, 20.5, 2.25], [7, 3.5, 1], faces=("south", "east", "west", "down"))
    skin.acc("rightCuff", "rightArm", [-7, 13.5, -2], [3, 2, 4], inflate=0.55, lowres=("up", "down"))
    skin.acc("leftCuff", "leftArm", [4, 13.5, -2], [3, 2, 4], inflate=0.55, lowres=("up", "down"))
    h = add_footwear(skin, height=3.0)
    paint_head(skin)
    paint_body(skin)
    paint_arms(skin)
    paint_legs(skin, h)
    paint_sneakers(skin, SHOE_R, 1900, pal_left=SHOE_L)
    return skin


BANGS = [15, 15, 6, 4, 3, 3, 4, 3, 3, 4, 3, 3, 4, 6, 15, 15]


def candy_bands(face, seed, top_row=0):
    """Cream tip, orange middle, yellow base, like a candy corn."""
    face.fill(CC_W)
    rows(face, top_row + 5, top_row + 9, CC_O)
    rows(face, top_row + 10, 99, CC_Y)
    face.shade(noise((face.h, face.w), seed, 0.04))
    rows(face, top_row + 5, top_row + 5, CC_O_D)
    rows(face, top_row + 10, top_row + 10, CC_Y_D)


def paint_head(skin):
    front = skin.face("head", "north")
    skin_tone(front, SKIN, 1800)
    hm = front.row <= np.array(BANGS)[front.col]
    hair(front, HAIR, HAIR_D, HAIR_L, 1801, mask=hm, shine=HAIR_S)
    front.shade(np.where((front.row == np.array(BANGS)[front.col] + 1) & ~hm, 0.88, 1.0))
    eye = ["EEE", "BhB", "BBB"]
    pal = {"E": (40, 22, 16), "B": (84, 44, 24), "h": (255, 250, 240)}
    front.stamp(eye, pal, top=7, left=3)
    front.stamp(eye, pal, top=7, left=10, mirror=True)
    front.set(7, 2, (40, 22, 16))
    front.set(7, 13, (40, 22, 16))
    front.set(10, 7, SKIN_D)
    front.stamp(["mWWm", ".pp."], {"m": (110, 44, 40), "W": (255, 255, 255), "p": (226, 112, 120)},
                top=12, left=6)
    for c in (3, 4, 11, 12):
        front.set(11, c, (238, 142, 132))
    for f in ("east", "west", "south", "up"):
        hair(skin.face("head", f), HAIR, HAIR_D, HAIR_L, 1810 + len(f), shine=HAIR_S)
    skin_tone(skin.face("head", "down"), SKIN_D, 1820)

    # hat layer is the hood: candy-corn bands with a yellow rim round the face
    for f in ("east", "west", "south"):
        candy_bands(skin.face("hat", f), 1830 + len(f))
    top = skin.face("hat", "up")
    top.fill(CC_W)
    top.shade(noise((16, 16), 1840, 0.04))
    hood = skin.face("hat", "north")
    candy_bands(hood, 1841)
    rim = (hood.row <= 1) | (hood.col <= 1) | (hood.col >= 14)
    hood.fill(CC_Y, rim & (hood.row >= 2))
    hood.fill(CC_Y_D, rim & (hood.row >= 2) & ((hood.col == 1) | (hood.col == 14)))
    hood.fill(CC_O, (hood.row == 1))
    hood.clear(~rim)
    # hood edges hang a little lower at the sides
    skin.face("hat", "down").clear()


def overalls(face, seed, mask=None):
    cloth(face, OV, seed, var=0.05, fold=0.05, freq=0.9, mask=mask)


def paint_body(skin):
    front = skin.face("body", "north")
    cloth(front, SHIRT, 1850, var=0.03, fold=0.03)
    bib = box(front, 4, 3, 23, 12) | (front.row >= 15)
    straps = box(front, 0, 3, 3, 4) | box(front, 0, 11, 3, 12)
    overalls(front, 1851, mask=bib | straps)
    front.fill(OV_H, box(front, 4, 3, 4, 12))
    front.set(4, 3, POCKET)
    front.set(4, 12, POCKET)
    pocket = box(front, 7, 5, 11, 10)
    front.fill(POCKET, pocket)
    front.fill((230, 170, 40), pocket & ((front.row == 11) | (front.col == 10)))
    front.set(6, 7, (90, 130, 40))
    front.set(6, 8, (90, 130, 40))
    for r, c in ((8, 6), (8, 9), (10, 7), (10, 8)):
        front.set(r, c, BROWN)
    front.fill(OV_D, (front.row == 15) & ~box(front, 15, 3, 15, 12))
    front.fill(OV_D, (front.col == 7) & (front.row >= 16))
    for f in ("east", "west"):
        face = skin.face("body", f)
        cloth(face, SHIRT, 1860 + len(f), var=0.03, fold=0.03)
        lower = face.row >= 15
        face.fill(OV, lower)
        face.shade(np.where(lower, noise((24, 8), 1864, 0.05), 1.0))
        face.fill(OV_D, face.row == 15)
    back = skin.face("body", "south")
    cloth(back, SHIRT, 1870, var=0.03, fold=0.03)
    for r in range(0, 15):
        for c in (r // 2 + 3, 12 - r // 2):
            back.set(r, c, OV)
            back.set(r, c + 1 if c < 8 else c - 1, OV_D)
    lower = back.row >= 15
    back.fill(OV, lower)
    back.shade(np.where(lower, noise((24, 16), 1871, 0.05), 1.0))
    back.fill(OV_D, back.row == 15)
    back.fill(OV_H, box(back, 17, 3, 19, 6) | box(back, 17, 9, 19, 12))     # back pockets
    cloth(skin.face("body", "up"), SHIRT, 1872, var=0.03)
    overalls(skin.face("body", "down"), 1873)
    for face in skin.each("jacket"):
        face.clear()

    for name in ("lockRight", "lockLeft"):
        for face in skin.each(name):
            hair(face, HAIR, HAIR_D, HAIR_L, 1880 + face.w, shine=HAIR_S)
        f = skin.face(name, "north")
        f.clear((f.row == f.h - 1) & (f.col == (0 if name == "lockRight" else f.w - 1)))
    for face in skin.each("hoodDrape"):
        face.fill(CC_Y)
        face.shade(noise((face.h, face.w), 1890 + face.w, 0.04))
    drape = skin.face("hoodDrape", "south")
    rows(drape, 0, 1, CC_O)
    rows(drape, drape.h - 1, drape.h - 1, CC_Y_D)
    drape.clear((drape.row == drape.h - 1) & ((drape.col == 0) | (drape.col == drape.w - 1)))


def paint_arms(skin):
    for arm, slv, cuff, seed in (("rightArm", "rightSleeve", "rightCuff", 1900),
                                 ("leftArm", "leftSleeve", "leftCuff", 1910)):
        for f in SIDES:
            face = skin.face(arm, f)
            cloth(face, CC_W, seed + len(f), var=0.03, fold=0.04)
            rows(face, 7, 8, CC_O)
            rows(face, 9, 10, CC_Y)
            rows(face, 7, 7, CC_O_D)
            hand = face.row >= 19
            face.fill(SKIN, hand)
            face.shade(np.where(hand, noise((24, face.w), seed + 3, 0.03), 1.0))
            face.shade(np.where(face.row == 19, 0.86, 1.0))
        cloth(skin.face(arm, "up"), CC_W, seed + 7, var=0.03)
        skin_tone(skin.face(arm, "down"), SKIN_D, seed + 8)
        copy_layer(skin, arm, slv)
        for f in SIDES:
            skin.face(slv, f).clear(skin.face(slv, f).row >= 15)
        skin.face(slv, "down").clear()
        for f in SIDES:
            face = skin.face(cuff, f)
            face.fill(CC_W)
            face.shade(noise((face.h, face.w), seed + 11 + len(f), 0.04))
            rows(face, face.h - 1, face.h - 1, CC_Y)
            face.fill(CC_W_D, (face.row == 1) & (face.col % 3 == 0))
        skin.face(cuff, "up").fill(CC_W)
        b = skin.face(cuff, "down")
        b.fill(CC_Y_D)
        b.clear(box(b, 1, 1, b.h - 2, b.w - 2))


def paint_legs(skin, shoe_h):
    for leg, pants, seed, stripes in (
            ("rightLeg", "rightPants", 2000, [CC_W, CC_O, CC_W, CC_Y]),
            ("leftLeg", "leftPants", 2010, [BLACK, LILAC])):
        for f in SIDES:
            face = skin.face(leg, f)
            overalls(face, seed + len(f))
            rows(face, 6, 7, CC_Y)
            for r in range(8, 24):
                rows(face, r, r, stripes[((r - 8) // 2) % len(stripes)])
            sock = face.row >= 8
            face.shade(np.where(sock, noise((24, 8), seed + 5 + len(f), 0.04), 1.0))
        skin.face(leg, "up").fill(OV_D)
        skin.face(leg, "down").fill(stripes[0])
        # puffy shorts hem on the overlay
        for f in SIDES:
            face = skin.face(pants, f)
            overalls(face, seed + 20 + len(f))
            rows(face, 6, 7, CC_Y)
            rows(face, 7, 7, CC_Y_D)
            face.clear(face.row > 7)
        skin.face(pants, "up").clear()
        skin.face(pants, "down").clear()
    clear_under_shoes(skin, shoe_h)
