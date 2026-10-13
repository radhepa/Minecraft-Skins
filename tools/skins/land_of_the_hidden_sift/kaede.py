"""Kaede the Blade Smith: forges every kunai and blade in the village and
will tell you exactly what you did wrong to the last one. Auburn hair in a
high ponytail, green eyes, a soot smudge on her cheek, the village headband,
a charcoal tank top under a leather forge apron with tool pockets, bare
arms with one heavy leather glove and a wrapped forearm, work trousers and
her forging hammer in hand.
"""

import numpy as np

from paintkit import SIDES, box, clear_under_shoes, cloth, rows, skin_tone
from skinlib import Skin, add_standard_body, noise

from .shinobi import (STEEL, STEEL_D, STEEL_L, add_headband, add_sandals, female_face,
                      hair_head, hair_painter, paint_headband, paint_sandals, wraps)

ID = "geometry.LandOfTheHiddenSift.Kaede"
TEXTURE = "kaede.png"
NAME = "Kaede the Blade Smith"
LOC = "Kaede"
DETAILS = [
    ("face", "High ponytail + soot smudge", {"yaw": 30, "pitch": 4, "dist": 52, "target": 28, "fov": 30}),
    ("hammer", "Forging hammer + glove", {"yaw": 50, "pitch": 4, "dist": 56, "target": 10, "fov": 30}),
    ("back34", "Ponytail + apron ties", {"yaw": 160, "pitch": 10}),
]

SKIN = (244, 210, 182)
SKIN_D = (218, 176, 148)
SOOT = (150, 136, 130)
HAIR = (194, 82, 46)
HAIR_D = (128, 46, 26)
HAIR_L = (232, 132, 82)
LASH = (70, 30, 20)
EYE_D = (36, 92, 48)
EYE = (68, 156, 80)
EYE_L = (148, 212, 138)
WHITE = (255, 255, 255)
MOUTH = (200, 112, 100)
TANK = (52, 52, 60)
TANK_D = (36, 36, 42)
APRON = (124, 78, 46)
APRON_D = (88, 52, 28)
APRON_L = (160, 108, 68)
PANTS = (84, 82, 72)
PANTS_D = (60, 58, 50)
GLOVE = (100, 66, 40)
GLOVE_D = (70, 44, 26)
WOOD = (130, 88, 52)
WOOD_D = (92, 60, 34)
SANDAL = (70, 52, 40)
SANDAL_D = (44, 32, 24)


def build():
    skin = Skin(ID, slim=True)
    add_standard_body(skin)
    add_headband(skin, yc=29.8)
    # high ponytail tied at the crown, falling down her back
    skin.acc("tie", "head", [-1.0, 31.0, 3.6], [2, 1.5, 1.5], lowres=SIDES + ("up", "down"))
    skin.acc("ponytail", "head", [-1.25, 24.0, 4.4], [2.5, 7.5, 1.75], rotation=[16, 0, 0],
             pivot=[0, 31.5, 5.0], lowres=("up", "down"))
    # forging hammer hanging from her gloved right hand
    skin.acc("haft", "rightArm", [-5.85, 6.0, -0.35], [0.7, 6.5, 0.7], lowres=SIDES + ("up", "down"))
    skin.acc("hammerHead", "rightArm", [-7.25, 4.5, -1.25], [3.5, 1.75, 2.25], lowres=("up", "down"))
    h = add_sandals(skin)
    paint_head(skin)
    paint_gear(skin)
    paint_body(skin)
    paint_arms(skin)
    paint_legs(skin, h)
    paint_sandals(skin, SANDAL, SANDAL_D, SKIN, SKIN_D)
    return skin


def paint_head(skin):
    auburn = hair_painter(HAIR, HAIR_D, HAIR_L, shine=(246, 168, 112))
    hair_head(skin, auburn, 11000, SKIN, SKIN_D,
              [10, 9, 7, 6, 5, 4, 4, 3, 3, 3, 4, 4, 5, 6, 8, 9], back_bottom=10)
    front = skin.face("head", "north")
    female_face(front, {"L": LASH, "W": WHITE, "D": EYE_D, "E": EYE, "H": EYE_L, "G": EYE_L}, MOUTH)
    # a soot smudge on her left cheek
    for r, c in ((12, 12), (12, 13), (13, 13)):
        front.set(r, c, SOOT)
    paint_headband(skin)
    for face in skin.each("ponytail"):
        auburn(face, 11100 + len(face.face), None)
    for f in SIDES:
        face = skin.face("ponytail", f)
        face.clear((face.row == face.h - 1) & (face.col % 2 == 1))
    for face in skin.each("tie"):
        face.fill(TANK)


