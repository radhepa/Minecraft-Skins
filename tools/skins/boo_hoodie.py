"""Boo Hoodie: a sheet-ghost face in an oversized mint hoodie with a dripping
ghost print, rolled teal pants and mint sneakers.
"""

import numpy as np

from paintkit import (SIDES, add_footwear, box, clear_under_shoes, cloth,
                      copy_layer, paint_sneakers, rows)
from skinlib import Skin, add_standard_body, noise

ID = "geometry.MidnightMischief.BooHoodie"
TEXTURE = "boo_hoodie.png"
NAME = "Boo Hoodie"
LOC = "BooHoodie"
REF_BOX = (780, 90, 1010, 540)  # crop of reference/midnight_mischief_lineup.webp
DETAILS = [
    ("face", "Ghost sheet face", {"yaw": 22, "pitch": 8, "dist": 42, "target": 26, "fov": 30}),
    ("back34", "3D bunched hood", {"yaw": 200, "pitch": 18}),
    ("shoes", "Bulky cuffs + mint sneakers", {"yaw": 35, "pitch": 14, "dist": 50, "target": 8, "fov": 30}),
]

CREAM = (240, 228, 210)
CREAM_D = (220, 204, 186)
CREAM_H = (252, 244, 232)
EYE = (30, 26, 32)
EYE_H = (74, 68, 80)
MINT = (156, 204, 170)
MINT_D = (124, 174, 142)
MINT_H = (186, 226, 194)
MINT_X = (98, 148, 120)
TEAL = (50, 84, 88)
TEAL_D = (36, 64, 68)
TEAL_H = (70, 106, 108)
HAND = (236, 208, 186)
HAND_D = (214, 184, 162)

SNEAKERS = {"upper": (170, 212, 182), "hi": (198, 232, 204), "dark": (122, 170, 140),
            "lace": (246, 236, 220), "lace_dark": (216, 204, 188),
            "sole": (242, 230, 212), "sole_dark": (212, 198, 180)}


def build():
    skin = Skin(ID)
    add_standard_body(skin)
    skin.acc("hood", "body", [-4, 21, 2], [8, 3, 2.5], faces=("south", "east", "west", "up", "down"))
    skin.acc("rightCuff", "rightArm", [-8, 13.5, -2], [4, 2, 4], inflate=0.5)
    skin.acc("leftCuff", "leftArm", [4, 13.5, -2], [4, 2, 4], inflate=0.5)
    h = add_footwear(skin, height=3.0)
    paint_head(skin)
    paint_body(skin)
    paint_arms(skin)
    paint_legs(skin, h)
    paint_sneakers(skin, SNEAKERS, 700)
    return skin


def sheet(face, seed):
    face.fill(CREAM)
    face.shade(noise((face.h, face.w), seed, 0.025))
    # soft fabric folds falling down the sheet
    face.shade(1 - 0.05 * (np.sin(face.col * 0.9 + seed) > 0.6))


def paint_head(skin):
    for f in SIDES + ("up",):
        sheet(skin.face("head", f), 600 + len(f))
    front = skin.face("head", "north")
    eye = [
        ".EE.",
        "EhEE",
        "EEEE",
        "EEEE",
        "EEEE",
        ".EE.",
    ]
    front.stamp(eye, {"E": EYE, "h": EYE_H}, top=5, left=2)
    front.stamp(eye, {"E": EYE, "h": EYE_H}, top=5, left=10)
    # a faint shadow under the eyes, cloth stretched over the face
    for c in (3, 4, 11, 12):
        front.set(11, c, CREAM_D)
    rows(front, 0, 0, CREAM_H)
    skin.face("head", "down").fill(CREAM_D)

    # hat layer: the hood drapes round the back and the lower sides
    for f in SIDES + ("up", "down"):
        skin.face("hat", f).clear()
    back = skin.face("hat", "south")
    cloth(back, MINT, 610, var=0.05, fold=0.06)
    back.clear(back.row < 6)
    back.fill(MINT_H, back.row == 6)
    for f, back_first in (("east", True), ("west", False)):
        side = skin.face("hat", f)
        cloth(side, MINT, 620 + len(f), var=0.05, fold=0.06)
        k = side.col if back_first else 15 - side.col   # distance from the back
        drape = side.row >= 6 + k * 1.1
        side.clear(~drape)
        side.fill(MINT_H, drape & (side.row == np.ceil(6 + k * 1.1)))


