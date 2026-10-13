"""Pip: tiny alien from Pluto, the far, frosty dwarf planet. Rosy cheeks and
big shiny eyes peek out of a cocoa parka with a fluffy 3D fur-trimmed hood,
Pluto's famous heart on the chest, cream mittens, snow pants, fur-cuffed
snow boots, and Charon, a little moon buddy with a face, floating by
Pip's shoulder.
"""

import numpy as np

from paintkit import (SIDES, add_footwear, box, cells, clear_under_shoes, cloth,
                      gradient, paint_boots, rows, skin_tone)
from skinlib import Skin, add_standard_body, noise

ID = "geometry.SolarSystem.Pip"
TEXTURE = "pip.png"
NAME = "Pip"
LOC = "Pip"
DETAILS = [
    ("face", "Fur-trimmed 3D hood", {"yaw": 20, "pitch": 6, "dist": 52, "target": 27, "fov": 30}),
    ("charon", "Charon, the moon buddy", {"yaw": 40, "pitch": 8, "dist": 58, "target": 24, "fov": 30}),
    ("back34", "Cosy parka", {"yaw": 150, "pitch": 10}),
]

SKIN = (246, 208, 222)
SKIN_D = (226, 182, 200)
ORB = (150, 220, 255)
ORB_L = (230, 250, 255)
BLUSH = (246, 150, 150)
EYE = (52, 34, 40)
EYE_M = (96, 60, 64)
WHITE = (255, 255, 255)
PARKA = (146, 86, 62)
PARKA_D = (110, 60, 44)
PARKA_H = (176, 112, 82)
FUR = (250, 240, 222)
FUR_M = (234, 218, 194)
FUR_D = (206, 184, 156)
HEART = (252, 236, 210)
HEART_D = (226, 200, 168)
SNOW = (84, 66, 70)
SNOW_D = (60, 46, 50)
CHARON = (170, 166, 170)
CHARON_D = (130, 124, 130)
CHARON_CAP = (120, 70, 60)
MOUTH = (140, 70, 80)

BOOTS = {"upper": (98, 66, 56), "hi": (130, 92, 76), "dark": (70, 46, 40), "strap": FUR_D,
         "strap_dark": FUR, "sole": (60, 50, 50), "sole_dark": (40, 32, 34)}


def build():
    skin = Skin(ID)
    add_standard_body(skin)
    # fluffy fur ruff framing the face, standing proud of the hood
    skin.acc("ruffTop", "head", [-5, 31.25, -5.25], [10, 2, 2], lowres=("up", "down", "south"))
    skin.acc("ruffR", "head", [-5.25, 23.75, -5.25], [2, 7.5, 2], lowres=("up", "down", "south"))
    skin.acc("ruffL", "head", [3.25, 23.75, -5.25], [2, 7.5, 2], like="ruffR")
    # little antennae poking out through the hood
    for side, x, lean in (("R", -1.75, -18), ("L", 1.75, 18)):
        kw = dict(pivot=[x, 32.5, 0.5], rotation=[0, 0, lean])
        if side == "R":
            skin.acc("stalkR", "head", [x - 0.25, 32.5, 0.25], [0.5, 2.5, 0.5], lowres=("up", "down"), **kw)
            skin.acc("orbR", "head", [x - 0.75, 35, -0.25], [1.5, 1.5, 1.5], **kw)
        else:
            skin.acc("stalkL", "head", [x - 0.25, 32.5, 0.25], [0.5, 2.5, 0.5], like="stalkR", **kw)
            skin.acc("orbL", "head", [x - 0.75, 35, -0.25], [1.5, 1.5, 1.5], like="orbR", **kw)
    # Charon floats by Pip's right shoulder, tilted a little
    skin.bone("charon", "body", [-9, 27, 0], rotation=[0, 15, -10])
    skin.acc("moon", "charon", [-11, 25.5, -1.75], [3.5, 3.5, 3.5])
    skin.acc("mitR", "rightArm", [-8.25, 11.75, -2.25], [4.5, 3.5, 4.5], lowres=("up",))
    skin.acc("mitL", "leftArm", [3.75, 11.75, -2.25], [4.5, 3.5, 4.5], like="mitR")
    h = add_footwear(skin, height=3.5, length=5.5, toe=1.0, tongue=False)
    paint_head(skin)
    paint_ruff(skin)
    paint_charon(skin)
    paint_antennae(skin)
    paint_body(skin)
    paint_arms(skin)
    paint_legs(skin, h)
    paint_boots(skin, BOOTS, 8900, straps=())
    paint_boot_cuffs(skin)
    return skin


