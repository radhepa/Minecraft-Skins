"""Itsuki the Rift Stalker: the Soul-Infused assassin who steps in and out
of the Sift's rifts. A deep violet hood over his slashed headband, a dark
cloth mask over the lower face, glowing violet eyes under scowling brows,
a charcoal stalker's coat torn with glowing rift cracks, a trailing scarf,
dark bandaged arms, a crystal rift dagger in his hand and a rift shard
drifting at his shoulder.
"""

import numpy as np

from paintkit import SIDES, box, clear_under_shoes, cloth, gradient, rows
from skinlib import Skin, add_standard_body, noise

from .shinobi import (add_headband, add_sandals, hair_head, hair_painter, male_face,
                      paint_headband, paint_sandals, wraps)

ID = "geometry.LandOfTheHiddenSift.Itsuki"
TEXTURE = "itsuki.png"
NAME = "Itsuki the Rift Stalker"
LOC = "Itsuki"
DETAILS = [
    ("face", "Hood, mask + slashed headband", {"yaw": 20, "pitch": 4, "dist": 48, "target": 28, "fov": 30}),
    ("dagger", "Rift dagger + shard", {"yaw": 35, "pitch": 6, "dist": 70, "target": 16, "fov": 30}),
    ("back34", "Rift-torn coat + scarf", {"yaw": 160, "pitch": 10}),
]

SKIN = (206, 192, 196)
SKIN_D = (176, 160, 168)
HAIR = (50, 40, 64)
HAIR_D = (26, 20, 36)
HAIR_L = (84, 70, 106)
BROW = (30, 22, 40)
LASH = (16, 12, 22)
RIFT = (176, 100, 255)
RIFT_C = (236, 210, 255)
RIFT_D = (110, 50, 190)
RIFT_T = (90, 236, 222)
HOOD = (58, 40, 86)
HOOD_D = (36, 24, 56)
HOOD_L = (84, 62, 118)
MASK = (30, 28, 38)
MASK_D = (18, 16, 24)
COAT = (40, 38, 50)
COAT_D = (24, 22, 32)
COAT_L = (64, 62, 78)
WRAP_DARK = (70, 66, 80)
SANDAL = (30, 28, 38)
SANDAL_D = (16, 14, 22)


def build():
    skin = Skin(ID)
    add_standard_body(skin)
    add_headband(skin, yc=29.8)
    # the hood's point falling behind
    skin.acc("hoodTip", "head", [-1.5, 26.0, 4.5], [3, 4, 1.25], rotation=[22, 0, 0],
             pivot=[0, 30.0, 4.5], lowres=("up", "down"))
    # a scarf end trailing over his left shoulder and down his back
    skin.acc("scarf", "body", [1.25, 14.5, 2.1], [2.25, 8.5, 0.4], faces=("north", "south", "east", "west"),
             lowres=("north", "east", "west"), rotation=[10, 0, -8], pivot=[2.4, 23.5, 2.3])
    # crystal rift dagger, held point-down
    skin.acc("grip", "rightArm", [-6.4, 10.0, -0.4], [0.8, 3, 0.8], lowres=SIDES + ("up", "down"))
    skin.acc("blade", "rightArm", [-6.6, 5.5, -0.15], [1.2, 4.5, 0.3], faces=("east", "west", "north", "south"),
             lowres=("north", "south"), pad=("east",), same={"west": "east"})
    # rift shard drifting by his left shoulder, turned onto a point
    skin.acc("shard", "body", [8.0, 25.0, -1.0], [1.5, 1.5, 1.5], rotation=[45, 0, 45],
             pivot=[8.75, 25.75, -0.25])
    h = add_sandals(skin)
    paint_head(skin)
    paint_gear(skin)
    paint_body(skin)
    paint_arms(skin)
    paint_legs(skin, h)
    paint_sandals(skin, SANDAL, SANDAL_D, SKIN, SKIN_D)
    return skin


def hood(face, seed):
    cloth(face, HOOD, seed, var=0.04, fold=0.06, freq=1.1)


def rift_crack(face, start, length, seed):
    """A jagged glowing tear running downwards."""
    rs = np.random.RandomState(seed)
    r, c = start
    for _ in range(length):
        face.set(r, c, RIFT_C if rs.rand() < 0.35 else RIFT)
        for dc in (-1, 1):
            cc = c + dc
            if 0 <= cc < face.w and face.rgba[r, cc, 3] > 0:
                face.rgba[r, cc, :3] = face.rgba[r, cc, :3] * 0.6 + np.array(RIFT_D) * 0.4
        r += 1
        c = int(np.clip(c + rs.choice([-1, 0, 1]), 0, face.w - 1))
        if r >= face.h:
            break


