"""Velvet Vampire: pale count with red eyes and a widow's peak, crimson
frock coat with gold trim, a tall standing collar, ruffled jabot and
buckled boots.
"""

import numpy as np

from paintkit import (SIDES, add_footwear, box, clear_under_shoes, cloth,
                      hair, paint_boots, rows, skin_tone)
from skinlib import Skin, add_standard_body, noise

ID = "geometry.MidnightMischief.VelvetVampire"
TEXTURE = "velvet_vampire.png"
NAME = "Velvet Vampire"
LOC = "VelvetVampire"
REF_BOX = (1130, 110, 1390, 540)  # crop of reference/midnight_mischief_lineup.webp
DETAILS = [
    ("face", "Red eyes + fangs", {"yaw": 18, "pitch": 6, "dist": 42, "target": 26, "fov": 30}),
    ("back34", "3D standing collar", {"yaw": 215, "pitch": 14}),
    ("jabot", "Jabot + gold cuffs", {"yaw": -30, "pitch": 6, "dist": 52, "target": 19, "fov": 30}),
]

PALE = (234, 228, 238)
PALE_D = (212, 204, 222)
PALE_H = (248, 245, 252)
HAIR = (50, 28, 44)
HAIR_D = (30, 16, 26)
HAIR_L = (74, 42, 64)
HAIR_S = (104, 62, 90)
RED = (132, 22, 36)
RED_D = (96, 14, 28)
RED_H = (160, 38, 52)
RED_IN = (70, 10, 22)
GOLD = (240, 178, 56)
GOLD_D = (190, 124, 30)
VEST = (40, 30, 42)
VEST_D = (26, 20, 30)
VEST_H = (58, 44, 60)
JABOT = (240, 230, 212)
JABOT_D = (214, 200, 180)
PANTS = (34, 26, 36)
PANTS_D = (24, 18, 26)

BOOTS = {"upper": (36, 28, 38), "hi": (64, 52, 66), "dark": (22, 16, 24),
         "strap": GOLD, "strap_dark": GOLD_D, "sole": (28, 22, 30), "sole_dark": (16, 12, 18)}


def build():
    skin = Skin(ID)
    add_standard_body(skin)
    skin.acc("collarBack", "body", [-5, 23.5, 4.5], [10, 5, 0.75], lowres=("north", "up", "down", "east", "west"))
    skin.acc("collarBase", "body", [-5, 23, 2.25], [10, 1, 3], faces=("east", "west", "up", "down"), px=1)
    skin.acc("collarRight", "body", [-5.75, 24.25, 0], [0.75, 4, 5.25], lowres=("west", "up", "down", "north", "south"))
    skin.acc("collarLeft", "body", [5, 24.25, 0], [0.75, 4, 5.25], lowres=("east", "up", "down", "north", "south"))
    skin.acc("jabot", "body", [-1.5, 18.5, -3], [3, 3.5, 0.75])
    skin.acc("rightCuff", "rightArm", [-8, 14, -2], [4, 2.5, 4], inflate=0.5, lowres=("up", "down"))
    skin.acc("leftCuff", "leftArm", [4, 14, -2], [4, 2.5, 4], inflate=0.5, lowres=("up", "down"))
    h = add_footwear(skin, height=5.0, length=5.5, toe=1.0, tongue=False)
    paint_head(skin)
    paint_collar(skin)
    paint_body(skin)
    paint_arms(skin)
    paint_legs(skin, h)
    paint_boots(skin, BOOTS, 900, straps=(2, 6))
    return skin


HAIRLINE = [7, 6, 4, 3, 3, 3, 3, 5, 5, 3, 3, 3, 3, 4, 6, 7]


