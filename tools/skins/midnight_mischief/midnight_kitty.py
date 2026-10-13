"""Midnight Kitty: black cat with glowing amber eyes and pink-lined ears,
dark purple moon hoodie, puffy lilac cuffs, cargo pants and pink sneakers.
"""

import numpy as np

from paintkit import (SIDES, add_footwear, box, clear_under_shoes, cloth,
                      copy_layer, paint_sneakers, rows)
from skinlib import Skin, add_standard_body, noise

ID = "geometry.MidnightMischief.MidnightKitty"
TEXTURE = "midnight_kitty.png"
NAME = "Midnight Kitty"
LOC = "MidnightKitty"
REF_BOX = (500, 520, 730, 1000)  # crop of reference/midnight_mischief_lineup.webp
DETAILS = [
    ("face", "3D cat ears + amber eyes", {"yaw": 20, "pitch": 10, "dist": 44, "target": 27, "fov": 30}),
    ("back34", "Curled 3D tail", {"yaw": 140, "pitch": 8}),
    ("shoes", "Cargo pockets + pink sneakers", {"yaw": 50, "pitch": 12, "dist": 52, "target": 8, "fov": 30}),
]

FUR = (38, 28, 46)
FUR_D = (24, 18, 30)
FUR_H = (58, 44, 68)
BLUSH = (150, 82, 170)
BLUSH_H = (186, 116, 204)
EAR_IN = (238, 150, 196)
HOOD = (60, 38, 88)
HOOD_D = (44, 28, 68)
HOOD_H = (80, 52, 112)
STRING = (198, 142, 224)
GOLD = (244, 172, 52)
CUFF = (216, 148, 224)
CUFF_D = (186, 118, 198)
CUFF_H = (236, 180, 240)
PANTS = (112, 64, 154)
PANTS_D = (88, 48, 126)
PANTS_H = (138, 86, 178)

SNEAKERS = {"upper": (238, 152, 206), "hi": (252, 186, 226), "dark": (206, 112, 172),
            "lace": (250, 238, 228), "lace_dark": (220, 204, 196),
            "sole": (246, 232, 218), "sole_dark": (214, 198, 186)}


def build():
    skin = Skin(ID)
    add_standard_body(skin)
    for side, sx in (("Right", -1), ("Left", 1)):
        x_base = -4 if sx < 0 else 1
        x_tip = -4 if sx < 0 else 2.5
        skin.acc(f"ear{side}", "head", [x_base, 32.25, -2], [3, 2, 1.5], lowres=("up", "down"))
        skin.acc(f"earTip{side}", "head", [x_tip, 34.25, -1.75], [1.5, 1, 1], px=2)
    skin.acc("tailBase", "body", [-0.75, 13, 2.25], [1.5, 1.5, 3], lowres=("up", "down"))
    skin.acc("tailUp", "body", [-0.75, 14.5, 3.75], [1.5, 5, 1.5], lowres=("up", "down"))
    skin.acc("tailTip", "body", [-0.75, 19.5, 3.75], [1.5, 1.5, 1.5])
    for side, x in (("Right", -4.65), ("Left", 4.15)):
        skin.acc(f"pocket{side}", f"{side.lower()}Leg", [x, 5, -1], [0.5, 2.5, 2], px=2)
    skin.acc("rightCuff", "rightArm", [-8, 13.5, -2], [4, 2, 4], inflate=0.6, lowres=("up", "down"))
    skin.acc("leftCuff", "leftArm", [4, 13.5, -2], [4, 2, 4], inflate=0.6, lowres=("up", "down"))
    h = add_footwear(skin, height=3.0)
    paint_head(skin)
    paint_extras(skin)
    paint_body(skin)
    paint_arms(skin)
    paint_legs(skin, h)
    paint_sneakers(skin, SNEAKERS, 1500)
    return skin


