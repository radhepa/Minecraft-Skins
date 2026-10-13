"""Luna: moon-white alien from Earth's Moon with tiny crater freckles, dreamy
star-lit blue eyes and long silver hair, a 3D golden crescent-moon hair
ornament with little stars, a puffy white space suit with a control panel,
a 3D life-support backpack, periwinkle gloves and chunky moon boots.
"""

import numpy as np

from paintkit import (SIDES, add_footwear, box, clear_under_shoes, cloth,
                      gradient, hair, rows, skin_tone)
from skinlib import Skin, add_standard_body, noise

ID = "geometry.SolarSystem.Luna"
TEXTURE = "luna.png"
NAME = "Luna"
LOC = "Luna"
DETAILS = [
    ("face", "Crater freckles + 3D crescent", {"yaw": 20, "pitch": 6, "dist": 52, "target": 28, "fov": 30}),
    ("back34", "Life-support backpack", {"yaw": 150, "pitch": 10}),
    ("boots", "Puffy suit + moon boots", {"yaw": -30, "pitch": 12, "dist": 60, "target": 8, "fov": 30}),
]

SKIN = (230, 232, 240)
SKIN_D = (204, 208, 222)
CRATER = (196, 198, 214)
CRATER_L = (246, 248, 252)
BLUSH = (240, 186, 206)
HAIR = (48, 56, 118)
HAIR_D = (30, 34, 82)
HAIR_L = (78, 92, 164)
SHINE = (196, 206, 250)
IRIS = (64, 96, 196)
IRIS_L = (130, 170, 240)
LASH = (54, 50, 86)
MOON = (255, 230, 140)
MOON_L = (255, 248, 206)
MOON_D = (230, 186, 80)
SUIT = (244, 244, 248)
SUIT_D = (212, 214, 226)
SUIT_X = (176, 180, 200)
PERI = (128, 140, 230)
PERI_D = (92, 102, 196)
PERI_L = (176, 186, 255)
GREY = (120, 124, 144)
GREY_D = (84, 88, 108)
MOUTH = (150, 90, 120)

# crescent ornament: a flat plate painted at 3 texels per unit, in its own
# tilted bone on the side of the head
CX, CY, CZ = -6.75, 29.75, -5.0
CS = 6.0


def build():
    skin = Skin(ID, slim=True)
    add_standard_body(skin)
    skin.bone("crescent", "head", [CX + CS / 2, CY + CS / 2, CZ], rotation=[0, 0, -20])
    skin.acc("moon", "crescent", [CX, CY, CZ], [CS, CS, 0.5], px=3, faces=("north", "south"), pad=("north", "south"))
    skin.acc("star0", "crescent", [CX + 4.0, CY + 3.25, CZ], [1.5, 1.5, 0.5], faces=("north", "south"), pad=("north", "south"))
    skin.acc("star1", "crescent", [CX + 4.75, CY + 1.25, CZ], [1, 1, 0.5], faces=("north", "south"), pad=("north", "south"))
    skin.acc("pack", "body", [-3.5, 13.5, 2.25], [7, 9, 3], lowres=("up", "down", "north", "east", "west"))
    skin.acc("collar", "body", [-4.5, 23, -2.5], [9, 1, 5], lowres=("up", "down", "east", "west"))
    h = add_footwear(skin, height=4.0, length=5.5, toe=1.25, tongue=False, width=4.5)
    paint_head(skin)
    paint_crescent(skin)
    paint_body(skin)
    paint_arms(skin)
    paint_legs(skin, h)
    paint_boots(skin)
    return skin


def craters(face, spots):
    """Tiny craters: a darker dish with a bright rim catching the light."""
    for r, c in spots:
        face.set(r, c, CRATER)
        face.set(r + 1, c + 1, CRATER_L)
        face.set(r, c + 1, SKIN_D)


BANGS = [8, 7, 5, 4, 4, 3, 3, 2, 2, 3, 3, 4, 4, 5, 7, 8]


