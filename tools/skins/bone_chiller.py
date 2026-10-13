"""Bone Chiller: grinning skull with glowing cyan eye sockets under a black
hood, skeleton-print hoodie and pants, cyan cuffs and sneakers.
"""

import numpy as np

from paintkit import (SIDES, add_footwear, box, clear_under_shoes, cloth,
                      copy_layer, paint_sneakers, rows)
from skinlib import Skin, add_standard_body, noise

ID = "geometry.MidnightMischief.BoneChiller"
TEXTURE = "bone_chiller.png"
NAME = "Bone Chiller"
LOC = "BoneChiller"
REF_BOX = (1140, 520, 1380, 1000)  # crop of reference/midnight_mischief_lineup.webp
DETAILS = [
    ("face", "Glowing skull + hood", {"yaw": 24, "pitch": 8, "dist": 42, "target": 26, "fov": 30}),
    ("back34", "Spine print + 3D hood", {"yaw": 200, "pitch": 12}),
    ("shoes", "Bone legs + cyan sneakers", {"yaw": 35, "pitch": 12, "dist": 52, "target": 8, "fov": 30}),
]

BONE = (238, 224, 206)
BONE_D = (214, 198, 180)
BONE_H = (250, 242, 230)
SOCKET = (22, 18, 26)
GLOW_C = (196, 254, 255)
GLOW = (80, 224, 244)
GLOW_R = (34, 156, 196)
BK = (32, 26, 38)
BK_D = (20, 16, 26)
BK_H = (48, 40, 56)
CYAN = (72, 212, 234)
CYAN_D = (40, 166, 198)
CYAN_H = (156, 240, 252)

SNEAKERS = {"upper": (36, 30, 42), "hi": (60, 52, 68), "dark": (22, 18, 28),
            "lace": CYAN, "lace_dark": CYAN_D, "sole": CYAN, "sole_dark": BONE}


def build():
    skin = Skin(ID)
    add_standard_body(skin)
    skin.acc("hoodPeak", "head", [-4.5, 32.5, -4.5], [9, 0.75, 9.5], lowres=("up", "down", "south"))
    skin.acc("hoodBack", "body", [-3.5, 21, 2.25], [7, 3, 1.25], faces=("south", "east", "west", "down"))
    h = add_footwear(skin, height=3.0)
    paint_head(skin)
    paint_body(skin)
    paint_arms(skin)
    paint_legs(skin, h)
    paint_sneakers(skin, SNEAKERS, 2300)
    return skin


def bone(face, seed):
    face.fill(BONE)
    face.shade(noise((face.h, face.w), seed, 0.03))


def black(face, seed):
    cloth(face, BK, seed, var=0.1, fold=0.05, freq=1.1)


