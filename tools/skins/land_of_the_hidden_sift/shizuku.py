"""Shizuku the Ichor Weaver: the Soul-Infused poisoner, who draws the
glowing coral ichor out of the Sift's toxic pools and spins it into traps.
Plum hair in a sleek high bun pinned with two ichor-tipped hairpins, a
blunt hime-cut fringe with long side locks fading to glowing coral, glowing
pink eyes, dark lips and a beauty mark, her slashed headband worn round her
neck, a high-collared plum dress dripping with ichor, long dark gloves,
a bandolier of ichor vials and stained tights.
"""

import numpy as np

from paintkit import SIDES, box, clear_under_shoes, cloth, gradient, rows, skin_tone
from skinlib import Skin, add_standard_body, noise

from .shinobi import (EYE_SOFT, add_neckband, add_sandals, anime_eyes, hair_head, hair_painter,
                      paint_neckband, paint_sandals)

ID = "geometry.LandOfTheHiddenSift.Shizuku"
TEXTURE = "shizuku.png"
NAME = "Shizuku the Ichor Weaver"
LOC = "Shizuku"
DETAILS = [
    ("face", "Hime cut, high bun + hairpins", {"yaw": 24, "pitch": 4, "dist": 50, "target": 26, "fov": 30}),
    ("vials", "Ichor vials", {"yaw": -30, "pitch": 6, "dist": 52, "target": 13, "fov": 30}),
    ("back34", "Dripping ichor", {"yaw": 160, "pitch": 10}),
]

SKIN = (242, 214, 208)
SKIN_D = (216, 182, 178)
HAIR = (96, 50, 96)
HAIR_D = (60, 28, 62)
HAIR_L = (138, 80, 134)
LASH = (40, 16, 40)
ICHOR = (255, 98, 150)
ICHOR_C = (255, 200, 222)
ICHOR_D = (178, 40, 104)
MOUTH = (150, 60, 110)
MARK = (90, 50, 70)
DRESS = (54, 30, 64)
DRESS_D = (34, 18, 42)
DRESS_L = (86, 52, 100)
GLOVE = (30, 22, 36)
TIGHTS = (44, 32, 54)
GLASS = (230, 214, 236)
STRAP = (74, 46, 54)
SANDAL = (40, 26, 46)
SANDAL_D = (22, 14, 28)


def build():
    skin = Skin(ID, slim=True)
    add_standard_body(skin)
    # sleek high bun with two crossed hairpins
    skin.acc("bun", "head", [-1.75, 31.75, 0.25], [3.5, 2.75, 3.5], lowres=("down",))
    for side, rz in (("R", 68), ("L", -68)):
        kw = dict(like="pinR") if side == "L" else dict(lowres=SIDES + ("up", "down"))
        skin.acc(f"pin{side}", "head", [-0.25, 30.5, 1.75], [0.5, 5.5, 0.5], rotation=[0, 0, rz],
                 pivot=[0, 33.0, 2.0], **kw)
    # long side locks framing her face, hime-cut
    skin.acc("lockR", "head", [-4.85, 21.0, -4.4], [1.0, 7.5, 1.4], lowres=("up", "down"))
    skin.acc("lockL", "head", [3.85, 21.0, -4.4], [1.0, 7.5, 1.4], like="lockR")
    add_neckband(skin)
    # bandolier of ichor vials across her hips
    for i, x in enumerate((-3.4, -1.9, -0.4)):
        kw = dict(like="vial") if i else dict(lowres=("down",))
        skin.acc("vial" if i == 0 else f"vial{i}", "body", [x, 12.6, -2.75], [0.9, 1.75, 0.9], **kw)
    h = add_sandals(skin)
    paint_head(skin)
    paint_gear(skin)
    paint_body(skin)
    paint_arms(skin)
    paint_legs(skin, h)
    paint_sandals(skin, SANDAL, SANDAL_D, SKIN, SKIN_D)
    return skin


def ombre(face, seed, mask=None, fade_from=None):
    """Plum hair whose strand ends glow coral, by model height."""
    old = face.rgba.copy()
    hair_painter(HAIR, HAIR_D, HAIR_L)(face, seed, None)
    if fade_from is not None:
        t = np.clip((fade_from - face.Y) / 4.0, 0, 1)
        tint = np.array(ICHOR, float)
        face.rgba[..., :3] = face.rgba[..., :3] * (1 - t[..., None] * 0.75) + tint * t[..., None] * 0.75
    if mask is not None:
        face.rgba = np.where(mask[..., None], face.rgba, old)


