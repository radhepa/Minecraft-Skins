"""Kenji the Academy Hopeful: a sharp, stubborn young genin fresh out of the
academy and itching for his first real mission. Short dark hair with a
side-swept fringe and sideburns, thick brows over steady grey-green eyes,
the village headband, a slate high-collar jacket with teal piping, a utility
belt with a pouch and a training scroll, fingerless gloves, a steel armguard,
cargo trousers bound at the shins, a thigh holster and shinobi sandals.
"""

import numpy as np

from paintkit import SIDES, box, clear_under_shoes, cloth, hair, rows, skin_tone
from skinlib import Skin, add_standard_body, noise

from .shinobi import (EYE_SHARP, STEEL, STEEL_D, STEEL_L, add_headband, add_holster,
                      add_sandals, anime_eyes, brows, paint_headband, paint_holster,
                      paint_sandals, wraps)

ID = "geometry.LandOfTheHiddenSift.Kenji"
TEXTURE = "kenji.png"
NAME = "Kenji the Academy Hopeful"
LOC = "Kenji"
DETAILS = [
    ("face", "Village headband", {"yaw": 18, "pitch": 4, "dist": 46, "target": 28, "fov": 30}),
    ("gear", "Armguard + belt pouch", {"yaw": -45, "pitch": 6, "dist": 60, "target": 15, "fov": 30}),
    ("back34", "Training scroll", {"yaw": 160, "pitch": 10}),
]

SKIN = (234, 194, 158)
SKIN_D = (206, 160, 126)
HAIR = (54, 42, 38)
HAIR_D = (28, 22, 20)
HAIR_L = (92, 74, 64)
BROW = (40, 30, 26)
LASH = (24, 18, 16)
EYE_D = (58, 82, 70)
EYE = (96, 132, 112)
EYE_L = (150, 186, 162)
WHITE = (246, 246, 244)
MOUTH = (174, 122, 98)
JACKET = (58, 68, 80)
JACKET_D = (38, 44, 54)
JACKET_L = (84, 96, 110)
PIPING = (52, 168, 168)
SHIRT = (40, 42, 48)
CARGO = (78, 82, 70)
CARGO_D = (54, 58, 48)
BELT = (70, 52, 40)
BELT_D = (46, 34, 26)
GLOVE = (34, 34, 40)
SCROLL = (232, 220, 190)
SCROLL_R = (176, 64, 54)
SANDAL = (38, 44, 58)
SANDAL_D = (22, 26, 36)


def build():
    skin = Skin(ID)
    add_standard_body(skin)
    add_headband(skin, yc=30.0)
    # training scroll across the small of his back, a pouch on the belt
    skin.acc("scroll", "body", [-3.5, 12.6, 2.1], [7, 1.75, 1.75], lowres=("up", "down", "north"),
             first=True)
    skin.acc("pouch", "body", [1.6, 11.5, -2.85], [2, 2, 0.85], lowres=("up", "down", "east", "west"))
    # steel armguard on the left forearm
    skin.acc("guard", "leftArm", [3.75, 14.0, -2.25], [4.5, 3.5, 4.5], lowres=("up", "down"))
    add_holster(skin, "right")
    h = add_sandals(skin)
    paint_head(skin)
    paint_gear(skin)
    paint_body(skin)
    paint_arms(skin)
    paint_legs(skin, h)
    paint_sandals(skin, SANDAL, SANDAL_D, SKIN, SKIN_D)
    return skin


def dark_hair(face, seed, mask=None):
    hair(face, HAIR, HAIR_D, HAIR_L, seed, mask=mask)


def paint_head(skin):
    front = skin.face("head", "north")
    skin_tone(front, SKIN, 7000, var=0.012)
    dark_hair(front, 7001, mask=front.row <= 6)
    brows(front, 7, BROW)
    anime_eyes(front, 8, EYE_SHARP, {"L": LASH, "W": WHITE, "D": EYE_D, "E": EYE, "H": EYE_L,
                                     "G": EYE_L}, lefts=(2, 10))
    # small, straight mouth a few shades darker than his skin
    rows(front, 13, 13, MOUTH, (front.col >= 7) & (front.col <= 9))
    # a little jaw shading
    front.shade(0.95, (front.row == 15) & ((front.col <= 2) | (front.col >= 13)))
    for f in ("east", "west", "south", "up"):
        face = skin.face("head", f)
        skin_tone(face, SKIN, 7010 + len(f))
        if f in ("south", "up"):
            dark_hair(face, 7020 + len(f))
        else:
            ear = (face.row >= 8) & (face.row <= 11) & (np.abs(face.Z + 0.5) <= 1.5)
            # short at the sides: hair above the ear and a sideburn in front
            burn = (face.Z < -2.6) & (face.Z > -3.6) & (face.row <= 10)
            dark_hair(face, 7030 + len(f), mask=(((face.Z > -1) & (face.row <= 11)) | (face.row <= 6) | burn) & ~ear)
            face.fill(SKIN_D, ear & (np.abs(face.Z + 0.5) <= 0.6) & (face.row >= 9) & (face.row <= 10))
    back = skin.face("head", "south")
    back.fill(SKIN, back.row >= 13)
    skin_tone(skin.face("head", "down"), SKIN_D, 7040)

    for face in skin.each("hat"):
        face.clear()
    dark_hair(skin.face("hat", "up"), 7050)
    hf = skin.face("hat", "north")
    dark_hair(hf, 7051)
    # side-swept fringe: longer on his right, short sideburns
    fringe = np.array([9, 8, 6, 5, 4, 3, 3, 2, 2, 2, 1, 1, 1, 2, 6, 7])
    hf.clear(hf.row > fringe[hf.col])
    for f in ("east", "west", "south"):
        face = skin.face("hat", f)
        dark_hair(face, 7052 + len(f))
        bottom = 10 + (face.col % 4 == 1)
        face.clear(face.row > bottom)
        if f != "south":
            face.clear((face.Z < -1.0) & (face.Z > -3.8) & (face.row > 5))
    paint_headband(skin)