def paint_head(skin):
    front = skin.face("head", "north")
    skin_tone(front, PALE, 800)
    hm = front.row <= np.array(HAIRLINE)[front.col]
    hair(front, HAIR, HAIR_D, HAIR_L, 801, mask=hm, shine=HAIR_S)
    front.shade(np.where((front.row == np.array(HAIRLINE)[front.col] + 1) & ~hm, 0.9, 1.0))
    brow = (36, 18, 28)
    for r, c in ((6, 3), (6, 4), (6, 5), (6, 12), (6, 11), (6, 10)):
        front.set(r, c, brow)
    eye = ["EEEE", "WRRW", "WrRW"]
    pal = {"E": (40, 20, 30), "W": (250, 246, 252), "R": (200, 18, 30), "r": (255, 92, 92)}
    front.stamp(eye, pal, top=8, left=3)
    front.stamp(eye, pal, top=8, left=9, mirror=True)
    for r in (11, 12):
        front.set(r, 7 if r == 11 else 8, PALE_D)
    front.stamp([".mmmm."], {"m": (150, 120, 140)}, top=13, left=5)
    front.set(14, 6, (255, 255, 255))
    front.set(14, 9, (255, 255, 255))
    for c in (2, 3, 12, 13):
        front.set(12, c, PALE_D)
    for f in ("east", "west", "south", "up"):
        hair(skin.face("head", f), HAIR, HAIR_D, HAIR_L, 810 + len(f), shine=HAIR_S)
    for f, a, b in (("east", 9, 15), ("west", 0, 6)):
        side = skin.face("head", f)
        skin_tone(side, PALE, 820, var=0.02)
        hair(side, HAIR, HAIR_D, HAIR_L, 821 + a, mask=~box(side, 7, a, 15, b), shine=HAIR_S)
        ear = a + 2 if f == "east" else b - 3
        side.fill(PALE_D, box(side, 9, ear, 11, ear + 1))
    skin_tone(skin.face("head", "down"), PALE_D, 830)

    hat = skin.face("hat", "north")
    hair(hat, HAIR, HAIR_D, HAIR_L, 840, shine=HAIR_S)
    hat.clear(hat.row > np.array(HAIRLINE)[hat.col] - 1)
    hat.clear((hat.row == np.array(HAIRLINE)[hat.col] - 1) & (hat.col % 3 == 0))
    for f in ("east", "west", "south", "up"):
        face = skin.face("hat", f)
        hair(face, HAIR, HAIR_D, HAIR_L, 850 + len(f), shine=HAIR_S)
        if f in ("east", "west"):
            a, b = (9, 15) if f == "east" else (0, 6)
            face.clear(box(face, 6, a, 15, b))
        if f == "south":
            face.clear((face.row >= 14) & (face.col % 2 == 0))
    skin.face("hat", "down").clear()


def velvet(face, seed, base=RED):
    cloth(face, base, seed, var=0.06, fold=0.06, freq=0.8)


