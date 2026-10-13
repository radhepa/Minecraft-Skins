"""Zippy: liquid-chrome speedster from Mercury, the fastest planet. Bright
orange eyes and a cheeky grin, a racing helmet with 3D feathered wings, a
charcoal racing suit with orange chevrons and the Mercury symbol, orange
gloves and winged 3D sneakers.
"""

import numpy as np

from paintkit import (SIDES, add_footwear, box, clear_under_shoes, cloth,
                      gradient, paint_sneakers, rows)
from skinlib import Skin, add_standard_body, noise

ID = "geometry.SolarSystem.Zippy"
TEXTURE = "zippy.png"
NAME = "Zippy"
LOC = "Zippy"
DETAILS = [
    ("face", "Winged racing helmet", {"yaw": 35, "pitch": 8, "dist": 50, "target": 27, "fov": 30}),
    ("shoes", "Winged 3D sneakers", {"yaw": 50, "pitch": 16, "dist": 44, "target": 4, "fov": 30}),
    ("back34", "Speed stripes", {"yaw": 160, "pitch": 10}),
]

CHROME_L = (240, 244, 252)
CHROME = (184, 192, 210)
CHROME_D = (112, 120, 142)
CHROME_X = (76, 82, 104)
EYE = (255, 140, 30)
EYE_L = (255, 214, 120)
PUPIL = (30, 24, 40)
HELM = (255, 116, 32)
HELM_L = (255, 170, 80)
HELM_D = (204, 72, 18)
WHITE = (250, 250, 252)
FEATHER = (246, 248, 255)
FEATHER_D = (196, 206, 226)
FEATHER_X = (150, 164, 196)
SUIT = (44, 46, 62)
SUIT_D = (30, 32, 44)
SUIT_H = (62, 66, 86)
ORANGE = (255, 122, 34)
ORANGE_D = (214, 82, 20)
MOUTH = (60, 40, 70)

SNEAKERS = {"upper": WHITE, "hi": (255, 255, 255), "dark": ORANGE, "lace": ORANGE,
            "lace_dark": ORANGE_D, "sole": (60, 62, 80), "sole_dark": (36, 38, 52)}


def add_wing(skin, prefix, bone, x0, base_y, z0, side=1, first=True):
    """Three feathers swept up and back, flaring out from the head. The first
    wing paints them; the other reuses the same texture."""
    piv = [x0 + 0.25, base_y, z0]
    rot = [-28, -18 * side, 0]
    parts = [("A", [0.5, 1.5, 6.0], 0.0, 0.0), ("B", [0.5, 1.5, 5.0], 1.4, 0.6),
             ("C", [0.5, 1.5, 4.0], 2.8, 1.2)]
    for key, size, dy, dz in parts:
        origin = [x0, base_y + dy, z0 + dz]
        name = f"{prefix}{key}"
        if first:
            skin.acc(name, bone, origin, size, lowres=("up", "down", "north", "south"),
                     pivot=piv, rotation=rot)
        else:
            skin.acc(name, bone, origin, size, like=f"wingR{key}", pivot=piv, rotation=rot)


def build():
    skin = Skin(ID)
    add_standard_body(skin)
    add_wing(skin, "wingR", "head", -5.0, 29.0, -0.5, side=1, first=True)
    add_wing(skin, "wingL", "head", 4.5, 29.0, -0.5, side=-1, first=False)
    h = add_footwear(skin, height=3.0)
    # little heel wings reuse the smallest helmet feather
    skin.acc("shoeWingR", "rightLeg", [-5.0, 1.0, 0.0], [0.5, 1.5, 4.0], like="wingRC",
             pivot=[-4.75, 1.0, 0.0], rotation=[-25, 15, 0])
    skin.acc("shoeWingL", "leftLeg", [4.5, 1.0, 0.0], [0.5, 1.5, 4.0], like="wingRC",
             pivot=[4.75, 1.0, 0.0], rotation=[-25, -15, 0])
    paint_head(skin)
    paint_wings(skin)
    paint_body(skin)
    paint_arms(skin)
    paint_legs(skin, h)
    paint_sneakers(skin, SNEAKERS, 2400)
    return skin


