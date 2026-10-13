"""Daichi the Gate Warden: the big, steady guard who has watched the village
gate for twenty years and knows every face that passes. Warm brown skin,
short black hair, calm dark eyes under heavy brows, a
wide straw kasa hat over the village headband, a deep teal flak vest with
pouches over a black undershirt, steel armguards, dark trousers bound at
the shins, and a long iron-capped staff.
"""

import numpy as np

from paintkit import SIDES, box, clear_under_shoes, cloth, rows, skin_tone
from skinlib import Skin, add_standard_body, noise

from .shinobi import (STEEL, STEEL_D, STEEL_L, add_headband, add_sandals, hair_head,
                      hair_painter, male_face, paint_headband, paint_sandals, wraps)

ID = "geometry.LandOfTheHiddenSift.Daichi"
TEXTURE = "daichi.png"
NAME = "Daichi the Gate Warden"
LOC = "Daichi"
DETAILS = [
    ("face", "Kasa hat + headband", {"yaw": 20, "pitch": 10, "dist": 58, "target": 29, "fov": 30}),
    ("staff", "Iron-capped staff", {"yaw": 40, "pitch": 4, "dist": 96, "target": 15, "fov": 30}),
    ("back34", "Flak vest", {"yaw": 160, "pitch": 10}),
]

SKIN = (168, 114, 80)
SKIN_D = (138, 90, 60)
HAIR = (34, 30, 30)
HAIR_D = (18, 16, 16)
HAIR_L = (64, 58, 56)
BROW = (28, 22, 20)
LASH = (20, 14, 12)
EYE_D = (40, 28, 22)
EYE = (78, 56, 40)
EYE_L = (124, 92, 66)
WHITE = (240, 236, 230)
MOUTH = (118, 74, 52)
STRAW = (216, 184, 112)
STRAW_D = (170, 136, 72)
STRAW_L = (240, 214, 150)
VEST = (40, 92, 96)
VEST_D = (26, 62, 66)
VEST_L = (64, 126, 128)
UNDER = (32, 32, 38)
UNDER_L = (52, 52, 60)
PANTS = (44, 44, 52)
WOOD = (120, 80, 48)
WOOD_D = (86, 56, 32)
SANDAL = (36, 36, 44)
SANDAL_D = (20, 20, 26)


def build():
    skin = Skin(ID)
    add_standard_body(skin)
    add_headband(skin, yc=29.6)
    # wide straw kasa, in rings narrowing to a peak
    for k, (half, y, h) in enumerate(((7.0, 31.6, 0.6), (5.25, 32.2, 1.0), (3.5, 33.2, 1.0), (1.75, 34.2, 0.8))):
        skin.acc(f"kasa{k}", "head", [-half, y, -half], [2 * half, h, 2 * half],
                 lowres=SIDES + ("up", "down"))
    # long staff gripped upright
    skin.acc("staff", "rightArm", [-6.4, 1.0, -3.0], [0.8, 27, 0.8], lowres=SIDES + ("up", "down"))
    h = add_sandals(skin)
    paint_head(skin)
    paint_gear(skin)
    paint_body(skin)
    paint_arms(skin)
    paint_legs(skin, h)
    paint_sandals(skin, SANDAL, SANDAL_D, SKIN, SKIN_D)
    return skin


def paint_head(skin):
    black = hair_painter(HAIR, HAIR_D, HAIR_L)
    hair_head(skin, black, 10000, SKIN, SKIN_D,
              [8, 7, 4, 3, 2, 2, 2, 2, 2, 2, 2, 2, 3, 4, 7, 8], back_bottom=10)
    front = skin.face("head", "north")
    male_face(front, BROW, {"L": LASH, "W": WHITE, "D": EYE_D, "E": EYE, "H": EYE_L, "G": EYE_L},
              MOUTH)
    # chin strap of the kasa down each cheek
    for f in ("east", "west"):
        face = skin.face("head", f)
        face.fill((96, 70, 40), (np.abs(face.Z + 2.6) < 0.3) & (face.row >= 6))
    paint_headband(skin)


