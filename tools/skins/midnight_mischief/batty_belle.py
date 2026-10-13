"""Batty Belle: pale vampire kid with magenta eyes and tiny fangs, a bat-eared
hood, scalloped bat wings on the back, bat-emblem hoodie and purple sneakers.
"""

import numpy as np

from paintkit import (SIDES, add_footwear, box, clear_under_shoes, cloth,
                      copy_layer, hair, paint_sneakers, rows, skin_tone)
from skinlib import Skin, add_standard_body, noise

ID = "geometry.MidnightMischief.BattyBelle"
TEXTURE = "batty_belle.png"
NAME = "Batty Belle"
LOC = "BattyBelle"
DETAILS = [
    ("face", "Bat-ear hood + fangs", {"yaw": 22, "pitch": 8, "dist": 46, "target": 27, "fov": 30}),
    ("back34", "Scalloped 3D bat wings", {"yaw": 160, "pitch": 10}),
    ("wings", "Wings from the front", {"yaw": 0, "pitch": 4, "dist": 70, "target": 18, "fov": 30}),
]

SKIN = (238, 220, 216)
SKIN_D = (218, 196, 196)
HAIR = (46, 30, 60)
HAIR_D = (28, 18, 40)
HAIR_L = (72, 50, 94)
HOOD = (60, 34, 84)
HOOD_D = (42, 24, 62)
HOOD_H = (82, 50, 112)
LINING = (150, 100, 192)
EAR_IN = (196, 122, 182)
WING = (92, 54, 128)
WING_D = (70, 40, 102)
WING_BONE = (30, 18, 42)
LILAC = (206, 168, 236)
BAT = (24, 16, 32)
LEGGING = (34, 28, 44)
LEGGING_H = (50, 42, 62)

SNEAKERS = {"upper": (112, 62, 162), "hi": (144, 92, 194), "dark": (72, 38, 112),
            "lace": LILAC, "lace_dark": (170, 130, 204),
            "sole": (44, 36, 54), "sole_dark": (28, 22, 36)}


def build():
    skin = Skin(ID, slim=True)
    add_standard_body(skin)
    for side, x_base, x_tip in (("Right", -4.75, -4.75), ("Left", 1.25, 3.25)):
        skin.acc(f"ear{side}", "head", [x_base, 32.25, -1.5], [3.5, 1.5, 1], lowres=("up", "down"))
        skin.acc(f"earTip{side}", "head", [x_tip, 33.75, -1.25], [1.5, 2, 0.75], lowres=("up", "down"))
    skin.acc("wingRight", "body", [-11, 13, 2.75], [9, 8, 0.5], lowres=("east", "west", "up", "down"))
    skin.acc("wingLeft", "body", [2, 13, 2.75], [9, 8, 0.5], lowres=("east", "west", "up", "down"))
    h = add_footwear(skin, height=3.0)
    paint_head(skin)
    paint_wings(skin)
    paint_body(skin)
    paint_arms(skin)
    paint_legs(skin, h)
    paint_sneakers(skin, SNEAKERS, 4300)
    return skin


BANGS = [15, 15, 5, 4, 3, 4, 5, 4, 3, 4, 5, 4, 3, 5, 15, 15]


