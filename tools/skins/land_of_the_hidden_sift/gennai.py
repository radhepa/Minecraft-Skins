"""Gennai the Noodle Chef: runs the steaming noodle stall by the village
gate, where every shinobi ends up after a mission. A cheerful middle-aged
man with greying hair, bushy brows and a neat moustache, a white bandana
knotted at the back, a white chef's coat with teal trim and rolled sleeves,
a navy apron printed with a steaming bowl, and his giant ladle.
"""

import numpy as np

from paintkit import SIDES, box, clear_under_shoes, cloth, rows, skin_tone
from skinlib import Skin, add_standard_body, noise

from .shinobi import (STEEL, STEEL_D, STEEL_L, add_sandals, hair_head, hair_painter, male_face,
                      paint_sandals)

ID = "geometry.LandOfTheHiddenSift.Gennai"
TEXTURE = "gennai.png"
NAME = "Gennai the Noodle Chef"
LOC = "Gennai"
DETAILS = [
    ("face", "Bandana + moustache", {"yaw": 18, "pitch": 4, "dist": 46, "target": 28, "fov": 30}),
    ("ladle", "Giant ladle", {"yaw": 40, "pitch": 14, "dist": 60, "target": 18, "fov": 30}),
    ("back34", "Bandana knot", {"yaw": 160, "pitch": 10}),
]

SKIN = (238, 196, 160)
SKIN_D = (210, 162, 128)
HAIR = (96, 92, 92)
HAIR_D = (60, 56, 58)
HAIR_L = (150, 146, 146)
BROW = (70, 66, 66)
LASH = (40, 30, 26)
EYE_D = (70, 48, 30)
EYE = (122, 86, 52)
EYE_L = (176, 136, 90)
WHITE = (246, 246, 242)
MOUTH = (172, 116, 92)
CLOTH = (244, 242, 236)
CLOTH_D = (210, 206, 196)
TEAL = (40, 140, 140)
TEAL_D = (24, 96, 100)
APRON = (36, 50, 92)
APRON_D = (24, 34, 66)
NOODLE = (250, 226, 150)
PANTS = (60, 60, 68)
WOOD = (150, 104, 62)
WOOD_D = (110, 72, 40)
GETA = (120, 84, 52)
GETA_D = (84, 56, 34)


def build():
    skin = Skin(ID)
    add_standard_body(skin)
    # bandana knot and its two short tails
    skin.acc("knot", "head", [-0.9, 28.6, 4.45], [1.8, 1.8, 0.7], lowres=("up", "down", "east", "west"))
    skin.acc("tieR", "head", [-1.6, 24.8, 4.7], [1.25, 4, 0.25], faces=("north", "south"),
             pad=("north",), same={"south": "north"}, rotation=[18, 0, -14], pivot=[-1.0, 29.0, 4.8])
    skin.acc("tieL", "head", [0.35, 25.3, 4.7], [1.25, 4, 0.25], like="tieR", rotation=[22, 0, 12],
             pivot=[1.0, 29.0, 4.8])
    # the giant ladle, held upright in front of him
    skin.acc("handle", "rightArm", [-6.25, 11.0, -3.0], [0.5, 10, 0.5], lowres=SIDES + ("up", "down"))
    skin.acc("ladle", "rightArm", [-7.25, 20.5, -4.0], [2.5, 1.5, 2.5], lowres=("down",))
    h = add_sandals(skin)
    paint_head(skin)
    paint_gear(skin)
    paint_body(skin)
    paint_arms(skin)
    paint_legs(skin, h)
    paint_sandals(skin, GETA, GETA_D, SKIN, SKIN_D)
    return skin


def bandana(face, seed):
    cloth(face, CLOTH, seed, var=0.03, fold=0.04)
    face.fill(TEAL, face.row == face.h - 2)


def paint_head(skin):
    grey = hair_painter(HAIR, HAIR_D, HAIR_L)
    hair_head(skin, grey, 8000, SKIN, SKIN_D, [6] * 16, back_bottom=11)
    front = skin.face("head", "north")
    male_face(front, BROW, {"L": LASH, "W": WHITE, "D": EYE_D, "E": EYE, "H": EYE_L, "G": EYE_L},
              MOUTH, mouth_row=14, mouth_cols=(7, 8))
    # bushy brows and a neat moustache
    for c in (1, 14):
        front.set(7, c, BROW)
    rows(front, 12, 12, HAIR_D, (front.col >= 5) & (front.col <= 10))
    front.fill(HAIR_D, (front.row == 13) & ((front.col == 5) | (front.col == 10)))
    front.set(12, 7, HAIR)
    # bandana over the hat layer: covers the crown down to the brow
    for f in ("north", "east", "west", "south", "up"):
        face = skin.face("hat", f)
        m = np.ones((face.h, face.w), bool) if f == "up" else face.row <= 6
        old = face.rgba.copy()
        bandana(face, 8100 + len(f))
        if f != "up":
            face.rgba = np.where(m[..., None], face.rgba, old)
            face.fill(TEAL_D, face.row == 6)
    for face in skin.each("knot"):
        bandana(face, 8110 + face.w)
    for f in ("north",):
        tie = skin.face("tieR", f)
        cloth(tie, CLOTH, 8120, var=0.03, fold=0.06)
        tie.fill(CLOTH_D, tie.col == tie.w - 1)
        tie.fill(TEAL, tie.row == tie.h - 2)