def paint_head(skin):
    plum = lambda face, seed, mask: ombre(face, seed, mask, fade_from=26.0)
    # blunt, straight fringe; the hair is swept up into the bun behind
    hair_head(skin, plum, 15000, SKIN, SKIN_D, [6] * 16, back_bottom=11, long_sides=True)
    front = skin.face("head", "north")
    anime_eyes(front, 8, EYE_SOFT, {"L": LASH, "W": (250, 240, 246), "D": ICHOR_D, "E": ICHOR,
                                    "H": ICHOR_C, "G": ICHOR_C})
    # dark lips and a beauty mark
    for c in (7, 8):
        front.set(13, c, MOUTH)
    front.set(12, 12, MARK)
    for face in skin.each("bun"):
        ombre(face, 15100 + len(face.face))
    skin.face("bun", "up").fill(HAIR_D, np.abs(skin.face("bun", "up").col - 3.5) < 0.6)
    for face in skin.each("pinR"):
        face.fill((214, 170, 86))
        face.fill(ICHOR, face.row >= face.h - 2)
        face.fill(ICHOR_C, face.row == face.h - 1)
    for face in skin.each("lockR"):
        ombre(face, 15110 + len(face.face), fade_from=25.0)
        face.clear((face.row == face.h - 1) & (face.col % 2 == 0))


def drips(face, top, seed, count=5, colour=ICHOR):
    """Glowing ichor running down from row `top`."""
    rs = np.random.RandomState(seed)
    for c in rs.choice(face.w, size=min(count, face.w), replace=False):
        length = rs.randint(2, 6)
        for r in range(top, min(face.h, top + length)):
            face.set(r, c, ICHOR_C if r == top + length - 1 else colour)


def paint_gear(skin):
    for face in skin.each("vial"):
        face.fill(GLASS)
        face.fill(ICHOR, face.row >= 1)
        face.fill(ICHOR_C, (face.row == 1) & (face.col == 0))
    skin.face("vial", "up").fill((120, 90, 70))


def paint_body(skin):
    for f in SIDES + ("up", "down"):
        cloth(skin.face("body", f), DRESS, 15200 + len(f), var=0.04, fold=0.05)
    for f in SIDES:
        face = skin.face("body", f)
        rows(face, 6, 6, DRESS_L)
        drips(face, 7, 15210 + len(f), count=4)
        rows(face, 17, 18, STRAP)
        rows(face, 19, 23, DRESS_D)
    front = skin.face("body", "north")
    front.fill(DRESS_L, (front.col == 9) & (front.row >= 7) & (front.row <= 16))   # side fastening
    for r in (8, 11, 14):
        front.set(r, 10, ICHOR)
    for face in skin.each("jacket"):
        face.clear()
    paint_neckband(skin, slashed=True)


def paint_arms(skin):
    for arm, slv, seed in (("rightArm", "rightSleeve", 15300), ("leftArm", "leftSleeve", 15310)):
        for f in SIDES + ("up", "down"):
            skin_tone(skin.face(arm, f), SKIN, seed + len(f), var=0.02)
        for f in SIDES:
            face = skin.face(arm, f)
            cloth(face, DRESS, seed + 5 + len(f), var=0.04, fold=0.04, mask=face.row <= 4)
            cloth(face, GLOVE, seed + 9 + len(f), var=0.04, fold=0.04, mask=face.row >= 9)
            rows(face, 9, 9, DRESS_L)
            drips(face, 19, seed + 20 + len(f), count=3)
        skin.face(arm, "up").fill(DRESS)
        skin.face(arm, "down").fill(ICHOR)
        for face in skin.each(slv):
            face.clear()


def paint_legs(skin, boot_h):
    for leg, pants, seed in (("rightLeg", "rightPants", 15400), ("leftLeg", "leftPants", 15410)):
        for f in SIDES:
            face = skin.face(leg, f)
            cloth(face, TIGHTS, seed + len(f), var=0.04, fold=0.04)
            # ichor stains splashed up the shins
            rs = np.random.RandomState(seed + 9 + len(f))
            face.fill(ICHOR_D, (face.row >= 15) & (rs.rand(face.h, face.w) < 0.18))
        skin.face(leg, "up").fill(TIGHTS)
        skin.face(leg, "down").fill(TIGHTS)
        for face in skin.each(pants):
            face.clear()
        # the dress skirt to mid-thigh
        for f in SIDES:
            face = skin.face(pants, f)
            cloth(face, DRESS_D, seed + 20 + len(f), var=0.04, fold=0.05, mask=face.row <= 6)
            face.fill(ICHOR, face.row == 6)
    clear_under_shoes(skin, boot_h)