def paint_head(skin):
    front = skin.face("head", "north")
    skin_tone(front, SKIN, 4000, var=0.015)
    bangs = front.row <= np.array(BANGS)[front.col]
    side = ((front.col <= 0) | (front.col >= 15))
    hair(front, HAIR, HAIR_D, HAIR_L, 4001, mask=bangs | side, shine=SHINE)
    front.shade(np.where((front.row == np.array(BANGS)[front.col] + 1) & ~bangs, 0.92, 1.0))
    # dreamy eyes with a star-shaped glint
    eye = [
        "LLLL.",
        "WWIIL",
        "WIIIL",
        "IIIWI",
        ".JJJ.",
    ]
    pal = {"L": LASH, "I": IRIS, "W": (255, 255, 255), "J": IRIS_L}
    front.stamp(eye, pal, top=6, left=2)
    front.stamp(eye, pal, top=6, left=9, mirror=True)
    front.set(6, 1, LASH)
    front.set(6, 14, LASH)
    for c in (2, 3, 12, 13):
        front.set(11, c, BLUSH)
    craters(front, [(12, 1), (10, 12)])
    front.stamp([".MM."], {"M": MOUTH}, top=13, left=6)
    front.set(12, 6, MOUTH)
    front.set(12, 9, MOUTH)
    for f in ("east", "west", "south", "up"):
        face = skin.face("head", f)
        hair(face, HAIR, HAIR_D, HAIR_L, 4010 + len(f), shine=SHINE)
    skin_tone(skin.face("head", "down"), SKIN_D, 4020)
    # hat layer: long hair falling over the shoulders at the back
    for face in skin.each("hat"):
        face.clear()
    for f in ("east", "west", "south", "up"):
        face = skin.face("hat", f)
        hair(face, HAIR, HAIR_D, HAIR_L, 4030 + len(f), shine=SHINE)
        if f in ("east", "west"):
            near_front = face.col >= 13 if f == "east" else face.col <= 2
            face.clear(near_front & (face.row >= 3))
    hf = skin.face("hat", "north")
    hair(hf, HAIR, HAIR_D, HAIR_L, 4040, shine=SHINE)
    hf.clear(hf.row > np.array(BANGS)[hf.col] - 1)
    skin.face("hat", "down").clear()