def paint_gear(skin):
    for face in skin.each("haft"):
        face.fill(WOOD)
        face.fill(WOOD_D, face.row % 3 == 0)
    for face in skin.each("hammerHead"):
        face.fill(STEEL_D)
        face.shade(noise((face.h, face.w), 11200 + face.w, 0.04))
        face.fill(STEEL, face.row == 0)
    for f in ("east", "west"):
        end = skin.face("hammerHead", f)
        end.fill(STEEL)
        end.fill(STEEL_L, box(end, 1, 1, end.h - 2, end.w - 2))


def paint_body(skin):
    for f in SIDES + ("up", "down"):
        cloth(skin.face("body", f), TANK, 11300 + len(f), var=0.04, fold=0.04)
    for f in SIDES:
        face = skin.face("body", f)
        rows(face, 20, 23, PANTS)
    front = skin.face("body", "north")
    # leather apron over the tank top, with a bib and pockets
    bib = (front.row >= 4) & (front.col >= 2) & (front.col <= 13)
    cloth(front, APRON, 11310, var=0.05, fold=0.04, mask=bib)
    front.fill(APRON_L, bib & (front.row == 4))
    front.fill(APRON_D, (front.row >= 0) & (front.row <= 3) & ((front.col == 3) | (front.col == 12)))
    for c0 in (3, 9):
        front.fill(APRON_D, box(front, 13, c0, 17, c0 + 3) & ~box(front, 14, c0 + 1, 16, c0 + 2))
    front.fill(STEEL, box(front, 14, 4, 16, 4))     # a file in one pocket
    back = skin.face("body", "south")
    rows(back, 14, 14, APRON_D)
    back.fill(APRON_D, box(back, 13, 7, 16, 8))
    for f in ("east", "west"):
        rows(skin.face("body", f), 14, 14, APRON_D)
    for face in skin.each("jacket"):
        face.clear()


def paint_arms(skin):
    for arm, slv, seed in (("rightArm", "rightSleeve", 11400), ("leftArm", "leftSleeve", 11410)):
        for f in SIDES + ("up", "down"):
            skin_tone(skin.face(arm, f), SKIN, seed + len(f), var=0.02)
        for f in SIDES:
            face = skin.face(arm, f)
            face.fill(TANK, face.row <= 1)
            if arm == "rightArm":
                cloth(face, GLOVE, seed + 5 + len(f), var=0.05, fold=0.04, mask=face.row >= 14)
                face.fill(GLOVE_D, face.row == 14)
            else:
                wraps(face, 12, 20)
        skin.face(arm, "down").fill(GLOVE if arm == "rightArm" else SKIN_D)
        for face in skin.each(slv):
            face.clear()
        if arm == "rightArm":
            for f in SIDES:
                face = skin.face(slv, f)
                rows(face, 13, 15, GLOVE)                 # flared glove cuff
                rows(face, 15, 15, GLOVE_D)


def paint_legs(skin, boot_h):
    for leg, pants, seed in (("rightLeg", "rightPants", 11500), ("leftLeg", "leftPants", 11510)):
        for f in SIDES:
            cloth(skin.face(leg, f), PANTS, seed + len(f), var=0.05, fold=0.07, freq=0.9)
        skin.face(leg, "up").fill(PANTS)
        skin.face(leg, "down").fill(PANTS_D)
        for face in skin.each(pants):
            face.clear()
        ap = skin.face(pants, "north")
        cloth(ap, APRON, seed + 9, var=0.05, fold=0.04, mask=ap.row <= 9)
        ap.fill(APRON_D, ap.row == 9)
        for f in SIDES:
            face = skin.face(pants, f)
            wraps(face, 16, 19)
            face.shade(0.85, (face.row >= 16) & (face.row <= 19))
    clear_under_shoes(skin, boot_h)