def paint_gear(skin):
    for face in skin.each("handle"):
        face.fill(WOOD)
        face.fill(WOOD_D, face.row % 3 == 0)
    for face in skin.each("ladle"):
        face.fill(STEEL)
        face.shade(noise((face.h, face.w), 8200 + face.w, 0.03))
        face.fill(STEEL_L, face.row == 0)
        face.fill(STEEL_D, face.row == face.h - 1)
    top = skin.face("ladle", "up")
    top.fill((236, 214, 160))                    # broth
    top.fill(NOODLE, (top.row + top.col) % 2 == 0)
    top.fill(STEEL_L, (top.row == 0) | (top.col == 0) | (top.row == top.h - 1) | (top.col == top.w - 1))


def bowl(face, top, left):
    art = [
        ".S..S..S.",
        "..S..S..S",
        ".S..S..S.",
        "WWWWWWWWW",
        "WNNNNNNNW",
        ".WWWWWWW.",
        "..WWWWW..",
        "...WWW...",
    ]
    face.stamp(art, {"S": (170, 190, 220), "W": CLOTH, "N": NOODLE}, top=top, left=left)


def paint_body(skin):
    for f in SIDES + ("up", "down"):
        cloth(skin.face("body", f), CLOTH, 8300 + len(f), var=0.03, fold=0.04)
    front = skin.face("body", "north")
    # wrap-front coat: teal trim crossing to the left
    for r in range(0, 9):
        front.set(r, 4 + r // 1 if r < 4 else 7 + (r - 4) // 2, TEAL)
    for r in range(0, 10):
        c = 11 - r // 2
        front.set(r, c, TEAL)
        front.set(r, c + 1, TEAL_D)
    # navy apron from the chest down, with the stall's bowl on it
    apron = (front.row >= 9)
    cloth(front, APRON, 8310, var=0.04, fold=0.05, mask=apron)
    front.fill(APRON_D, (front.row == 9))
    bowl(front, 12, 3)
    for f in ("east", "west"):
        face = skin.face("body", f)
        rows(face, 18, 19, APRON_D)               # apron strings
    back = skin.face("body", "south")
    rows(back, 18, 19, APRON_D)
    back.fill(APRON_D, box(back, 17, 6, 20, 9))   # the bow
    for f in SIDES:
        rows(skin.face("body", f), 20, 23, PANTS, None if f != "north" else None)
    rows(front, 20, 23, APRON)
    for face in skin.each("jacket"):
        face.clear()
    jk = skin.face("jacket", "north")
    jk.fill(APRON_D, (jk.row == 9) & (jk.col >= 1) & (jk.col <= 14))


def paint_arms(skin):
    for arm, slv, seed in (("rightArm", "rightSleeve", 8400), ("leftArm", "leftSleeve", 8410)):
        for f in SIDES + ("up", "down"):
            skin_tone(skin.face(arm, f), SKIN, seed + len(f), var=0.02)
        for f in SIDES:
            face = skin.face(arm, f)
            cloth(face, CLOTH, seed + 5 + len(f), var=0.03, fold=0.04, mask=face.row <= 8)
        skin.face(arm, "up").fill(CLOTH)
        skin.face(arm, "down").fill(SKIN_D)
        for face in skin.each(slv):
            face.clear()
        for f in SIDES:
            face = skin.face(slv, f)
            rows(face, 8, 10, CLOTH_D)              # rolled-up sleeves
            rows(face, 10, 10, TEAL)


def paint_legs(skin, boot_h):
    for leg, pants, seed in (("rightLeg", "rightPants", 8500), ("leftLeg", "leftPants", 8510)):
        for f in SIDES:
            cloth(skin.face(leg, f), PANTS, seed + len(f), var=0.05, fold=0.06)
        skin.face(leg, "up").fill(PANTS)
        skin.face(leg, "down").fill(PANTS)
        for face in skin.each(pants):
            face.clear()
        # the apron hangs to the knee
        ap = skin.face(pants, "north")
        cloth(ap, APRON, seed + 9, var=0.04, fold=0.05, mask=ap.row <= 10)
        ap.fill(APRON_D, ap.row == 10)
        for f in SIDES:
            face = skin.face(pants, f)
            rows(face, 18, 19, (90, 90, 98))
    clear_under_shoes(skin, boot_h)
