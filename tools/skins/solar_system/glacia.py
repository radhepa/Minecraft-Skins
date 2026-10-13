"""Glacia: icy princess from Uranus, the planet that spins on its side. Pale
cyan skin, violet eyes, frosty white-and-cyan hair in a 3D sideways ponytail,
a 3D ice-crystal tiara and shoulder crystals, a teal skater dress with a
snowflake and a 3D icicle-fringed skirt, and fur-trimmed white boots.
"""

import numpy as np

from paintkit import (SIDES, add_footwear, box, clear_under_shoes, cloth,
                      gradient, hair, rows, skin_tone)
from skinlib import Skin, add_standard_body, noise

ID = "geometry.SolarSystem.Glacia"
TEXTURE = "glacia.png"
NAME = "Glacia"
LOC = "Glacia"
DETAILS = [
    ("face", "Crystal tiara + violet eyes", {"yaw": 18, "pitch": 6, "dist": 52, "target": 28, "fov": 30}),
    ("pony", "Sideways ponytail", {"yaw": -70, "pitch": 8, "dist": 60, "target": 26, "fov": 30}),
    ("skirt", "Icicle skirt + shoulder crystals", {"yaw": 30, "pitch": 10, "dist": 66, "target": 16, "fov": 30}),
]

SKIN = (184, 234, 240)
SKIN_D = (150, 210, 222)
BLUSH = (236, 176, 220)
HAIR = (226, 244, 252)
HAIR_D = (150, 214, 236)
HAIR_L = (255, 255, 255)
IRIS = (128, 86, 214)
IRIS_L = (190, 160, 255)
LASH = (40, 54, 92)
ICE = (196, 240, 255)
ICE_L = (246, 254, 255)
ICE_D = (110, 196, 230)
ICE_X = (70, 150, 200)
TEAL = (30, 132, 156)
TEAL_D = (18, 92, 116)
TEAL_L = (70, 180, 200)
SILVER = (220, 228, 240)
SILVER_D = (160, 172, 196)
FUR = (250, 252, 255)
FUR_D = (214, 226, 240)
MOUTH = (110, 70, 130)
VIOLET = (140, 100, 224)
VIOLET_D = (100, 66, 180)


def crystal(skin, name, bone, x, y, z, w, h, like=None, lean=0.0):
    """A diamond-section ice crystal: a square prism turned 45 degrees."""
    kw = dict(pivot=[x, y, z], rotation=[0, 45, lean])
    origin = [x - w / 2, y, z - w / 2]
    if like:
        return skin.acc(name, bone, origin, [w, h, w], like=like, **kw)
    return skin.acc(name, bone, origin, [w, h, w], lowres=("down",), **kw)


def build():
    skin = Skin(ID, slim=True)
    add_standard_body(skin)
    # tiara crystals along the front of the head
    crystal(skin, "tiaraMid", "head", 0, 32.0, -3.5, 1.5, 3.5)
    crystal(skin, "tiaraR", "head", -2.25, 32.0, -3.5, 1.0, 2.0, lean=12)
    crystal(skin, "tiaraL", "head", 2.25, 32.0, -3.5, 1.0, 2.0, like="tiaraR", lean=-12)
    # sideways ponytail, swept out from her left side
    skin.acc("ponyTie", "head", [4.25, 27.5, -0.5], [1, 2, 2], lowres=("up", "down"))
    skin.acc("pony", "head", [5.0, 27.0, -0.75], [5, 2.5, 2.5], lowres=("east",),
             pivot=[5.0, 28.25, 0.5], rotation=[0, 0, 32])
    skin.acc("ponyTip", "head", [9.75, 27.5, -0.25], [3, 1.5, 1.5], lowres=("east",),
             pivot=[5.0, 28.25, 0.5], rotation=[0, 0, 32])
    # crystals on the shoulders
    crystal(skin, "shoulderR", "rightArm", -5.5, 23.0, 0, 1.25, 2.5, lean=25)
    crystal(skin, "shoulderL", "leftArm", 5.5, 23.0, 0, 1.25, 2.5, like="shoulderR", lean=-25)
    skin.acc("skirt", "body", [-4.5, 10.5, -2.5], [9, 2.5, 5], lowres=("up", "down"))
    h = add_footwear(skin, height=3.5, length=5.0, toe=1.0, tongue=False, width=4.25)
    paint_head(skin)
    paint_ice(skin)
    paint_body(skin)
    paint_arms(skin)
    paint_legs(skin, h)
    paint_boots(skin)
    return skin


def frost_hair(face, seed, mask=None):
    hair(face, HAIR, HAIR_D, HAIR_L, seed, mask=mask, shine=(255, 255, 255))


