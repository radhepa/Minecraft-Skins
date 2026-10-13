"""Suzu the Field Medic: the village's calm, quick-handed medic, who patches
up every academy kid and gate guard. A rose-brown bob with a little bun tied
in a white ribbon, warm hazel eyes, the village headband, a white medic
tunic with teal trim and a soul-heart emblem, a matching armband, a leather
satchel slung across her, bandaged forearms with hands glowing soft healing
mint, cropped teal trousers and sandals.
"""

import numpy as np

from paintkit import SIDES, box, clear_under_shoes, cloth, rows, skin_tone
from skinlib import Skin, add_standard_body, noise

from .shinobi import (add_headband, add_holster, add_sandals, female_face, hair_head,
                      hair_painter, paint_headband, paint_holster, paint_sandals, wraps)

ID = "geometry.LandOfTheHiddenSift.Suzu"
TEXTURE = "suzu.png"
NAME = "Suzu the Field Medic"
LOC = "Suzu"
DETAILS = [
    ("face", "Bob with a ribboned bun", {"yaw": 28, "pitch": 4, "dist": 48, "target": 28, "fov": 30}),
    ("satchel", "Medic satchel", {"yaw": -50, "pitch": 6, "dist": 56, "target": 15, "fov": 30}),
    ("hands", "Healing glow", {"yaw": 20, "pitch": 0, "dist": 54, "target": 13, "fov": 30}),
]

SKIN = (250, 220, 200)
SKIN_D = (226, 186, 168)
BLUSH = (248, 170, 170)
HAIR = (176, 106, 96)
HAIR_D = (122, 66, 62)
HAIR_L = (212, 148, 132)
LASH = (66, 34, 32)
EYE_D = (98, 72, 38)
EYE = (162, 124, 62)
EYE_L = (216, 186, 116)
WHITE = (255, 255, 255)
MOUTH = (210, 124, 124)
TUNIC = (246, 244, 238)
TUNIC_D = (212, 210, 202)
TEAL = (40, 150, 146)
TEAL_D = (24, 100, 100)
HEART = (64, 196, 176)
LEATHER = (138, 88, 54)
LEATHER_D = (96, 58, 34)
LEATHER_L = (176, 122, 80)
PANTS = (34, 86, 92)
PANTS_D = (22, 58, 64)
GLOW = (176, 255, 226)
GLOW_C = (236, 255, 246)
SANDAL = (90, 64, 50)
SANDAL_D = (60, 40, 32)


def build():
    skin = Skin(ID, slim=True)
    add_standard_body(skin)
    add_headband(skin, yc=30.0)
    skin.acc("bun", "head", [-1.25, 27.0, 4.3], [2.5, 2.5, 2], lowres=("down",))
    skin.acc("ribbon", "head", [-1.5, 26.6, 5.3], [3, 0.75, 1.1], lowres=SIDES + ("up", "down"))
    skin.acc("satchel", "body", [3.6, 10.5, -1.75], [1.5, 3.5, 3.5], lowres=("up", "down"))
    add_holster(skin, "right")
    h = add_sandals(skin)
    paint_head(skin)
    paint_gear(skin)
    paint_body(skin)
    paint_arms(skin)
    paint_legs(skin, h)
    paint_sandals(skin, SANDAL, SANDAL_D, SKIN, SKIN_D)
    return skin


def heart(face, top, left, colour=HEART, line=TEAL_D):
    face.stamp([".HH.HH.", "HHHHHHH", ".HHHHH.", "..HHH..", "...H..."], {"H": colour}, top=top, left=left)
    face.fill(line, (face.row == top + 2) & (face.col == left + 3))


def paint_head(skin):
    rose = hair_painter(HAIR, HAIR_D, HAIR_L, shine=(232, 176, 160))
    # a jaw-length bob: long at the sides, a straight soft fringe
    hair_head(skin, rose, 9000, SKIN, SKIN_D,
              [12, 11, 7, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 7, 11, 12], back_bottom=11, long_sides=True)
    front = skin.face("head", "north")
    female_face(front, {"L": LASH, "W": WHITE, "D": EYE_D, "E": EYE, "H": EYE_L, "G": EYE_L},
                MOUTH, blush=BLUSH)
    paint_headband(skin)
    for face in skin.each("bun"):
        rose(face, 9100 + len(face.face), None)
    for face in skin.each("ribbon"):
        face.fill(WHITE)
        face.fill(TUNIC_D, face.row == face.h - 1)


