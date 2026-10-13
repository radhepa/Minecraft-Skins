"""Frankie Stitches: green flat-top monster with neck bolts and stitched scars,
purple varsity jacket with cream sleeves, ripped jeans and lime sneakers.
"""

import numpy as np

from paintkit import (SIDES, add_footwear, box, clear_under_shoes, cloth,
                      copy_layer, hair, paint_sneakers, rows, skin_tone)
from skinlib import Skin, add_standard_body, noise

ID = "geometry.MidnightMischief.FrankieStitches"
TEXTURE = "frankie_stitches.png"
NAME = "Frankie Stitches"
LOC = "FrankieStitches"
REF_BOX = (180, 520, 420, 1000)  # crop of reference/midnight_mischief_lineup.webp
DETAILS = [
    ("face", "Flat-top + 3D neck bolts", {"yaw": 30, "pitch": 6, "dist": 42, "target": 26, "fov": 30}),
    ("back34", "Varsity jacket back", {"yaw": 205, "pitch": 10}),
    ("shoes", "Ripped jeans + lime sneakers", {"yaw": 35, "pitch": 14, "dist": 50, "target": 8, "fov": 30}),
]

GREEN = (148, 188, 96)
GREEN_D = (122, 160, 76)
GREEN_H = (172, 206, 118)
GREEN_X = (92, 124, 56)
HAIR = (38, 34, 42)
HAIR_D = (22, 20, 26)
HAIR_L = (60, 54, 66)
SCAR = (96, 44, 46)
PURPLE = (110, 52, 168)
PURPLE_D = (82, 36, 132)
PURPLE_H = (136, 74, 196)
CREAM = (234, 214, 196)
CREAM_D = (212, 190, 172)
CREAM_H = (246, 232, 216)
SHIRT = (40, 30, 38)
GOLD = (244, 168, 48)
DENIM = (48, 50, 62)
DENIM_D = (34, 36, 46)
DENIM_H = (66, 68, 82)
METAL = (176, 176, 188)
METAL_D = (112, 112, 126)

SNEAKERS = {"upper": (168, 204, 62), "hi": (198, 228, 98), "dark": (126, 162, 38),
            "lace": (244, 236, 220), "lace_dark": (214, 204, 186),
            "sole": (242, 230, 212), "sole_dark": (210, 196, 176)}


def build():
    skin = Skin(ID)
    add_standard_body(skin)
    for side, sx in (("Right", -1), ("Left", 1)):
        shaft_x = -5.5 if sx < 0 else 4
        cap_x = -6 if sx < 0 else 5.5
        skin.acc(f"bolt{side}", "head", [shaft_x, 24.5, -0.5], [1.5, 1, 1], lowres=("up", "down"))
        skin.acc(f"boltCap{side}", "head", [cap_x, 24.25, -0.75], [0.5, 1.5, 1.5])
    h = add_footwear(skin, height=3.0)
    paint_head(skin)
    paint_body(skin)
    paint_arms(skin)
    paint_legs(skin, h)
    paint_sneakers(skin, SNEAKERS, 1100)
    return skin


FRINGE = [4, 3, 5, 3, 4, 3, 3, 5, 4, 3, 4, 3, 5, 3, 4, 4]


def stitches(face, cells, cross):
    for r, c in cells:
        face.set(r, c, SCAR)
    for r, c in cross:
        face.set(r, c, SCAR)