def paint_gear(skin):
    for face in skin.each("scroll"):
        face.fill(SCROLL)
        face.shade(noise((face.h, face.w), 7100 + face.w, 0.03))
    for f in ("south", "up", "down", "north"):
        face = skin.face("scroll", f)
        face.fill(SCROLL_R, (face.col <= 1) | (face.col >= face.w - 2))
        face.fill(BELT_D, (face.col == face.w // 2))
    for f in ("east", "west"):
        end = skin.face("scroll", f)
        end.fill(SCROLL_R)
        end.fill((214, 196, 160), box(end, 1, 1, end.h - 2, end.w - 2))
    for face in skin.each("pouch"):
        face.fill(BELT)
        face.shade(noise((face.h, face.w), 7110 + face.w, 0.05))
    p = skin.face("pouch", "north")
    rows(p, 0, 1, (92, 70, 54))
    p.set(1, p.w // 2, STEEL)
    for face in skin.each("guard"):
        face.fill(STEEL)
        face.shade(noise((face.h, face.w), 7120 + face.w, 0.03))
        face.fill(STEEL_L, face.row == 0)
        face.fill(STEEL_D, face.row == face.h - 1)
    out = skin.face("guard", "west")
    out.fill(STEEL_D, box(out, 2, 2, 4, out.w - 3))
    out.fill(PIPING, box(out, 3, 3, 3, out.w - 4))


def paint_body(skin):
    for f in SIDES + ("up", "down"):
        cloth(skin.face("body", f), JACKET, 7200 + len(f), var=0.04, fold=0.05)
    for f in SIDES:
        face = skin.face("body", f)
        rows(face, 0, 2, JACKET_D)
        rows(face, 2, 2, PIPING)
        rows(face, 19, 21, BELT)
        rows(face, 19, 19, BELT_D)
        rows(face, 22, 23, CARGO)
    front = skin.face("body", "north")
    # zip front with teal piping and chest panels
    front.fill(SHIRT, box(front, 0, 7, 2, 8))
    front.fill(STEEL, (front.col == 7) & (front.row >= 3) & (front.row <= 18))
    front.fill(JACKET_D, (front.col == 8) & (front.row >= 3) & (front.row <= 18))
    for c in (3, 12):
        front.fill(PIPING, (front.col == c) & (front.row >= 3) & (front.row <= 9))
    front.fill(JACKET_L, box(front, 10, 2, 10, 5) | box(front, 10, 10, 10, 13))
    front.fill(STEEL, box(front, 19, 7, 21, 8))
    back = skin.face("body", "south")
    back.fill(JACKET_D, (back.col == 7) | (back.col == 8))
    for face in skin.each("jacket"):
        face.clear()
    # standing collar
    for f in SIDES:
        face = skin.face("jacket", f)
        face.fill(JACKET_L, face.row <= 1)
        face.fill(PIPING, face.row == 0)
    jk = skin.face("jacket", "north")
    jk.clear(box(jk, 0, 6, 1, 9))


def paint_arms(skin):
    for arm, slv, seed in (("rightArm", "rightSleeve", 7300), ("leftArm", "leftSleeve", 7310)):
        for f in SIDES + ("up", "down"):
            cloth(skin.face(arm, f), JACKET, seed + len(f), var=0.04, fold=0.06)
        for f in SIDES:
            face = skin.face(arm, f)
            rows(face, 3, 3, PIPING)
            rows(face, 18, 23, GLOVE)
            rows(face, 18, 18, JACKET_D)
            face.fill(SKIN, (face.row == 23) & (face.col % 2 == 0))
        skin.face(arm, "down").fill(GLOVE)
        for face in skin.each(slv):
            face.clear()
        for f in SIDES:
            face = skin.face(slv, f)
            rows(face, 16, 17, JACKET_L)
            rows(face, 17, 17, JACKET_D)


def paint_legs(skin, boot_h):
    for leg, pants, seed in (("rightLeg", "rightPants", 7400), ("leftLeg", "leftPants", 7410)):
        for f in SIDES:
            face = skin.face(leg, f)
            cloth(face, CARGO, seed + len(f), var=0.05, fold=0.07, freq=0.9)
        out = skin.face(leg, "east" if leg == "rightLeg" else "west")
        out.fill(CARGO_D, box(out, 3, 1, 8, 6) & ~box(out, 4, 2, 7, 5))
        out.fill(CARGO_D, box(out, 3, 1, 3, 6))
        skin.face(leg, "up").fill(CARGO)
        skin.face(leg, "down").fill(CARGO_D)
        for face in skin.each(pants):
            face.clear()
        for f in SIDES:
            face = skin.face(pants, f)
            wraps(face, 14, 19)
            face.shade(0.85, (face.row >= 14) & (face.row <= 19))
    paint_holster(skin, "right")
    clear_under_shoes(skin, boot_h)