def fur(face, seed, base=FUR):
    face.fill(base)
    face.shade(noise((face.h, face.w), seed, 0.08))
    face.fill(FUR_H, (noise((face.h, face.w), seed + 1, 1.0) > 1.82))


def paint_head(skin):
    for f in SIDES + ("up", "down"):
        fur(skin.face("head", f), 1400 + len(f))
    front = skin.face("head", "north")
    eye = [
        ".AA.",
        "AWPO",
        "AOPO",
        "AYPY",
        ".YY.",
    ]
    pal = {"A": (214, 116, 10), "O": (250, 160, 28), "Y": (255, 204, 72),
           "P": (30, 16, 10), "W": (255, 250, 230)}
    front.stamp(eye, pal, top=6, left=2)
    front.stamp(eye, pal, top=6, left=10, mirror=True)
    nose = (236, 122, 172)
    for r, c in ((11, 7), (11, 8)):
        front.set(r, c, nose)
    for r, c in ((12, 7), (12, 8), (13, 6), (13, 9)):
        front.set(r, c, (120, 50, 96))
    for c in (1, 2, 13, 14):
        front.set(11, c, (226, 140, 210))

    # hat layer: fluffy fur cap and purple cheek tufts
    for f in SIDES + ("up", "down"):
        fur(skin.face("hat", f), 1410 + len(f), FUR_H)
    skin.face("hat", "down").clear()
    hat = skin.face("hat", "north")
    hat.clear()
    for f, front_first in (("east", False), ("west", True)):
        side = skin.face("hat", f)
        k = side.col if front_first else 15 - side.col           # 0 at the front
        cheek = (side.row >= 10) & (side.row <= 14) & (k <= 4)
        side.fill(BLUSH, cheek)
        side.fill(BLUSH_H, cheek & (side.row == 9))
        side.clear(~cheek & (side.row >= 8) & (k <= 8))
        side.clear((side.row >= 14) & (side.col % 2 == 0))
    back = skin.face("hat", "south")
    back.clear((back.row >= 14) & (back.col % 2 == 1))


