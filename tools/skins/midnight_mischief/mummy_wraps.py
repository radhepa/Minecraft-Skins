"""Mummy Wraps: bandaged from head to toe with one glowing green eye, a gold
pharaoh collar with a purple scarab, a purple sash and loose 3D wraps
trailing from the head, arm and leg.
"""

import numpy as np

from paintkit import SIDES, box, eye_glow, rows
from skinlib import Skin, add_standard_body, noise

ID = "geometry.MidnightMischief.MummyWraps"
TEXTURE = "mummy_wraps.png"
NAME = "Mummy Wraps"
LOC = "MummyWraps"
DETAILS = [
    ("face", "Glowing eye + loose wraps", {"yaw": 30, "pitch": 6, "dist": 42, "target": 26, "fov": 30}),
    ("back34", "Trailing 3D bandages", {"yaw": 145, "pitch": 8}),
    ("collar", "Pharaoh collar + scarab", {"yaw": -15, "pitch": 6, "dist": 46, "target": 19, "fov": 30}),
]

WRAP = (228, 216, 190)
WRAP_D = (204, 190, 162)
WRAP_H = (242, 234, 214)
WRAP_X = (178, 162, 132)
GAP = (52, 40, 40)
GREEN_C = (214, 255, 200)
GREEN = (110, 240, 122)
GREEN_R = (48, 168, 80)
GOLD = (240, 182, 56)
GOLD_D = (190, 128, 30)
LAPIS = (52, 80, 176)
TURQ = (64, 196, 186)
PURPLE = (110, 52, 168)
PURPLE_D = (80, 34, 128)
PURPLE_H = (140, 80, 196)


def build():
    skin = Skin(ID)
    add_standard_body(skin)
    skin.acc("wrapHead", "head", [1.5, 21, 4.25], [1.5, 5.5, 0.5], px=2, faces=("north", "south", "east", "west", "down"))
    skin.acc("wrapArm", "rightArm", [-8.75, 9, -0.75], [0.5, 5, 1.5], px=2, faces=("north", "south", "east", "west", "down"))
    skin.acc("wrapLeg", "leftLeg", [4.15, 4, -0.5], [0.5, 4.5, 1.5], px=2, faces=("north", "south", "east", "west", "down"))
    paint_all(skin)
    return skin


def bandage(face, seed, slant=4):
    """Slanted wraps: 2-texel strips separated by a darker seam line."""
    rs = np.random.RandomState(seed)
    t = face.row + face.col // slant
    strip, phase = t // 3, t % 3
    tones = np.array([WRAP, WRAP_H, WRAP_D], float)
    pick = rs.randint(0, 3, size=strip.max() + 1)
    face.rgba[..., :3] = tones[pick[strip]]
    face.rgba[..., 3] = 255
    face.fill(WRAP_X, phase == 2)
    face.shade(np.where(phase == 0, 1.03, 1.0))
    face.shade(noise((face.h, face.w), seed + 1, 0.02))


def loose_mask(face, every=4, which=1, slant=4):
    t = face.row + face.col // slant
    return ((t // 3) % every == which) & (t % 3 != 2)


def paint_all(skin):
    seed = 3600
    for name in ("head", "body", "rightArm", "leftArm", "rightLeg", "leftLeg"):
        for face in skin.each(name):
            bandage(face, seed)
            seed += 3
    front = skin.face("head", "north")
    rows(front, 7, 8, GAP, (front.col >= 1) & (front.col <= 14))
    eye_glow(front, [(7, 3), (7, 4), (7, 5), (8, 3), (8, 4), (8, 5)], GREEN_C, GREEN, GREEN_R)
    front.set(7, 4, GREEN_C)
    front.set(8, 11, GREEN_R)                          # glint behind the wraps
    rows(front, 9, 9, WRAP_X, (front.col >= 1) & (front.col <= 14))
    rows(front, 12, 12, GAP, (front.col >= 5) & (front.col <= 10))
    rows(front, 13, 13, WRAP_X, (front.col >= 5) & (front.col <= 10))
    skin.face("head", "down").fill(WRAP_D)

    # hat layer: a few loose wraps standing proud of the head
    for f in SIDES + ("up", "down"):
        face = skin.face("hat", f)
        bandage(face, 3700 + len(f), slant=3)
        face.clear(~loose_mask(face, 4, 1, 3))
        if f == "north":
            face.clear((face.row >= 5) & (face.row <= 9))
    skin.face("hat", "down").clear()

    # pharaoh collar + scarab on the jacket layer, purple sash on the base
    body = skin.face("body", "north")
    rows(body, 14, 15, PURPLE)
    rows(body, 15, 15, PURPLE_D)
    body.fill(PURPLE, box(body, 16, 6, 22, 9))
    body.fill(PURPLE_H, box(body, 16, 6, 22, 6))
    body.fill(GOLD, box(body, 23, 6, 23, 9))
    body.set(14, 7, GOLD)
    body.set(14, 8, GOLD)
    for f in ("east", "west", "south"):
        face = skin.face("body", f)
        rows(face, 14, 15, PURPLE)
        rows(face, 15, 15, PURPLE_D)
    for face in skin.each("jacket"):
        face.clear()
    jk = skin.face("jacket", "north")
    collar_rows = [(0, GOLD), (1, LAPIS), (2, GOLD), (3, TURQ), (4, GOLD_D)]
    for r, col in collar_rows:
        width = 6 + r
        jk.fill(col, (jk.row == r) & (abs(jk.col - 7.5) <= width))
    scarab = [".PP.", "PHPP", "PPPP", ".GG."]
    jk.stamp(scarab, {"P": PURPLE, "H": PURPLE_H, "G": GOLD}, top=5, left=6)
    for f in ("east", "west", "south"):
        face = skin.face("jacket", f)
        for r, col in collar_rows[:3]:
            rows(face, r, r, col)
    jtop = skin.face("jacket", "up")
    jtop.fill(GOLD)
    jtop.clear(box(jtop, 2, 3, 6, 12))

    # loose bandage overlays on arms and legs, ragged
    for layer, s in (("rightSleeve", 3800), ("leftSleeve", 3810), ("rightPants", 3820), ("leftPants", 3830)):
        for face in skin.each(layer):
            bandage(face, s + face.w)
            face.clear(~loose_mask(face, 5, 2))
        skin.face(layer, "up").clear()
        skin.face(layer, "down").clear()

    for name in ("wrapHead", "wrapArm", "wrapLeg"):
        for face in skin.each(name):
            bandage(face, 3900 + face.w + face.h, slant=99)
        for f in SIDES:
            if (name, f) in skin.faces:
                face = skin.face(name, f)
                face.clear((face.row == face.h - 1) & (face.col % 2 == 1))
