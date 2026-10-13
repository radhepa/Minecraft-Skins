"""Tobio the Scroll Runner: the fastest messenger in the village, carrying
sealed scrolls between the outposts of the Sift. Messy sandy hair, sky-blue
eyes under raised brows, a plaster across his nose and an
easy smile, the village headband, a mustard courier vest with a
hood bunched at the back over a navy shirt, a crossbody strap holding a big
message tube on his back, wrapped wrists, knee-length trousers and shin wraps.
"""

import numpy as np

from paintkit import SIDES, box, clear_under_shoes, cloth, rows
from skinlib import Skin, add_standard_body, noise

from .shinobi import (EYE_SHARP, STEEL, add_headband, add_holster, add_sandals, anime_eyes,
                      hair_head, hair_painter, paint_headband, paint_holster, paint_sandals, wraps)

ID = "geometry.LandOfTheHiddenSift.Tobio"
TEXTURE = "tobio.png"
NAME = "Tobio the Scroll Runner"
LOC = "Tobio"
DETAILS = [
    ("face", "Raised brows + nose plaster", {"yaw": 18, "pitch": 4, "dist": 46, "target": 28, "fov": 30}),
    ("tube", "Message tube + hood", {"yaw": 150, "pitch": 12, "dist": 70, "target": 20, "fov": 30}),
    ("walk", "Courier vest", {"yaw": -30, "pitch": 6}),
]

SKIN = (240, 204, 170)
SKIN_D = (214, 170, 136)
HAIR = (178, 138, 84)
HAIR_D = (122, 88, 48)
HAIR_L = (216, 180, 120)
BROW = (110, 78, 44)
LASH = (40, 28, 20)
EYE_D = (40, 88, 150)
EYE = (82, 150, 212)
EYE_L = (156, 208, 242)
WHITE = (248, 248, 246)
MOUTH = (180, 124, 104)
VEST = (214, 158, 50)
VEST_D = (160, 110, 30)
VEST_L = (240, 196, 96)
SHIRT = (40, 48, 82)
SHIRT_D = (26, 32, 58)
PANTS = (58, 62, 72)
STRAP = (84, 58, 40)
TUBE = (40, 120, 124)
TUBE_D = (24, 82, 88)
TUBE_L = (70, 164, 162)
SANDAL = (44, 50, 66)
SANDAL_D = (26, 30, 40)


def build():
    skin = Skin(ID)
    add_standard_body(skin)
    add_headband(skin, yc=30.0)
    # hood bunched at the back of the neck
    skin.acc("hood", "body", [-3.5, 21.75, 1.9], [7, 2.5, 1.6], lowres=("up", "down", "north", "east", "west"))
    # message tube slung diagonally across his back
    skin.bone("tube", "body", [0, 17.5, 3.0], rotation=[0, 0, 32])
    skin.acc("tube", "tube", [-0.9, 11.0, 2.2], [1.8, 13, 1.8], lowres=("up", "down", "north"))
    skin.acc("capTop", "tube", [-1.1, 24.0, 2.0], [2.2, 1.2, 2.2], lowres=SIDES + ("up", "down"))
    skin.acc("capBottom", "tube", [-1.1, 9.8, 2.0], [2.2, 1.2, 2.2], like="capTop")
    add_holster(skin, "right")
    h = add_sandals(skin)
    paint_head(skin)
    paint_gear(skin)
    paint_body(skin)
    paint_arms(skin)
    paint_legs(skin, h)
    paint_sandals(skin, SANDAL, SANDAL_D, SKIN, SKIN_D)
    return skin