def paint_head(skin):
    for f in SIDES + ("up", "down"):
        bone(skin.face("head", f), 2200 + len(f))
    front = skin.face("head", "north")
    sock = [
        "KKKK",
        "KgcK",
        "KccK",
        "KrrK",
    ]
    pal = {"K": SOCKET, "c": GLOW, "g": GLOW_C, "r": GLOW_R}
    front.stamp(sock, pal, top=6, left=2)
    front.stamp(sock, pal, top=6, left=10, mirror=True)
    for c in (2, 3, 4, 5, 10, 11, 12, 13):
        front.set(5, c, BONE_D)
    front.stamp(["KK", "K."], {"K": SOCKET}, top=10, left=7)
    front.set(11, 8, BONE_D)
    for c in range(4, 12):
        front.set(13, c, SOCKET if c % 2 == 0 else BONE_D)
        front.set(14, c, SOCKET if c % 2 == 0 else BONE)
    rows(front, 12, 12, BONE_D, (front.col >= 4) & (front.col <= 11))
    # hollow cheeks give the jaw its shape
    jaw = (front.row >= 12) & ((front.col <= 2 - (15 - front.row) // 2 + 1) | (front.col >= 13 + (15 - front.row) // 2 - 1))
    front.fill(SOCKET, jaw & (front.row >= 13))
    front.fill(BONE_H, box(front, 1, 3, 2, 6))

    # the hood: black fabric over top, back and sides, open at the face
    for f in ("east", "west", "south", "up"):
        black(skin.face("hat", f), 2210 + len(f))
    hood = skin.face("hat", "north")
    black(hood, 2215)
    hood.clear(~((hood.row <= 1) | (hood.col == 0) | (hood.col == 15)))
    for f, front_first in (("east", False), ("west", True)):
        side = skin.face("hat", f)
        k = side.col if front_first else 15 - side.col
        side.fill(BK_H, k == 0)
    skin.face("hat", "down").clear()
    for face in skin.each("hoodPeak"):
        black(face, 2220 + face.w)
    peak = skin.face("hoodPeak", "north")
    rows(peak, 0, 0, BK_H)
    for face in skin.each("hoodBack"):
        black(face, 2230 + face.w)
    hb = skin.face("hoodBack", "south")
    rows(hb, 0, 0, BK_H)
    hb.fill(BK_D, hb.col == hb.w // 2)


def rib_cage(face):
    """Cream skeleton print on a 16x24 torso front."""
    for r in range(2, 16):
        face.set(r, 7, BONE)
        face.set(r, 8, BONE_D if r % 3 == 0 else BONE)
    for i, r in enumerate((3, 6, 9, 12)):
        span = 5 - (i // 2)
        for c in range(7 - span, 7):
            face.set(r, c, BONE)
            face.set(r + 1, c, BONE_D)
        for c in range(9, 9 + span):
            face.set(r, c, BONE)
            face.set(r + 1, c, BONE_D)
        face.set(r + 1, 7 - span, BONE)
        face.set(r + 2, 7 - span, BONE_D)
        face.set(r + 1, 8 + span, BONE)
        face.set(r + 2, 8 + span, BONE_D)
    pelvis = [
        "BBB......BBB",
        ".BBBB..BBBB.",
        "..BBBBBBBB..",
        "...BB..BB...",
    ]
    face.stamp(pelvis, {"B": BONE}, top=17, left=2)
    face.set(18, 7, BONE_D)
    face.set(18, 8, BONE_D)


def paint_body(skin):
    front = skin.face("body", "north")
    black(front, 2240)
    rib_cage(front)
    rows(front, 22, 23, BK_D)
    back = skin.face("body", "south")
    black(back, 2241)
    for r in range(1, 21):
        if r % 3 != 0:
            back.set(r, 7, BONE)
            back.set(r, 8, BONE_D)
    for r in (4, 5, 6):
        for c in (3, 4, 11, 12):
            back.set(r, c, BONE_D if r == 6 else BONE)
    rows(back, 22, 23, BK_D)
    for f in ("east", "west"):
        face = skin.face("body", f)
        black(face, 2242 + len(f))
        for r in (4, 7, 10):
            rows(face, r, r, BONE_D, (face.col >= 2) & (face.col <= 5))
        rows(face, 22, 23, BK_D)
    black(skin.face("body", "up"), 2246)
    black(skin.face("body", "down"), 2247)
    copy_layer(skin, "body", "jacket")
    skin.face("jacket", "up").clear()


def long_bone(face, c0, r0, r1, width=2):
    """Vertical bone with knobbly ends, c0 = left column of the shaft."""
    for r in range(r0 + 2, r1 - 1):
        for c in range(c0, c0 + width):
            face.set(r, c, BONE if c == c0 else BONE_D)
    for r in (r0, r0 + 1, r1 - 1, r1):
        for c in range(c0 - 1, c0 + width + 1):
            face.set(r, c, BONE)
    face.set(r0, c0 + width // 2 - (1 if width == 2 else 0), BK)
    face.set(r1, c0 + width // 2 - (1 if width == 2 else 0), BK)


def paint_arms(skin):
    for arm, slv, outer, seed in (("rightArm", "rightSleeve", "east", 2300),
                                  ("leftArm", "leftSleeve", "west", 2310)):
        for f in SIDES:
            face = skin.face(arm, f)
            black(face, seed + len(f))
            if f in ("north", outer):
                long_bone(face, 3, 1, 14)
            rows(face, 17, 19, CYAN)
            rows(face, 17, 17, CYAN_H)
            rows(face, 19, 19, CYAN_D)
            hand = face.row >= 20
            face.fill(BONE, hand)
            face.fill(BONE_D, hand & (face.col % 2 == 1) & (face.row >= 22))
            face.fill(SOCKET, hand & (face.col % 2 == 1) & (face.row == 23))
        black(skin.face(arm, "up"), seed + 7)
        bone(skin.face(arm, "down"), seed + 8)
        copy_layer(skin, arm, slv)
        for f in SIDES:
            skin.face(slv, f).clear(skin.face(slv, f).row >= 20)
        skin.face(slv, "down").clear()


def paint_legs(skin, shoe_h):
    for leg, pants, outer, seed in (("rightLeg", "rightPants", "east", 2400),
                                    ("leftLeg", "leftPants", "west", 2410)):
        for f in SIDES:
            face = skin.face(leg, f)
            black(face, seed + len(f))
            if f == "north":
                long_bone(face, 3, 1, 10)
                face.fill(BONE, box(face, 11, 3, 12, 4))
                for r in range(13, 18):
                    face.set(r, 3, BONE)
                    face.set(r, 4, BONE_D)
                face.fill(BONE, box(face, 17, 2, 17, 5))
            elif f == outer:
                long_bone(face, 4, 2, 9, width=1)
                long_bone(face, 4, 12, 17, width=1)
        skin.face(leg, "up").fill(BK_D)
        skin.face(leg, "down").fill(BK_D)
        for face in skin.each(pants):
            face.clear()
    clear_under_shoes(skin, shoe_h)