def paint_gear(skin):
    for k in range(4):
        for face in skin.each(f"kasa{k}"):
            face.fill(STRAW)
            face.shade(noise((face.h, face.w), 10100 + 7 * k + face.w, 0.06))
            if face.face == "up":
                # woven rings
                d = np.maximum(np.abs(face.col - (face.w - 1) / 2), np.abs(face.row - (face.h - 1) / 2))
                face.fill(STRAW_D, d.astype(int) % 2 == 1)
                face.fill(STRAW_L, d.astype(int) % 4 == 0)
            elif face.face == "down":
                face.fill(STRAW_D)
            else:
                face.fill(STRAW_D, face.row == face.h - 1)
    for face in skin.each("staff"):
        face.fill(WOOD)
        face.fill(WOOD_D, face.row % 4 == 1)
        face.fill(STEEL, (face.row <= 1) | (face.row >= face.h - 2))
        face.fill(STEEL_D, (face.row == 12) | (face.row == 15))
    skin.face("staff", "up").fill(STEEL_L)
    skin.face("staff", "down").fill(STEEL)


def paint_body(skin):
    for f in SIDES + ("up", "down"):
        cloth(skin.face("body", f), VEST, 10200 + len(f), var=0.04, fold=0.04)
    for f in SIDES:
        face = skin.face("body", f)
        rows(face, 0, 2, VEST_L)
        rows(face, 2, 2, VEST_D)
        face.shade(np.where(face.row % 5 == 4, 0.88, 1.0))
        rows(face, 18, 19, UNDER_L)
        rows(face, 20, 23, PANTS)
    front = skin.face("body", "north")
    front.fill(VEST_D, (front.col == 7) & (front.row >= 3) & (front.row <= 17))
    for c0 in (2, 10):
        front.fill(VEST_D, box(front, 10, c0, 15, c0 + 3))
        front.fill(VEST_L, box(front, 10, c0, 11, c0 + 3))
        front.set(11, c0 + 1, STEEL)
    for face in skin.each("jacket"):
        face.clear()
    for f in SIDES:
        skin.face("jacket", f).fill(VEST_L, skin.face("jacket", f).row == 0)


def paint_arms(skin):
    for arm, slv, seed in (("rightArm", "rightSleeve", 10300), ("leftArm", "leftSleeve", 10310)):
        for f in SIDES + ("up", "down"):
            cloth(skin.face(arm, f), UNDER, seed + len(f), var=0.04, fold=0.05)
        for f in SIDES:
            face = skin.face(arm, f)
            face.fill(VEST, face.row <= 3)
            face.fill(VEST_D, face.row == 3)
            rows(face, 21, 23, SKIN)
        skin.face(arm, "down").fill(SKIN_D)
        for face in skin.each(slv):
            face.clear()
        for f in SIDES:
            face = skin.face(slv, f)
            rows(face, 13, 19, STEEL)
            rows(face, 13, 13, STEEL_L)
            rows(face, 19, 19, STEEL_D)
            rows(face, 16, 16, STEEL_D)


def paint_legs(skin, boot_h):
    for leg, pants, seed in (("rightLeg", "rightPants", 10400), ("leftLeg", "leftPants", 10410)):
        for f in SIDES:
            cloth(skin.face(leg, f), PANTS, seed + len(f), var=0.05, fold=0.07, freq=0.9)
        skin.face(leg, "up").fill(PANTS)
        skin.face(leg, "down").fill(PANTS)
        for face in skin.each(pants):
            face.clear()
        for f in SIDES:
            face = skin.face(pants, f)
            wraps(face, 14, 19)
            face.shade(0.8, (face.row >= 14) & (face.row <= 19))
    clear_under_shoes(skin, boot_h)