def fur(face, seed, size=2.5):
    """Fluffy fur: soft clumps, lighter at the tips."""
    centre, lane = cells(face, seed, size)
    gradient(face, [(0, FUR), (0.6, FUR_M), (1, FUR_D)], t=centre)
    face.fill(FUR_D, lane & (centre > 0.7))
    face.shade(noise((face.h, face.w), seed + 1, 0.02))


def parka(face, seed):
    cloth(face, PARKA, seed, var=0.04, fold=0.06, freq=0.9)
    # quilted puffer channels
    face.shade(np.where(face.row % 5 == 4, 0.86, 1.0))


def paint_head(skin):
    front = skin.face("head", "north")
    skin_tone(front, SKIN, 8000, var=0.015)
    # big shiny eyes
    eye = [
        ".EEE.",
        "EWWEE",
        "EWEEE",
        "EEEWE",
        ".EEE.",
    ]
    pal = {"E": EYE, "W": WHITE}
    front.stamp(eye, pal, top=6, left=2)
    front.stamp(eye, pal, top=6, left=9, mirror=True)
    for c in (2, 3, 12, 13):
        front.set(11, c, BLUSH)
        front.set(12, c, BLUSH)
    front.stamp(["M..M", ".MM."], {"M": MOUTH}, top=12, left=6)
    front.set(10, 7, SKIN_D)
    # parka hood over the rest of the head (base layer)
    for f in ("east", "west", "south", "up", "down"):
        parka(skin.face("head", f), 8010 + len(f))
    rows(front, 0, 3, PARKA)
    front.fill(PARKA, (front.col <= 1) | (front.col >= 14))
    # hat layer: the puffy hood shell
    for face in skin.each("hat"):
        face.clear()
    for f in ("east", "west", "south", "up"):
        face = skin.face("hat", f)
        parka(face, 8020 + len(f))
        face.shade(np.where(face.col % 6 == 5, 0.9, 1.0))
    for f in ("east", "west"):
        rows(skin.face("hat", f), 15, 15, PARKA_D)


def paint_ruff(skin):
    for name in ("ruffTop", "ruffR"):
        for face in skin.each(name):
            fur(face, 8100 + face.w * 3 + face.h)
        for f in ("north", "east", "west"):
            if (name, f) in skin.faces:
                face = skin.face(name, f)
                # tufty outline
                face.clear((face.row == 0) & (face.col % 3 == 0) & (name == "ruffTop"))


def paint_antennae(skin):
    for face in skin.each("stalkR"):
        gradient(face, [(0, SKIN), (1, SKIN_D)])
    for face in skin.each("orbR"):
        face.fill(ORB)
        face.fill(ORB_L, (face.row == 0) | (face.col == 0))


def paint_charon(skin):
    for face in skin.each("moon"):
        face.fill(CHARON)
        rs = np.random.RandomState(8200 + face.w + len(face.face))
        face.fill(CHARON_D, rs.rand(face.h, face.w) < 0.2)
        d = np.maximum(abs(face.row - (face.h - 1) / 2), abs(face.col - (face.w - 1) / 2))
        face.shade(np.where(d >= (face.w - 1) / 2 - 0.01, 0.82, 1.06))
    # Charon's reddish polar cap, and a sleepy little face
    top = skin.face("moon", "up")
    top.fill(CHARON_CAP)
    for f in SIDES:
        rows(skin.face("moon", f), 0, 0, CHARON_CAP)
    face = skin.face("moon", "north")
    face.stamp(["E...E", "E...E", ".....", "..M.."], {"E": EYE, "M": MOUTH}, top=2, left=1)
    face.set(4, 0, BLUSH)
    face.set(4, 6, BLUSH)