def paint_extras(skin):
    for side in ("Right", "Left"):
        for name in (f"ear{side}", f"earTip{side}"):
            for face in skin.each(name):
                fur(face, 1420 + face.w)
        front = skin.face(f"ear{side}", "north")
        # stepped triangle of pink, peaking under the tip on the outer side
        tip_col = 1 if side == "Right" else front.w - 2
        dist = abs(front.col - tip_col)
        inner = (front.row >= 1) & (dist <= front.row - 1) & (front.col >= 1) & (front.col <= front.w - 2)
        front.fill(EAR_IN, inner)
        tip = skin.face(f"earTip{side}", "north")
        tip.fill(EAR_IN, (tip.row == tip.h - 1) & (tip.col == tip.w // 2))
        pocket = f"pocket{side}"
        for face in skin.each(pocket):
            cloth(face, PANTS_H, 1430, var=0.05, fold=0.0)
        outer = skin.face(pocket, "east" if side == "Right" else "west")
        rows(outer, 0, 1, PANTS)
        rows(outer, 2, 2, PANTS_D)
        outer.set(3, outer.w // 2, (230, 200, 250))
    for name in ("tailBase", "tailUp", "tailTip"):
        for face in skin.each(name):
            fur(face, 1440 + face.w)
    for face in skin.each("tailTip"):
        face.fill(BLUSH)
        face.shade(noise((face.h, face.w), 1450, 0.06))


def paint_body(skin):
    front = skin.face("body", "north")
    cloth(front, HOOD, 1460, var=0.06)
    for c in (5, 10):
        rows(front, 1, 6, STRING, front.col == c)
        front.set(7, c, (236, 200, 246))
    rows(front, 0, 0, HOOD_D, (front.col >= 4) & (front.col <= 11))
    moon = [".GG", "G..", "G..", ".GG"]
    front.stamp(moon, {"G": GOLD}, top=8, left=6)
    front.set(8, 8, (210, 140, 30))
    pocket = box(front, 14, 3, 19, 12)
    front.fill(HOOD_H, pocket)
    front.fill((104, 68, 144), pocket & ((front.row == 14) | (front.col == 3) | (front.col == 12)))
    front.fill(HOOD_D, box(front, 15, 4, 19, 4) | box(front, 15, 11, 19, 11))
    rows(front, 22, 23, HOOD_D)
    front.fill(HOOD, (front.row >= 22) & (front.col % 2 == 0))
    for f in ("east", "west", "south"):
        face = skin.face("body", f)
        cloth(face, HOOD, 1470 + len(f), var=0.06)
        rows(face, 22, 23, HOOD_D)
        face.fill(HOOD, (face.row >= 22) & (face.col % 2 == 0))
    back = skin.face("body", "south")
    hood = box(back, 0, 3, 6, 12) & ~((back.row == 6) & ((back.col == 3) | (back.col == 12)))
    back.fill(HOOD_H, hood)
    back.fill(HOOD_D, hood & (back.row == 6))
    cloth(skin.face("body", "up"), HOOD_D, 1480)
    cloth(skin.face("body", "down"), HOOD_D, 1481)
    copy_layer(skin, "body", "jacket")
    skin.face("jacket", "up").clear()


def paint_arms(skin):
    for arm, slv, cuff, seed in (("rightArm", "rightSleeve", "rightCuff", 1500),
                                 ("leftArm", "leftSleeve", "leftCuff", 1510)):
        for f in SIDES:
            face = skin.face(arm, f)
            cloth(face, HOOD, seed + len(f), var=0.06)
            rows(face, 17, 20, CUFF)
            paw = face.row >= 21
            face.fill(FUR, paw)
            face.shade(np.where(paw, noise((24, 8), seed + 5, 0.08), 1.0))
        cloth(skin.face(arm, "up"), HOOD, seed + 7)
        paw = skin.face(arm, "down")
        paw.fill(FUR)
        for r, c in ((5, 3), (5, 4), (6, 3), (6, 4), (2, 1), (2, 3), (2, 5)):
            paw.set(r, c, EAR_IN)
        copy_layer(skin, arm, slv)
        for f in SIDES:
            skin.face(slv, f).clear(skin.face(slv, f).row >= 17)
        skin.face(slv, "down").clear()
        for f in SIDES:
            face = skin.face(cuff, f)
            face.fill(CUFF)
            face.shade(noise((face.h, face.w), seed + 9 + len(f), 0.06))
            rows(face, 0, 0, CUFF_H)
            rows(face, face.h - 1, face.h - 1, CUFF_D)
            face.fill(CUFF_H, (face.row == 1) & (face.col % 3 == 0))
        skin.face(cuff, "up").fill(CUFF_H)
        b = skin.face(cuff, "down")
        b.fill(CUFF_D)
        b.clear(box(b, 1, 1, b.h - 2, b.w - 2))


def paint_legs(skin, shoe_h):
    for leg, pants, seed in (("rightLeg", "rightPants", 1600), ("leftLeg", "leftPants", 1610)):
        for f in SIDES:
            face = skin.face(leg, f)
            cloth(face, PANTS, seed + len(f), var=0.07, fold=0.08, freq=0.8)
            face.fill(PANTS_D, face.col == (4 if f in ("east", "west") else 0))
            rows(face, 16, 17, PANTS_D)
        skin.face(leg, "up").fill(PANTS_D)
        skin.face(leg, "down").fill(PANTS_D)
        for face in skin.each(pants):
            face.clear()
        # slouchy hem bunching over the shoes
        for f in SIDES:
            face = skin.face(pants, f)
            cloth(face, PANTS_H, seed + 20 + len(f), var=0.05, fold=0.0, mask=(face.row >= 15) & (face.row <= 17))
            face.fill(PANTS_D, (face.row == 17) & (face.col % 3 == 0))
    clear_under_shoes(skin, shoe_h)