def paint_collar(skin):
    for name in ("collarBack", "collarBase", "collarRight", "collarLeft"):
        for face in skin.each(name):
            velvet(face, 860 + face.w)
    # dark lining faces the head; gold piping on the outer rim
    skin.face("collarBack", "north").fill(RED_IN)
    skin.face("collarRight", "west").fill(RED_IN)
    skin.face("collarLeft", "east").fill(RED_IN)
    for name in ("collarBack", "collarRight", "collarLeft"):
        skin.face(name, "up").fill(GOLD)
    back = skin.face("collarBack", "south")
    rows(back, 0, 0, GOLD)
    for name, f in (("collarRight", "east"), ("collarLeft", "west")):
        face = skin.face(name, f)
        rows(face, 0, 0, GOLD)
        face.fill(GOLD, face.col == (face.w - 1 if f == "east" else 0))
    jab = skin.face("jabot", "north")
    jab.fill(JABOT)
    jab.fill(JABOT_D, (jab.row % 2 == 1) & ((jab.col + jab.row // 2) % 2 == 0))
    jab.clear((jab.row == jab.h - 1) & ((jab.col == 0) | (jab.col == jab.w - 1)))
    for f in ("east", "west", "up", "down", "south"):
        skin.face("jabot", f).fill(JABOT_D)


def paint_body(skin):
    for layer, seed in (("body", 870), ("jacket", 880)):
        front = skin.face(layer, "north")
        velvet(front, seed)
        center = (front.col >= 5) & (front.col <= 10)
        cloth(front, VEST, seed + 1, var=0.06, fold=0.0, mask=center)
        front.fill(VEST_H, center & ((front.col == 5) | (front.col == 10)))
        for r in (10, 13, 16, 19):
            front.set(r, 6, GOLD)
            front.set(r, 9, GOLD)
            front.set(r + 1, 6, GOLD_D)
            front.set(r + 1, 9, GOLD_D)
        cravat = center & (front.row <= 7)
        front.fill(JABOT, cravat)
        front.fill(JABOT_D, cravat & (front.row % 2 == 1) & ((front.col + front.row // 2) % 2 == 0))
        # gold trim down the coat edges, notched lapels at the top
        for c in (4, 11):
            front.fill(GOLD, front.col == c)
        for r, c in ((0, 3), (1, 3), (2, 2), (3, 2), (4, 3), (0, 12), (1, 12), (2, 13), (3, 13), (4, 12)):
            front.set(r, c, GOLD)
        front.fill(RED_H, box(front, 0, 0, 3, 1) | box(front, 0, 14, 3, 15))
        rows(front, 23, 23, GOLD, ~center)
        if layer == "jacket":
            front.clear(center)
        for f in ("east", "west", "south"):
            face = skin.face(layer, f)
            velvet(face, seed + len(f))
            rows(face, 23, 23, GOLD)
            if f == "south":
                face.fill(RED_D, (face.col == 7) | (face.col == 8))
                for r in (14, 15):
                    face.set(r, 5, GOLD)
                    face.set(r, 10, GOLD)
        velvet(skin.face(layer, "up"), seed + 9)
        bottom = skin.face(layer, "down")
        velvet(bottom, seed + 10, RED_D)
        if layer == "jacket":
            bottom.clear((bottom.col >= 5) & (bottom.col <= 10))


def paint_arms(skin):
    for arm, slv, cuff, seed in (("rightArm", "rightSleeve", "rightCuff", 900),
                                 ("leftArm", "leftSleeve", "leftCuff", 910)):
        for layer, s in ((arm, seed), (slv, seed + 5)):
            for f in SIDES:
                face = skin.face(layer, f)
                velvet(face, s + len(f))
                hand = face.row >= 20
                face.fill(PALE, hand)
                face.shade(np.where(hand, noise((24, 8), s + 3, 0.02), 1.0))
                face.shade(np.where(face.row == 20, 0.88, 1.0))
                if layer == slv:
                    face.clear(face.row >= 15)
            velvet(skin.face(layer, "up"), s + 9)
            if layer == arm:
                skin_tone(skin.face(layer, "down"), PALE_D, s + 10)
            else:
                skin.face(layer, "down").clear()
        for f in SIDES:
            face = skin.face(cuff, f)
            velvet(face, seed + 20 + len(f))
            rows(face, 0, 0, GOLD)
            rows(face, face.h - 1, face.h - 1, GOLD)
        velvet(skin.face(cuff, "up"), seed + 30)
        b = skin.face(cuff, "down")
        b.fill(GOLD_D)
        b.clear(box(b, 1, 1, b.h - 2, b.w - 2))


def paint_legs(skin, boot_h):
    for leg, pants, outer, seed in (("rightLeg", "rightPants", "east", 920),
                                    ("leftLeg", "leftPants", "west", 930)):
        for f in SIDES:
            face = skin.face(leg, f)
            cloth(face, PANTS, seed + len(f), var=0.08, fold=0.05, freq=0.9)
            face.fill(PANTS_D, face.col == (3 if f in ("north", "south") else 4))
        skin.face(leg, "up").fill(PANTS_D)
        skin.face(leg, "down").fill(PANTS_D)
        # frock-coat tails hang round the outside and back of each leg
        for f in SIDES:
            face = skin.face(pants, f)
            velvet(face, seed + 20 + len(f))
            rows(face, 13, 13, GOLD)
            face.clear(face.row > 13)
            if f == "north":
                keep = face.col <= 1 if leg == "rightLeg" else face.col >= 6
                edge = face.col == (2 if leg == "rightLeg" else 5)
                face.fill(GOLD, edge & (face.row <= 13))
                face.clear(~keep & ~edge)
            elif f != outer and f != "south":
                face.clear()
        skin.face(pants, "up").clear()
        skin.face(pants, "down").clear()
    clear_under_shoes(skin, boot_h)