def chrome(face, seed):
    """Liquid metal: a sky-and-ground reflection band plus soft ripples."""
    t = np.clip(face.row / max(face.h - 1, 1) + 0.12 * np.sin(face.col * 0.7 + seed), 0, 1)
    gradient(face, [(0, CHROME_L), (0.35, CHROME), (0.55, CHROME_D), (0.62, CHROME), (1, CHROME_L)], t=t)
    face.shade(noise((face.h, face.w), seed, 0.02))


def paint_head(skin):
    for f in SIDES + ("up", "down"):
        chrome(skin.face("head", f), 2000 + len(f))
    front = skin.face("head", "north")
    # flat-ish face plate so the features read
    gradient(front, [(0, CHROME_L), (0.5, (214, 220, 234)), (1, CHROME)], mask=front.row >= 4)
    eye = [
        "PPPP",
        "PLEW",
        "PEEE",
        ".EE.",
    ]
    pal = {"P": PUPIL, "L": EYE_L, "E": EYE, "W": WHITE}
    front.stamp(eye, pal, top=6, left=2)
    front.stamp(eye, pal, top=6, left=10, mirror=True)
    front.set(10, 7, CHROME_D)
    # lopsided grin
    front.stamp(["M.....M", ".MWWWM.", "..MMM.."], {"M": MOUTH, "W": WHITE}, top=11, left=5)
    front.set(10, 12, MOUTH)

    # hat layer: racing helmet over the top, back and upper sides
    for f in SIDES + ("up", "down"):
        skin.face("hat", f).clear()
    for f in ("north", "east", "west", "south", "up"):
        face = skin.face("hat", f)
        gradient(face, [(0, HELM_L), (0.5, HELM), (1, HELM_D)], t=np.clip(face.row / 10, 0, 1))
        face.shade(noise((face.h, face.w), 2010 + len(f), 0.03))
    hf = skin.face("hat", "north")
    hf.clear(hf.row >= 5)
    rows(hf, 4, 4, HELM_D)
    rows(hf, 0, 4, WHITE, (hf.col == 7) | (hf.col == 8))
    # racing goggles pushed up on the helmet
    rows(hf, 2, 2, (40, 40, 52))
    for left in (2, 9):
        hf.stamp(["FFFFF", "FLGGF", "FGGGF", ".FFF."],
                 {"F": (40, 40, 52), "L": (220, 250, 255), "G": (90, 200, 236)}, top=1, left=left)
    for f in ("east", "west"):
        face = skin.face("hat", f)
        front_cols = face.col >= 11 if f == "east" else face.col <= 4
        face.clear(front_cols & (face.row >= 5))
        face.clear(face.row >= 11)
        rows(face, 10, 10, HELM_D)
    back = skin.face("hat", "south")
    back.clear(back.row >= 12)
    rows(back, 11, 11, HELM_D)
    rows(back, 0, 11, WHITE, (back.col == 7) | (back.col == 8))
    up = skin.face("hat", "up")
    up.fill(HELM)
    up.fill(WHITE, (up.col == 7) | (up.col == 8))