def paint_head(skin):
    front = skin.face("head", "north")
    skin_tone(front, SKIN, 4100, var=0.02)
    hm = front.row <= np.array(BANGS)[front.col]
    hair(front, HAIR, HAIR_D, HAIR_L, 4101, mask=hm)
    front.shade(np.where((front.row == np.array(BANGS)[front.col] + 1) & ~hm, 0.9, 1.0))
    eye = ["EEE.", "WMhE", "WMME"]
    pal = {"E": (30, 18, 34), "W": (252, 246, 252), "M": (214, 38, 112), "h": (255, 170, 210)}
    front.stamp(eye, pal, top=7, left=2)
    front.stamp(eye, pal, top=7, left=10, mirror=True)
    front.stamp(["mmmm", "F..F"], {"m": (150, 70, 96), "F": (255, 255, 255)}, top=12, left=6)
    for c in (2, 3, 12, 13):
        front.set(11, c, (240, 160, 186))
    for f in ("east", "west", "south", "up"):
        hair(skin.face("head", f), HAIR, HAIR_D, HAIR_L, 4110 + len(f))
    skin_tone(skin.face("head", "down"), SKIN_D, 4120)

    # hat layer is the hood, lined in lilac round the face
    for f in ("east", "west", "south", "up"):
        cloth(skin.face("hat", f), HOOD, 4130 + len(f), var=0.05, fold=0.04)
    hood = skin.face("hat", "north")
    cloth(hood, HOOD, 4135, var=0.05, fold=0.0)
    rim = (hood.row <= 1) | (hood.col <= 1) | (hood.col >= 14)
    hood.fill(LINING, rim & ((hood.row == 1) | (hood.col == 1) | (hood.col == 14)) & (hood.row >= 1))
    hood.clear(~rim)
    skin.face("hat", "down").clear()
    for side in ("Right", "Left"):
        for name in (f"ear{side}", f"earTip{side}"):
            for face in skin.each(name):
                cloth(face, HOOD, 4140 + face.w, var=0.05, fold=0.0)
        ear = skin.face(f"ear{side}", "north")
        ear.fill(EAR_IN, box(ear, 1, 1, ear.h - 1, ear.w - 2))
        tip = skin.face(f"earTip{side}", "north")
        tip.fill(EAR_IN, (tip.row == tip.h - 1) & (tip.col == tip.w // 2))


def paint_wings(skin):
    for side in ("Right", "Left"):
        name = f"wing{side}"
        for face in skin.each(name):
            face.fill(WING_BONE)
        # thin membrane: only the top edge shows, the cut-out edges stay open
        for f in ("east", "west", "down"):
            skin.face(name, f).clear()
        for f in ("north", "south"):
            face = skin.face(name, f)
            face.fill(WING)
            face.shade(noise((face.h, face.w), 4150 + len(f), 0.04))
            # distance from the body: tip of the wing is the far end
            outer_is_right = (side == "Left") == (f == "north")
            d = face.col if outer_is_right else face.w - 1 - face.col
            # three scallops along the lower edge
            seg = face.w / 3
            local = (d % seg) / seg
            # lower edge scallops up between the finger tips, and the whole
            # wing tapers up toward its tip
            scallop = face.h - 1 - np.round(5 * np.sin(np.pi * local)).astype(int) - (d * 4 // face.w)
            face.clear(face.row > scallop)
            # finger bones: straight lines from the shoulder corner to each tip
            for k in range(1, 4):
                tip_d = k * seg - 0.5
                tip_r = face.h - 1 - int(round(tip_d)) * 4 // face.w
                for t in np.linspace(0, 1, 60):
                    rr = int(round(t * tip_r))
                    cc = int(round(t * tip_d))
                    col = cc if outer_is_right else face.w - 1 - cc
                    if 0 <= rr < face.h and 0 <= col < face.w:
                        face.set(rr, col, WING_BONE)
            rows(face, 0, 0, WING_BONE)
            face.fill(WING_D, (face.row == scallop) & (face.row > 0))
            face.clear(face.row > scallop)


def paint_body(skin):
    front = skin.face("body", "north")
    cloth(front, HOOD, 4200, var=0.05)
    bat = [
        "B....B.B....B",
        "BB...BBB...BB",
        "BBBB.BBB.BBBB",
        "BBBBBBBBBBBBB",
        ".BBBBBBBBBBB.",
        "..BB..B..BB..",
        "...B.....B...",
    ]
    front.stamp(bat, {"B": BAT}, top=8, left=1)
    front.set(10, 6, (214, 38, 112))
    front.set(10, 8, (214, 38, 112))
    front.set(9, 6, BAT)
    for c in (5, 10):
        rows(front, 1, 5, LILAC, front.col == c)
    rows(front, 0, 0, HOOD_D, (front.col >= 4) & (front.col <= 11))
    rows(front, 22, 23, HOOD_D)
    front.fill(HOOD, (front.row >= 22) & (front.col % 2 == 0))
    for f in ("east", "west", "south"):
        face = skin.face("body", f)
        cloth(face, HOOD, 4210 + len(f), var=0.05)
        rows(face, 22, 23, HOOD_D)
        face.fill(HOOD, (face.row >= 22) & (face.col % 2 == 0))
    cloth(skin.face("body", "up"), HOOD_D, 4220)
    cloth(skin.face("body", "down"), HOOD_D, 4221)
    copy_layer(skin, "body", "jacket")
    skin.face("jacket", "up").clear()


def paint_arms(skin):
    for arm, slv, seed in (("rightArm", "rightSleeve", 4300), ("leftArm", "leftSleeve", 4310)):
        for f in SIDES:
            face = skin.face(arm, f)
            cloth(face, HOOD, seed + len(f), var=0.05)
            rows(face, 16, 18, LILAC)
            rows(face, 18, 18, (176, 136, 210))
            hand = face.row >= 19
            face.fill(SKIN, hand)
            face.shade(np.where(face.row == 19, 0.88, 1.0))
        cloth(skin.face(arm, "up"), HOOD, seed + 7)
        skin_tone(skin.face(arm, "down"), SKIN_D, seed + 8)
        copy_layer(skin, arm, slv)
        for f in SIDES:
            skin.face(slv, f).clear(skin.face(slv, f).row >= 19)
        skin.face(slv, "down").clear()


def paint_legs(skin, shoe_h):
    for leg, pants, outer, seed in (("rightLeg", "rightPants", "east", 4400),
                                    ("leftLeg", "leftPants", "west", 4410)):
        for f in SIDES:
            face = skin.face(leg, f)
            cloth(face, LEGGING, seed + len(f), var=0.06, fold=0.05)
            if f == outer:
                face.fill((112, 62, 162), (face.col == 3) | (face.col == 4))
            face.fill(LEGGING_H, (face.row % 8 == 4) & (face.col % 3 == 1))
        skin.face(leg, "up").fill(LEGGING)
        skin.face(leg, "down").fill(LEGGING)
        for face in skin.each(pants):
            face.clear()
    clear_under_shoes(skin, shoe_h)