BANGS = [6, 5, 4, 4, 3, 3, 4, 3, 2, 3, 4, 4, 3, 4, 5, 6]


def paint_head(skin):
    front = skin.face("head", "north")
    skin_tone(front, SKIN, 7000, var=0.015)
    bangs = front.row <= np.array(BANGS)[front.col]
    frost_hair(front, 7001, mask=bangs | (((front.col == 0) | (front.col == 15)) & (front.row <= 10)))
    front.shade(np.where((front.row == np.array(BANGS)[front.col] + 1) & ~bangs, 0.92, 1.0))
    eye = [
        "LLLL.",
        "WIIIL",
        "IWIIL",
        "IIJJ.",
        ".JJJ.",
    ]
    pal = {"L": LASH, "W": (255, 255, 255), "I": IRIS, "J": IRIS_L}
    front.stamp(eye, pal, top=6, left=2)
    front.stamp(eye, pal, top=6, left=9, mirror=True)
    front.set(5, 1, LASH)
    front.set(5, 14, LASH)
    for c in (2, 3, 12, 13):
        front.set(11, c, BLUSH)
    # frost freckles: tiny snowflake sparkle under one eye
    front.set(11, 11, ICE_L)
    front.stamp(["M..M", ".MM."], {"M": MOUTH}, top=12, left=6)
    for f in ("east", "west", "south", "up"):
        face = skin.face("head", f)
        skin_tone(face, SKIN, 7010 + len(f))
        if f in ("east", "west"):
            near_front = face.col >= 12 if f == "east" else face.col <= 3
            frost_hair(face, 7020 + len(f), mask=~near_front | (face.row <= 4))
        else:
            frost_hair(face, 7020 + len(f))
    skin_tone(skin.face("head", "down"), SKIN_D, 7030)
    for face in skin.each("hat"):
        face.clear()
    # silver tiara band on the hat layer
    hf = skin.face("hat", "north")
    rows(hf, 1, 1, SILVER)
    rows(hf, 2, 2, SILVER_D)
    hf.set(1, 7, ICE_L)
    hf.set(1, 8, ICE_L)
    for f in ("east", "west", "south"):
        face = skin.face("hat", f)
        frost_hair(face, 7040 + len(f))
        if f != "south":
            near_front = face.col >= 12 if f == "east" else face.col <= 3
            face.clear(near_front & (face.row >= 1))
        face.clear(face.row >= 12)
        face.clear((face.row == 11) & (face.col % 3 == 0))
    frost_hair(skin.face("hat", "up"), 7050)


def ice(face, seed):
    """Faceted ice: bright upper half, deeper cyan below, one hard glint."""
    t = np.clip(face.row / max(face.h - 1, 1) + 0.25 * (face.col / max(face.w - 1, 1)) - 0.1, 0, 1)
    gradient(face, [(0, ICE_L), (0.35, ICE), (0.8, ICE_D), (1, ICE_X)], t=t)
    face.shade(noise((face.h, face.w), seed, 0.02))