def paint_wings(skin):
    for key in ("A", "B", "C"):
        name = f"wingR{key}"
        for face in skin.each(name):
            face.fill(FEATHER)
        for f in ("east", "west"):
            face = skin.face(name, f)
            # runs from the root (front) to the tip (back of the head)
            along = face.col if f == "west" else face.w - 1 - face.col
            gradient(face, [(0, FEATHER), (0.7, FEATHER), (1, FEATHER_D)], t=along / (face.w - 1))
            face.fill(FEATHER_X, face.row == face.h - 1)
            face.fill(FEATHER_D, (face.row == face.h - 2) & (along >= face.w // 2))
            # quill along the middle of the feather, notched rounded tip
            face.fill((255, 255, 255), (face.row == 0) & (along < face.w - 2))
            face.clear((along == face.w - 1) & (face.row != 1))


def chevrons(face, top, color, shadow):
    for k in range(2):
        for c in range(face.w):
            r = top + k * 3 + abs(c - (face.w - 1) / 2) * 0.5
            face.set(int(round(r)), c, color)
            face.set(int(round(r)) + 1, c, shadow)


def paint_body(skin):
    for f in SIDES:
        face = skin.face("body", f)
        cloth(face, SUIT, 2100 + len(f), var=0.04, fold=0.03)
        # orange side panels
        if f in ("east", "west"):
            face.fill(ORANGE, (face.col >= 3) & (face.col <= 4))
        rows(face, 18, 19, SUIT_D)
        rows(face, 18, 18, ORANGE)
    front = skin.face("body", "north")
    # orange yoke with a white piping line
    rows(front, 0, 3, ORANGE)
    rows(front, 3, 3, ORANGE_D)
    rows(front, 4, 4, WHITE)
    # racing bib: the fastest planet is number one
    bib = [
        ".WWWWWW.",
        "WWWOOWWW",
        "WWOOOWWW",
        "WWWOOWWW",
        "WWWOOWWW",
        "WWWOOWWW",
        "WWOOOOWW",
        ".WWWWWW.",
    ]
    front.stamp(bib, {"W": WHITE, "O": ORANGE}, top=7, left=4)
    for c in (4, 11):
        front.set(7, c, (200, 204, 216))
    back = skin.face("body", "south")
    chevrons(back, 3, ORANGE, ORANGE_D)
    chevrons(back, 10, WHITE, (200, 204, 216))
    cloth(skin.face("body", "up"), SUIT_D, 2120)
    cloth(skin.face("body", "down"), SUIT_D, 2121)
    for face in skin.each("jacket"):
        face.clear()
    # collar of the racing suit
    jk = skin.face("jacket", "north")
    jk.fill(ORANGE, (jk.row == 0) & ((jk.col <= 4) | (jk.col >= 11)))
    for f in ("east", "west", "south"):
        rows(skin.face("jacket", f), 0, 0, ORANGE)


def paint_arms(skin):
    for arm, slv, seed in (("rightArm", "rightSleeve", 2200), ("leftArm", "leftSleeve", 2210)):
        for f in SIDES + ("up", "down"):
            face = skin.face(arm, f)
            chrome(face, seed + len(f))
        for f in SIDES:
            face = skin.face(arm, f)
            # short suit sleeves, orange racing gloves
            cloth(face, SUIT, seed + 10 + len(f), var=0.04, fold=0.03, mask=face.row <= 7)
            rows(face, 7, 7, ORANGE)
            gradient(face, [(0, HELM_L), (1, ORANGE_D)], t=np.clip((face.row - 15) / 8, 0, 1), mask=face.row >= 15)
            rows(face, 15, 16, WHITE)
        skin.face(arm, "up").fill(SUIT)
        skin.face(arm, "down").fill(ORANGE_D)
        for face in skin.each(slv):
            face.clear()
        # raised glove cuffs
        for f in SIDES:
            face = skin.face(slv, f)
            rows(face, 15, 16, WHITE)
            rows(face, 16, 16, FEATHER_D)


def paint_legs(skin, shoe_h):
    for leg, pants, outer, seed in (("rightLeg", "rightPants", "east", 2300), ("leftLeg", "leftPants", "west", 2310)):
        for f in SIDES:
            face = skin.face(leg, f)
            cloth(face, SUIT, seed + len(f), var=0.04, fold=0.04)
            if f == outer:
                face.fill(ORANGE, (face.col >= 3) & (face.col <= 4))
                face.fill(WHITE, face.col == 2)
        skin.face(leg, "up").fill(SUIT)
        skin.face(leg, "down").fill(SUIT_D)
        for face in skin.each(pants):
            face.clear()
        knee = skin.face(pants, "north")
        knee.fill(SUIT_H, box(knee, 8, 1, 11, 6))
        knee.fill(ORANGE, box(knee, 9, 2, 10, 5))
    clear_under_shoes(skin, shoe_h)