def paint_head(skin):
    dark = hair_painter(HAIR, HAIR_D, HAIR_L)
    hair_head(skin, dark, 14000, SKIN, SKIN_D, [9, 8, 7, 7, 6, 6, 5, 5, 5, 5, 4, 4, 4, 5, 7, 8],
              back_bottom=11)
    front = skin.face("head", "north")
    male_face(front, BROW, {"L": LASH, "W": (226, 220, 236), "D": RIFT_D, "E": RIFT, "H": RIFT_C,
                            "G": RIFT_C}, MASK, slant=True)
    # cloth mask over the nose and mouth
    m = front.row >= 11
    cloth(front, MASK, 14010, var=0.03, fold=0.04, mask=m)
    front.fill(MASK_D, front.row == 11)
    front.fill((44, 42, 56), (front.row == 12) & ((front.col == 7) | (front.col == 8)))
    for f in ("east", "west", "south"):
        face = skin.face("head", f)
        cloth(face, MASK, 14020 + len(f), var=0.03, fold=0.04, mask=face.row >= 11)
    # the hood over the hat layer, open around the face
    for f in ("north", "east", "west", "south", "up"):
        face = skin.face("hat", f)
        hood(face, 14030 + len(f))
    hf = skin.face("hat", "north")
    hf.clear(box(hf, 5, 2, 15, 13))
    hf.fill(HOOD_D, ((hf.col == 1) | (hf.col == 14)) & (hf.row >= 5))
    for f in ("east", "west", "south"):
        face = skin.face("hat", f)
        face.fill(HOOD_D, face.row == face.h - 1)
    paint_headband(skin, slashed=True)
    for face in skin.each("hoodTip"):
        hood(face, 14040 + face.w)


def paint_gear(skin):
    for f in ("south",):
        face = skin.face("scarf", f)
        cloth(face, HOOD, 14100, var=0.04, fold=0.08, freq=1.4)
        face.fill(RIFT, face.col == 0)
        face.clear((face.row == face.h - 1) & (face.col % 2 == 1))
    for f in ("north", "east", "west"):
        skin.face("scarf", f).fill(HOOD_D)
    for face in skin.each("grip"):
        face.fill((40, 34, 50))
        face.fill(RIFT_D, face.row % 2 == 0)
    b = skin.face("blade", "east")
    gradient(b, [(0, RIFT_C), (0.5, RIFT), (1, RIFT_D)])
    b.fill(RIFT_C, b.col == 0)
    b.clear((b.row == b.h - 1) & (b.col != 0))          # the point
    for f in ("north", "south"):
        skin.face("blade", f).fill(RIFT_D)
    for face in skin.each("shard"):
        gradient(face, [(0, RIFT_C), (0.5, RIFT), (1, RIFT_D)])
        face.fill(RIFT_T, (face.row == face.col))


def paint_body(skin):
    for f in SIDES + ("up", "down"):
        cloth(skin.face("body", f), COAT, 14200 + len(f), var=0.04, fold=0.05)
    for f in SIDES:
        face = skin.face("body", f)
        rows(face, 0, 2, HOOD)
        rows(face, 2, 2, HOOD_D)
        rows(face, 18, 19, HOOD_D)
        rows(face, 20, 23, COAT_D)
    front = skin.face("body", "north")
    # wrap-front coat crossing left over right
    for r in range(3, 18):
        c = 4 + (r - 3) // 2
        front.set(r, c, COAT_L)
    rift_crack(front, (6, 11), 9, 14210)
    back = skin.face("body", "south")
    rift_crack(back, (3, 4), 12, 14211)
    rift_crack(back, (8, 11), 8, 14212)
    for face in skin.each("jacket"):
        face.clear()


def paint_arms(skin):
    for arm, slv, seed in (("rightArm", "rightSleeve", 14300), ("leftArm", "leftSleeve", 14310)):
        for f in SIDES + ("up", "down"):
            cloth(skin.face(arm, f), COAT, seed + len(f), var=0.04, fold=0.05)
        for f in SIDES:
            face = skin.face(arm, f)
            wraps(face, 10, 22)
            face.shade(0.45, (face.row >= 10) & (face.row <= 22))
            rows(face, 23, 23, SKIN_D)
        skin.face(arm, "down").fill(MASK)
        for face in skin.each(slv):
            face.clear()
        for f in SIDES:
            face = skin.face(slv, f)
            rows(face, 8, 9, COAT_L)
            rows(face, 9, 9, RIFT_D)
        if arm == "leftArm":
            rift_crack(skin.face(arm, "west"), (2, 3), 6, seed + 30)


def paint_legs(skin, boot_h):
    for leg, pants, seed in (("rightLeg", "rightPants", 14400), ("leftLeg", "leftPants", 14410)):
        for f in SIDES:
            cloth(skin.face(leg, f), COAT_D, seed + len(f), var=0.05, fold=0.07, freq=0.9)
        skin.face(leg, "up").fill(COAT_D)
        skin.face(leg, "down").fill(COAT_D)
        for face in skin.each(pants):
            face.clear()
        for f in SIDES:
            face = skin.face(pants, f)
            wraps(face, 12, 19)
            face.shade(0.45, (face.row >= 12) & (face.row <= 19))
    clear_under_shoes(skin, boot_h)