def paint_crescent(skin):
    for f in ("north", "south"):
        face = skin.face("moon", f)
        n = face.w
        cc = face.col if f == "north" else n - 1 - face.col
        r0 = np.hypot(cc - (n - 1) / 2, face.row - (n - 1) / 2)
        r1 = np.hypot(cc - (n - 1) / 2 - n * 0.36, face.row - (n - 1) / 2 + n * 0.1)
        moon = (r0 <= n / 2 - 0.2) & (r1 > n * 0.4)
        lit = np.clip(r0 / (n / 2), 0, 1)
        gradient(face, [(0, MOON_L), (0.6, MOON), (1, MOON_D)], t=1 - lit)
        face.fill(MOON_L, moon & (r1 <= n * 0.4 + 1.1))
        face.fill(MOON_D, moon & (r0 > n / 2 - 1.2))
        face.clear(~moon)
        # two little craters
        for r, c in ((6, 3), (12, 5)):
            c = c if f == "north" else n - 1 - c
            face.set(r, c, MOON_D)
    for name in ("star0", "star1"):
        for face in skin.each(name):
            face.clear()
        for f in ("north", "south"):
            face = skin.face(name, f)
            face.fill(MOON_L)
            face.clear((face.row != face.h // 2) & (face.col != face.w // 2) & (face.w > 1))


def suit(face, seed):
    cloth(face, SUIT, seed, var=0.025, fold=0.05, freq=0.9)
    # puffy quilted segments
    face.shade(np.where(face.row % 6 == 5, 0.9, 1.0))


def paint_body(skin):
    for f in SIDES + ("up", "down"):
        suit(skin.face("body", f), 4200 + len(f))
    front = skin.face("body", "north")
    # control panel on the chest
    front.fill(SUIT_X, box(front, 4, 4, 11, 11))
    front.fill(GREY_D, box(front, 5, 5, 10, 10))
    front.stamp(["RG.B", "....", "YY.C"], {"R": (255, 96, 120), "G": (110, 230, 140), "B": PERI_L,
                                           "Y": MOON, "C": (120, 230, 255)}, top=6, left=6)
    front.fill((200, 210, 230), box(front, 9, 6, 9, 9))
    # crescent mission patch
    front.stamp([".MM", "M..", ".MM"], {"M": MOON}, top=14, left=2)
    # periwinkle zip line and belt
    front.fill(PERI, (front.col == 7) & (front.row >= 12) & (front.row <= 23))
    for f in SIDES:
        face = skin.face("body", f)
        rows(face, 18, 19, PERI)
        rows(face, 19, 19, PERI_D)
    front.stamp(["MMMM", "M..M"], {"M": MOON_D}, top=18, left=6)
    for face in skin.each("jacket"):
        face.clear()

    for face in skin.each("pack"):
        suit(face, 4210 + face.w + face.h)
    back = skin.face("pack", "south")
    back.fill(SUIT_D, box(back, 1, 1, back.h - 2, back.w - 2))
    for r in range(3, 12, 3):
        rows(back, r, r, GREY, (back.col >= 3) & (back.col <= back.w - 4))
    back.fill(PERI, box(back, 13, 3, 15, back.w - 4))
    back.set(14, 4, (110, 230, 140))
    back.set(14, 6, (255, 96, 120))
    for f in ("east", "west"):
        face = skin.face("pack", f)
        rows(face, 2, 2, PERI)
    top = skin.face("pack", "up")
    top.fill(GREY)
    for face in skin.each("collar"):
        face.fill(PERI)
    for f in ("north", "south"):
        face = skin.face("collar", f)
        face.fill(PERI_L, face.row == 0)
        face.fill(PERI_D, face.row == face.h - 1)


def paint_arms(skin):
    for arm, slv, seed in (("rightArm", "rightSleeve", 4300), ("leftArm", "leftSleeve", 4310)):
        for f in SIDES + ("up", "down"):
            suit(skin.face(arm, f), seed + len(f))
        for f in SIDES:
            face = skin.face(arm, f)
            gradient(face, [(0, PERI_L), (0.3, PERI), (1, PERI_D)], t=np.clip((face.row - 16) / 7, 0, 1),
                     mask=face.row >= 16)
            rows(face, 7, 7, PERI)
        skin.face(arm, "down").fill(PERI_D)
        for face in skin.each(slv):
            face.clear()
        # chunky glove cuffs on the sleeve layer
        for f in SIDES:
            face = skin.face(slv, f)
            rows(face, 15, 17, SUIT_D)
            rows(face, 15, 15, SUIT)
            rows(face, 17, 17, SUIT_X)
        if True:
            patch = skin.face(slv, "east" if arm == "rightArm" else "west")
            patch.stamp(["PPP", "PWP", "PPP"], {"P": PERI, "W": MOON}, top=3, left=3)


def paint_legs(skin, boot_h):
    for leg, pants, seed in (("rightLeg", "rightPants", 4400), ("leftLeg", "leftPants", 4410)):
        for f in SIDES + ("up", "down"):
            suit(skin.face(leg, f), seed + len(f))
        for f in SIDES:
            face = skin.face(leg, f)
            if f in ("east", "west"):
                face.fill(PERI, (face.col >= 3) & (face.col <= 4) & (face.row <= 14))
        for face in skin.each(pants):
            face.clear()
        knee = skin.face(pants, "north")
        knee.fill(SUIT_D, box(knee, 7, 1, 10, 6))
        knee.fill(SUIT, box(knee, 7, 1, 7, 6))
    clear_under_shoes(skin, boot_h)


def paint_boots(skin):
    for side in ("right", "left"):
        shoe = f"{side}Shoe"
        for face in skin.each(shoe):
            suit(face, 4500 + face.w + face.h)
        for f in SIDES:
            face = skin.face(shoe, f)
            rows(face, 0, 1, PERI)
            rows(face, 0, 0, PERI_L)
            rows(face, face.h - 3, face.h - 1, GREY)
            rows(face, face.h - 1, face.h - 1, GREY_D)
            face.fill(GREY_D, (face.row == face.h - 2) & (face.col % 2 == 0))
        skin.face(shoe, "down").fill(GREY_D)
        top = skin.face(shoe, "up")
        top.fill(SUIT_D)