def paint_head(skin):
    sandy = hair_painter(HAIR, HAIR_D, HAIR_L)
    # messy fringe falling in uneven points
    hair_head(skin, sandy, 12000, SKIN, SKIN_D,
              [9, 8, 7, 5, 6, 4, 5, 3, 4, 5, 3, 5, 4, 6, 7, 8], back_bottom=11)
    front = skin.face("head", "north")
    # raised brows that kick up at the outer ends
    for left, outer in ((2, 1), (10, 14)):
        for c in range(left, left + 4):
            front.set(7, c, BROW)
        front.set(6, outer, BROW)
    anime_eyes(front, 8, EYE_SHARP, {"L": LASH, "W": WHITE, "D": EYE_D, "E": EYE, "H": EYE_L,
                                     "G": EYE_L}, lefts=(2, 10))
    # a plaster across the bridge of his nose
    for c in range(5, 11):
        front.set(11, c, (226, 212, 190) if c in (5, 10) else (252, 244, 228))
    front.set(11, 7, (232, 218, 196))
    front.set(11, 8, (232, 218, 196))
    # a quick, easy smile
    for r, c in ((13, 6), (14, 7), (14, 8), (13, 9)):
        front.set(r, c, MOUTH)
    paint_headband(skin)


def paint_gear(skin):
    for face in skin.each("hood"):
        cloth(face, VEST, 12100 + face.w, var=0.04, fold=0.12, freq=1.6)
        face.fill(VEST_D, face.row == face.h - 1)
        face.fill(VEST_L, face.row == 0)
    for face in skin.each("tube"):
        face.fill(TUBE)
        face.shade(noise((face.h, face.w), 12110 + face.w, 0.03))
        face.fill(TUBE_L, face.col == 0)
        face.fill(TUBE_D, face.col == face.w - 1)
        face.fill(STRAP, (face.row % 8 == 3))
    seal = skin.face("tube", "south")
    seal.fill((200, 60, 54), box(seal, 11, 1, 13, seal.w - 2))     # wax seal band
    for face in skin.each("capTop"):
        face.fill(STEEL)
        face.fill((150, 156, 170), face.row == face.h - 1)


def paint_body(skin):
    for f in SIDES + ("up", "down"):
        cloth(skin.face("body", f), VEST, 12200 + len(f), var=0.04, fold=0.05)
    for f in SIDES:
        face = skin.face("body", f)
        rows(face, 0, 1, VEST_D)
        rows(face, 19, 20, STRAP)
        rows(face, 21, 23, PANTS)
    front = skin.face("body", "north")
    # open vest over the navy shirt, zip pockets
    front.fill(SHIRT, box(front, 0, 6, 18, 9))
    front.fill(VEST_D, box(front, 0, 5, 18, 5) | box(front, 0, 10, 18, 10))
    for c0 in (1, 11):
        front.fill(VEST_D, box(front, 11, c0, 11, c0 + 3))
    # the tube strap across his chest
    for r in range(0, 18):
        c = int(round(13 - r * 12 / 17))
        front.set(r, c, STRAP)
    front.set(9, 7, STEEL)
    back = skin.face("body", "south")
    for r in range(0, 18):
        c = int(round(2 + r * 12 / 17))
        back.set(r, c, STRAP)
    for face in skin.each("jacket"):
        face.clear()


def paint_arms(skin):
    for arm, slv, seed in (("rightArm", "rightSleeve", 12300), ("leftArm", "leftSleeve", 12310)):
        for f in SIDES + ("up", "down"):
            cloth(skin.face(arm, f), SHIRT, seed + len(f), var=0.04, fold=0.06)
        for f in SIDES:
            face = skin.face(arm, f)
            face.fill(VEST, face.row <= 2)
            face.fill(VEST_D, face.row == 2)
            wraps(face, 17, 20)
            rows(face, 21, 23, SKIN)
        skin.face(arm, "down").fill(SKIN_D)
        for face in skin.each(slv):
            face.clear()


def paint_legs(skin, boot_h):
    for leg, pants, seed in (("rightLeg", "rightPants", 12400), ("leftLeg", "leftPants", 12410)):
        for f in SIDES:
            face = skin.face(leg, f)
            cloth(face, PANTS, seed + len(f), var=0.05, fold=0.07, freq=0.9, mask=face.row <= 12)
            rows(face, 13, 23, SKIN)
        skin.face(leg, "up").fill(PANTS)
        skin.face(leg, "down").fill(SKIN_D)
        for face in skin.each(pants):
            face.clear()
        for f in SIDES:
            face = skin.face(pants, f)
            rows(face, 11, 12, (78, 82, 94))
            wraps(face, 14, 19)
    paint_holster(skin, "right")
    clear_under_shoes(skin, boot_h)