def paint_ice(skin):
    for name in ("tiaraMid", "tiaraR", "shoulderR"):
        for face in skin.each(name):
            ice(face, 7100 + face.w + face.h)
        for f in SIDES:
            face = skin.face(name, f)
            face.fill(ICE_L, (face.col == 0) & (face.row < face.h - 1))
            face.clear((face.row == 0) & (face.col != face.w // 2) & (face.col != (face.w - 1) // 2))
        skin.face(name, "up").clear()
    # ponytail
    for name in ("pony", "ponyTip"):
        for face in skin.each(name):
            frost_hair(face, 7110 + face.w + face.h)
    tip = skin.face("ponyTip", "west")
    tip.clear((tip.row + tip.col) % 3 == 0)
    for face in skin.each("ponyTie"):
        face.fill(ICE)
        face.fill(ICE_L, face.row == 0)
        face.fill(ICE_D, face.row == face.h - 1)


def snowflake(face, top, left, color, hub):
    flake = [
        "C.C.C",
        ".CCC.",
        "CCHCC",
        ".CCC.",
        "C.C.C",
    ]
    face.stamp(flake, {"C": color, "H": hub}, top=top, left=left)


def dress(face, seed):
    cloth(face, TEAL, seed, var=0.04, fold=0.03)
    t = face.row / max(face.h - 1, 1)
    face.shade(1 + 0.15 * (1 - t))


def paint_body(skin):
    front = skin.face("body", "north")
    dress(front, 7200)
    neck = (front.row <= 2) & (front.col >= 3) & (front.col <= 12)
    tmp = front.rgba.copy()
    skin_tone(front, SKIN, 7201)
    front.rgba = np.where(neck[..., None], front.rgba, tmp)
    rows(front, 3, 3, FUR, (front.col >= 2) & (front.col <= 13))
    front.stamp([
        ".C..C.",
        "C.CC.C",
        ".CHHC.",
        ".CHHC.",
        "C.CC.C",
        ".C..C.",
    ], {"C": ICE_L, "H": ICE_D}, top=6, left=5)
    for f in ("east", "west", "south"):
        face = skin.face("body", f)
        dress(face, 7210 + len(f))
        rows(face, 0, 2, SKIN)
        rows(face, 3, 3, FUR)
    for f in SIDES:
        face = skin.face("body", f)
        rows(face, 15, 16, VIOLET)
        rows(face, 16, 16, VIOLET_D)
    back = skin.face("body", "south")
    snowflake(back, 7, 5, ICE_D, ICE_L)
    skin_tone(skin.face("body", "up"), SKIN, 7220)
    cloth(skin.face("body", "down"), TEAL_D, 7221)
    for face in skin.each("jacket"):
        face.clear()
    # frost sparkles scattered on the bodice
    jk = skin.face("jacket", "north")
    for r, c in ((5, 2), (9, 13), (12, 3), (13, 11)):
        jk.set(r, c, ICE_L)

    for face in skin.each("skirt"):
        dress(face, 7230 + face.w + face.h)
    for f in SIDES:
        face = skin.face("skirt", f)
        face.shade(1 + 0.1 * np.sin(face.col * 1.4))
        rows(face, 0, 0, VIOLET)
        # icicles hanging off the hem
        ice_band = face.row >= face.h - 2
        face.fill(ICE, ice_band)
        face.fill(ICE_L, (face.row == face.h - 2) & (face.col % 2 == 0))
        face.clear((face.row == face.h - 1) & (face.col % 3 != 1))
    skin.face("skirt", "up").fill(TEAL_D)
    skin.face("skirt", "down").fill(TEAL_D)


def paint_arms(skin):
    for arm, slv, seed in (("rightArm", "rightSleeve", 7300), ("leftArm", "leftSleeve", 7310)):
        for f in SIDES + ("up", "down"):
            skin_tone(skin.face(arm, f), SKIN, seed + len(f))
        for f in SIDES:
            face = skin.face(arm, f)
            # sheer teal sleeves to the wrist with frosty cuffs
            cloth(face, TEAL_L, seed + 10 + len(f), var=0.04, fold=0.03, mask=face.row <= 17)
            rows(face, 0, 1, TEAL)
            rows(face, 17, 18, FUR)
            rows(face, 18, 18, FUR_D)
            if f == "north":
                face.set(9, face.w // 2, ICE_L)
                face.set(13, face.w // 2, ICE_L)
        skin.face(arm, "up").fill(TEAL)
        for face in skin.each(slv):
            face.clear()
        for f in SIDES:
            face = skin.face(slv, f)
            rows(face, 17, 18, FUR)
            face.clear((face.row == 18) & (face.col % 2 == 0))


def paint_legs(skin, boot_h):
    for leg, pants, seed in (("rightLeg", "rightPants", 7400), ("leftLeg", "leftPants", 7410)):
        for f in SIDES:
            face = skin.face(leg, f)
            # pale tights with a frost sparkle
            skin_tone(face, (210, 236, 246), seed + len(f), var=0.02)
            face.fill(ICE_L, (face.row % 5 == 2) & (face.col % 4 == (face.row // 5) % 4))
        skin.face(leg, "up").fill(TEAL_D)
        skin.face(leg, "down").fill(FUR_D)
        for face in skin.each(pants):
            face.clear()
        # fluffy boot cuffs
        for f in SIDES:
            face = skin.face(pants, f)
            rows(face, 14, 16, FUR)
            rows(face, 16, 16, FUR_D)
            face.clear((face.row == 14) & (face.col % 2 == 1))
    clear_under_shoes(skin, boot_h)


def paint_boots(skin):
    for side in ("right", "left"):
        shoe = f"{side}Shoe"
        for face in skin.each(shoe):
            gradient(face, [(0, FUR), (1, FUR_D)])
            face.shade(noise((face.h, face.w), 7500 + face.w, 0.02))
        for f in SIDES:
            face = skin.face(shoe, f)
            rows(face, face.h - 2, face.h - 2, SILVER)
            rows(face, face.h - 1, face.h - 1, SILVER_D)
        toe = skin.face(shoe, "north")
        snowflake(toe, 0, toe.w // 2 - 2, ICE_D, ICE_X)
        skin.face(shoe, "down").fill(SILVER_D)