def paint_head(skin):
    front = skin.face("head", "north")
    skin_tone(front, GREEN, 1000, var=0.04)
    hm = front.row <= np.array(FRINGE)[front.col]
    hair(front, HAIR, HAIR_D, HAIR_L, 1001, mask=hm)
    front.shade(np.where((front.row == np.array(FRINGE)[front.col] + 1) & ~hm, 0.8, 1.0))
    pal = {"B": (26, 24, 30), "E": GREEN_X, "W": (240, 240, 230), "I": (140, 70, 200),
           "i": (190, 130, 240), "P": (250, 240, 255)}
    front.stamp(["BBBB", "EEEE", "WIIW"], pal, top=7, left=2)       # droopy eye
    front.stamp(["BBBB", "WPIW", "WIiW"], pal, top=7, left=10)      # wide eye
    front.set(11, 3, GREEN_D)
    stitches(front, [(11, c) for c in range(1, 6)], [(10, 2), (12, 2), (10, 4), (12, 4)])
    front.stamp(["mmm", "..m"], {"m": (70, 96, 44)}, top=13, left=7)
    front.set(11, 8, GREEN_D)
    rows(front, 15, 15, GREEN_D, ~hm)

    for f in ("south", "up"):
        hair(skin.face("head", f), HAIR, HAIR_D, HAIR_L, 1010 + len(f))
    back = skin.face("head", "south")
    skin_tone_rows = back.row >= 11
    back.fill(GREEN_D, skin_tone_rows)
    for f in ("east", "west"):
        side = skin.face("head", f)
        skin_tone(side, GREEN, 1020 + len(f), var=0.04)
        hair(side, HAIR, HAIR_D, HAIR_L, 1021 + len(f), mask=side.row <= 4)
    east = skin.face("head", "east")
    # a big stitched "C" scar on the right side of the head
    c_scar = [(6, 9), (6, 8), (7, 7), (8, 6), (9, 6), (10, 6), (11, 7), (12, 8), (12, 9)]
    stitches(east, c_scar, [(5, 8), (7, 9), (9, 5), (9, 7), (13, 8), (11, 9)])
    skin_tone(skin.face("head", "down"), GREEN_D, 1030)

    hat = skin.face("hat", "north")
    hair(hat, HAIR, HAIR_D, HAIR_L, 1040)
    hat.clear(hat.row > np.array(FRINGE)[hat.col])
    for f in ("east", "west", "south", "up"):
        face = skin.face("hat", f)
        hair(face, HAIR, HAIR_D, HAIR_L, 1050 + len(f))
        if f != "up":
            face.clear(face.row > (5 if f != "south" else 10))
    skin.face("hat", "down").clear()

    for name in ("boltRight", "boltLeft", "boltCapRight", "boltCapLeft"):
        for face in skin.each(name):
            face.fill(METAL if "Cap" in name else METAL_D)
            face.shade(noise((face.h, face.w), 1060 + face.w, 0.05))
        cap = name.startswith("boltCap")
        if cap:
            outer = skin.face(name, "east" if "Right" in name else "west")
            outer.set(outer.h // 2, outer.w // 2, METAL_D)
            outer.set(outer.h // 2 - 1, outer.w // 2, METAL_D)


def varsity(face, seed):
    cloth(face, PURPLE, seed, var=0.06, fold=0.05, freq=0.9)


def ribbed(face, r0, r1):
    rows(face, r0, r1, PURPLE_D)
    rows(face, r0 + 1, r0 + 1, CREAM)
    face.fill(PURPLE, (face.row >= r0) & (face.row <= r1) & (face.row != r0 + 1) & (face.col % 2 == 0))


def paint_body(skin):
    front = skin.face("body", "north")
    varsity(front, 1100)
    center = (front.col >= 5) & (front.col <= 10)
    cloth(front, SHIRT, 1101, var=0.08, fold=0.0, mask=center)
    rows(front, 0, 1, GREEN_D, center & (front.col >= 6) & (front.col <= 9))
    rows(front, 0, 0, GREEN_X, center & (front.col >= 6) & (front.col <= 9))
    ribbed(front, 20, 23)
    front.fill(SHIRT, center & (front.row >= 20))
    for r in range(2, 20, 3):
        front.set(r, 4, CREAM)
        front.set(r, 11, CREAM)
    rows(front, 0, 1, CREAM, ~center & ((front.col == 3) | (front.col == 12) | (front.col == 4) | (front.col == 11)))
    moon = [".GG.", "G...", "G...", "G...", ".GG."]
    front.stamp(moon, {"G": GOLD}, top=3, left=12)
    front.set(4, 13, (210, 130, 30))
    front.stamp(["CC", ".C"], {"C": CREAM}, top=12, left=1)          # little patch
    for f in ("east", "west", "south"):
        face = skin.face("body", f)
        varsity(face, 1110 + len(f))
        ribbed(face, 20, 23)
    back = skin.face("body", "south")
    # big varsity "M" for Midnight
    m = ["C...C", "CC.CC", "C.C.C", "C...C", "C...C"]
    back.stamp(m, {"C": CREAM}, top=6, left=5)
    back.stamp(["P...P", "PP.PP", "P.P.P", "P...P", "P...P"], {"P": GOLD}, top=7, left=6)
    back.stamp(m, {"C": CREAM}, top=6, left=5)
    varsity(skin.face("body", "up"), 1120)
    varsity(skin.face("body", "down"), 1121)
    copy_layer(skin, "body", "jacket")
    skin.face("jacket", "north").clear(center)
    skin.face("jacket", "up").clear()
    jb = skin.face("jacket", "down")
    jb.clear((jb.col >= 5) & (jb.col <= 10))


def leather(face, seed):
    cloth(face, CREAM, seed, var=0.035, fold=0.05, freq=0.8)


def paint_arms(skin):
    for arm, slv, outer, seed in (("rightArm", "rightSleeve", "east", 1200),
                                  ("leftArm", "leftSleeve", "west", 1210)):
        for f in SIDES:
            face = skin.face(arm, f)
            leather(face, seed + len(f))
            rows(face, 14, 14, PURPLE)
            rows(face, 15, 15, CREAM)
            rows(face, 16, 16, PURPLE)
            ribbed(face, 17, 19)
            rows(face, 18, 18, PURPLE_D)
            hand = face.row >= 20
            face.fill(GREEN, hand)
            face.shade(np.where(hand, noise((24, 8), seed + 3, 0.04), 1.0))
            face.shade(np.where(face.row == 20, 0.85, 1.0))
        o = skin.face(arm, outer)
        stitches(o, [(5, c) for c in range(1, 7)], [(4, 2), (6, 2), (4, 5), (6, 5)])
        front = skin.face(arm, "north")
        front.stamp(["P.P", ".P.", "P.P"], {"P": PURPLE}, top=8, left=2 if arm == "rightArm" else 3)
        leather(skin.face(arm, "up"), seed + 9)
        skin_tone(skin.face(arm, "down"), GREEN_D, seed + 10)
        copy_layer(skin, arm, slv)
        for f in SIDES:
            skin.face(slv, f).clear(skin.face(slv, f).row >= 20)
        skin.face(slv, "down").clear()


def paint_legs(skin, shoe_h):
    for leg, pants, outer, seed in (("rightLeg", "rightPants", "east", 1300),
                                    ("leftLeg", "leftPants", "west", 1310)):
        rips = {"north": (9, 2, 11, 5) if leg == "rightLeg" else (5, 3, 8, 5),
                outer: (13, 2, 15, 4)}
        for f in SIDES:
            face = skin.face(leg, f)
            cloth(face, DENIM, seed + len(f), var=0.09, fold=0.07, freq=0.8)
            face.fill(DENIM_H, (face.row % 6 == 2) & (face.col % 3 == 1))
            if f in rips:
                r0, c0, r1, c1 = rips[f]
                hole = box(face, r0, c0, r1, c1)
                hole &= ~(((face.row == r0) | (face.row == r1)) & ((face.col == c0) | (face.col == c1)))
                face.fill(GREEN, hole)
                face.fill(GREEN_D, hole & (face.row == r0))
                face.fill(GREEN_H, hole & (face.row == r0 + 1) & (face.col == c0 + 1))
                for c in range(c0, c1 + 1):
                    if c % 2 == 0:
                        face.set(r0 - 1, c, (200, 202, 210))
                    if c % 2 == 1:
                        face.set(r1 + 1, c, DENIM_H)
        skin.face(leg, "up").fill(DENIM_D)
        skin.face(leg, "down").fill(DENIM_D)
        # frayed threads over the rips stand out on the overlay
        for f in SIDES:
            face = skin.face(pants, f)
            face.clear()
            if f in rips:
                r0, c0, r1, c1 = rips[f]
                for c in range(c0, c1 + 1, 2):
                    face.set(r0 - 1, c, (220, 222, 230))
        skin.face(pants, "up").clear()
        skin.face(pants, "down").clear()
    clear_under_shoes(skin, shoe_h)