def paint_gear(skin):
    for face in skin.each("satchel"):
        cloth(face, LEATHER, 9200 + face.w, var=0.05, fold=0.04)
        face.fill(LEATHER_D, face.row == face.h - 1)
    flap = skin.face("satchel", "west")
    flap.fill(LEATHER_L, flap.row <= 2)
    flap.fill(LEATHER_D, flap.row == 3)
    heart(flap, 3, 0)


def paint_body(skin):
    for f in SIDES + ("up", "down"):
        cloth(skin.face("body", f), TUNIC, 9300 + len(f), var=0.03, fold=0.04)
    for f in SIDES:
        face = skin.face("body", f)
        rows(face, 0, 1, TEAL)
        rows(face, 17, 18, TEAL)
        rows(face, 19, 23, PANTS)
    front = skin.face("body", "north")
    front.fill(TEAL_D, (front.col == 7) & (front.row >= 2) & (front.row <= 16))
    heart(front, 4, 9)
    # satchel strap from her right shoulder to her left hip
    for r in range(0, 20):
        c = int(round(1 + r * 13 / 19))
        front.set(r, c, LEATHER)
        front.set(r, c + 1, LEATHER_D)
    back = skin.face("body", "south")
    for r in range(0, 20):
        c = int(round(14 - r * 13 / 19))
        back.set(r, c, LEATHER)
        back.set(r, c - 1, LEATHER_D)
    for face in skin.each("jacket"):
        face.clear()


def paint_arms(skin):
    for arm, slv, seed in (("rightArm", "rightSleeve", 9400), ("leftArm", "leftSleeve", 9410)):
        for f in SIDES + ("up", "down"):
            skin_tone(skin.face(arm, f), SKIN, seed + len(f), var=0.02)
        for f in SIDES:
            face = skin.face(arm, f)
            cloth(face, TUNIC, seed + 5 + len(f), var=0.03, fold=0.04, mask=face.row <= 6)
            rows(face, 6, 6, TEAL)
            wraps(face, 12, 19)
        skin.face(arm, "up").fill(TUNIC)
        skin.face(arm, "down").fill(SKIN_D)
        for face in skin.each(slv):
            face.clear()
        for f in SIDES:
            face = skin.face(slv, f)
            # a soft healing glow round her hands
            rs = np.random.RandomState(seed + 20 + len(f))
            glow = (face.row >= 20) & (rs.rand(face.h, face.w) < 0.45)
            face.fill(GLOW, glow)
            face.fill(GLOW_C, glow & (rs.rand(face.h, face.w) < 0.3))
        if arm == "leftArm":
            for f in SIDES:
                band = skin.face(slv, f)
                rows(band, 2, 5, TUNIC)
                rows(band, 2, 2, TEAL)
                rows(band, 5, 5, TEAL)
            heart(skin.face(slv, "west"), 1, 1) if skin.face(slv, "west").w >= 7 else None
            out = skin.face(slv, "west")
            out.fill(HEART, box(out, 3, 2, 4, out.w - 3))


def paint_legs(skin, boot_h):
    for leg, pants, seed in (("rightLeg", "rightPants", 9500), ("leftLeg", "leftPants", 9510)):
        for f in SIDES:
            face = skin.face(leg, f)
            skin_tone(face, SKIN, seed + len(f), var=0.02)
            cloth(face, PANTS, seed + 5 + len(f), var=0.04, fold=0.06, mask=face.row <= 14)
            rows(face, 14, 14, PANTS_D)
        skin.face(leg, "up").fill(PANTS)
        skin.face(leg, "down").fill(SKIN_D)
        for face in skin.each(pants):
            face.clear()
        for f in SIDES:
            face = skin.face(pants, f)
            rows(face, 13, 14, (52, 112, 116))
            wraps(face, 17, 19)
    paint_holster(skin, "right")
    clear_under_shoes(skin, boot_h)