def drip_mask(face):
    """Cream ghost drip across the chest (front of the hoodie)."""
    top = 9 + (np.sin(face.col * 1.3) > 0.3)
    bottom = np.array([14, 16, 13, 15, 17, 14, 13, 16, 15, 13, 14, 17, 15, 13, 16, 14])
    return (face.row >= top) & (face.row <= bottom[face.col])


def paint_body(skin):
    front = skin.face("body", "north")
    cloth(front, MINT, 630, var=0.05)
    m = drip_mask(front)
    front.fill(CREAM, m)
    front.shade(np.where(m, noise((24, 16), 631, 0.03), 1.0))
    edge = m & ~np.roll(m, -1, axis=0)
    front.fill(CREAM_D, edge)
    for c in (5, 10):
        rows(front, 0, 6, CREAM, front.col == c)
        front.set(7, c, CREAM_D)
    rows(front, 0, 0, MINT_X, (front.col >= 4) & (front.col <= 11))
    rows(front, 22, 23, MINT_D)
    front.fill(MINT_X, (front.row == 23) & (front.col % 2 == 0))
    for f in ("south", "east", "west"):
        face = skin.face("body", f)
        cloth(face, MINT, 640 + len(f), var=0.05)
        rows(face, 22, 23, MINT_D)
        face.fill(MINT_X, (face.row == 23) & (face.col % 2 == 0))
    back = skin.face("body", "south")
    # little ghost on the back
    ghost = [".CCC.", "CECEC", "CCCCC", "CCCCC", "C.C.C"]
    back.stamp(ghost, {"C": CREAM, "E": EYE}, top=9, left=6)
    cloth(skin.face("body", "up"), MINT_D, 645)
    cloth(skin.face("body", "down"), MINT_D, 646)
    copy_layer(skin, "body", "jacket")
    skin.face("jacket", "up").clear()


def paint_arms(skin):
    for arm, slv, cuff, seed in (("rightArm", "rightSleeve", "rightCuff", 650),
                                 ("leftArm", "leftSleeve", "leftCuff", 660)):
        for f in SIDES:
            face = skin.face(arm, f)
            cloth(face, MINT, seed + len(f), var=0.05)
            rows(face, 18, 20, MINT_D)
            face.fill(MINT_X, (face.row >= 18) & (face.row <= 20) & (face.col % 2 == 0))
            hand = face.row >= 21
            face.fill(HAND, hand)
            face.shade(np.where(face.row == 21, 0.88, 1.0))
        cloth(skin.face(arm, "up"), MINT, seed + 7)
        skin.face(arm, "down").fill(HAND_D)
        copy_layer(skin, arm, slv)
        for f in SIDES:
            skin.face(slv, f).clear(skin.face(slv, f).row >= 18)
        skin.face(slv, "down").clear()
        for f in SIDES:
            face = skin.face(cuff, f)
            face.fill(MINT_D)
            face.fill(MINT_X, face.col % 2 == 0)
            rows(face, 0, 0, MINT_H)
        cloth(skin.face(cuff, "up"), MINT, seed + 8)
        b = skin.face(cuff, "down")
        b.fill(MINT_X)
        b.clear(box(b, 1, 1, b.h - 2, b.w - 2))


def paint_legs(skin, shoe_h):
    for leg, pants, seed in (("rightLeg", "rightPants", 670), ("leftLeg", "leftPants", 680)):
        for f in SIDES:
            face = skin.face(leg, f)
            cloth(face, TEAL, seed + len(f), var=0.08, fold=0.08, freq=0.8)
            face.fill(TEAL_H, (face.row % 7 == 3) & (face.col % 3 == 1))
            rows(face, 17, 17, TEAL_D)
        skin.face(leg, "up").fill(TEAL_D)
        skin.face(leg, "down").fill(TEAL_D)
        # rolled cuff stands out on the overlay layer
        for f in SIDES:
            face = skin.face(pants, f)
            cloth(face, TEAL_H, seed + 20 + len(f), var=0.05, fold=0.0)
            rows(face, 13, 13, (86, 124, 124))
            rows(face, 16, 16, TEAL_D)
            face.clear((face.row < 13) | (face.row > 16))
        skin.face(pants, "up").clear()
    clear_under_shoes(skin, shoe_h)