def paint_body(skin):
    for f in SIDES + ("up", "down"):
        parka(skin.face("body", f), 8300 + len(f))
    front = skin.face("body", "north")
    # zip and Pluto's heart
    front.fill(PARKA_D, (front.col == 7) & (front.row >= 2))
    heart = [
        ".HHH..HHH.",
        "HHHHHHHHHH",
        "HHLHHHHHHH",
        "HHHHHHHHHH",
        ".HHHHHHHH.",
        "..HHHHHH..",
        "...HHHH...",
        "....HH....",
    ]
    front.stamp(heart, {"H": HEART, "L": WHITE}, top=6, left=3)
    for r, line in enumerate(heart):
        for c, ch in enumerate(line):
            if ch != "." and (r + 1 >= len(heart) or heart[r + 1][c] == "."):
                front.set(6 + r, 3 + c, HEART_D)
    # fur-lined hem on the jacket layer
    for face in skin.each("jacket"):
        face.clear()
    for f in SIDES:
        face = skin.face("jacket", f)
        fur(face, 8310 + len(f))
        face.clear(face.row < 20)
        face.clear((face.row == 20) & (face.col % 2 == 0))
    jk = skin.face("jacket", "north")
    fur(jk, 8320)
    jk.clear(~((jk.row >= 20) | (jk.row <= 1)))
    jk.clear((jk.row == 1) & (jk.col % 2 == 1))
    skin.face("jacket", "up").clear()
    skin.face("jacket", "down").clear()


def paint_arms(skin):
    for arm, slv, seed in (("rightArm", "rightSleeve", 8400), ("leftArm", "leftSleeve", 8410)):
        for f in SIDES + ("up", "down"):
            parka(skin.face(arm, f), seed + len(f))
        for face in skin.each(slv):
            face.clear()
        # fur cuff above the mitten
        for f in SIDES:
            face = skin.face(slv, f)
            fur(face, seed + 20 + len(f))
            face.clear((face.row < 14) | (face.row > 16))
    for face in skin.each("mitR"):
        fur(face, 8450 + face.w, size=3.5)
        face.shade(0.96)
    for f in SIDES:
        face = skin.face("mitR", f)
        face.fill(FUR_D, face.row == face.h - 1)
    down = skin.face("mitR", "down")
    down.fill(FUR_D)


def paint_legs(skin, boot_h):
    for leg, pants, outer, seed in (("rightLeg", "rightPants", "east", 8500), ("leftLeg", "leftPants", "west", 8510)):
        for f in SIDES:
            face = skin.face(leg, f)
            cloth(face, SNOW, seed + len(f), var=0.05, fold=0.07, freq=0.8)
            face.shade(np.where(face.row % 6 == 5, 0.86, 1.0))
            if f == outer:
                face.fill(HEART_D, (face.col == 3) & (face.row % 3 == 0))
        skin.face(leg, "up").fill(SNOW)
        skin.face(leg, "down").fill(SNOW_D)
        for face in skin.each(pants):
            face.clear()
    clear_under_shoes(skin, boot_h)


def paint_boot_cuffs(skin):
    for side in ("right", "left"):
        shoe = f"{side}Shoe"
        for f in SIDES:
            face = skin.face(shoe, f)
            top = face.row <= 2
            tmp = face.rgba.copy()
            fur(face, 8600 + face.w + len(f))
            face.rgba = np.where(top[..., None], face.rgba, tmp)
        up = skin.face(shoe, "up")
        fur(up, 8610)
