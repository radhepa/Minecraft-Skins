"""Hotaru the Academy Hopeful: the village's most eager academy kid, newly
handed his headband and determined to prove it. Tousled chestnut hair,
bright amber eyes and a big grin with a band-aid on one cheek, a fluttering
coral scarf knotted at the side, a teal tunic with a glowing soul-firefly on the back, khaki
shorts with a patched knee, a thigh holster and a little jar at his hip
holding a soul-firefly from the Sift's meadows.
"""

import numpy as np

from paintkit import SIDES, box, clear_under_shoes, cloth, hair, rows, skin_tone
from skinlib import Skin, add_standard_body, noise

from .shinobi import (EYE_ART, add_headband, add_holster, add_sandals, anime_eyes,
                      paint_headband, paint_holster, paint_sandals, wraps)

ID = "geometry.LandOfTheHiddenSift.Hotaru"
TEXTURE = "hotaru.png"
NAME = "Hotaru the Academy Hopeful"
LOC = "Hotaru"
DETAILS = [
    ("face", "Village headband + band-aid grin", {"yaw": 18, "pitch": 4, "dist": 46, "target": 28, "fov": 30}),
    ("jar", "Soul-firefly jar", {"yaw": -40, "pitch": 6, "dist": 50, "target": 14, "fov": 30}),
    ("back34", "Soul-firefly emblem", {"yaw": 160, "pitch": 10}),
]

SKIN = (246, 206, 168)
SKIN_D = (222, 172, 134)
HAIR = (138, 80, 44)
HAIR_D = (88, 46, 24)
HAIR_L = (184, 118, 66)
LASH = (52, 30, 20)
EYE_D = (150, 78, 18)
EYE = (232, 150, 36)
EYE_L = (255, 216, 112)
PUPIL = (70, 30, 10)
WHITE = (255, 255, 255)
MOUTH = (124, 44, 36)
TONGUE = (232, 100, 96)
PATCH = (244, 224, 192)
PATCH_D = (218, 190, 150)
SCARF = (248, 124, 138)
SCARF_D = (204, 80, 102)
SCARF_L = (255, 178, 184)
TEAL = (46, 122, 128)
TEAL_D = (28, 82, 90)
TEAL_L = (80, 164, 166)
FLY = (226, 255, 120)
FLY_C = (255, 255, 220)
KHAKI = (182, 156, 108)
KHAKI_D = (144, 118, 76)
GLASS = (190, 236, 240)
GLASS_D = (130, 186, 196)
CORK = (150, 104, 62)
SANDAL = (46, 78, 92)
SANDAL_D = (26, 46, 56)


def build():
    skin = Skin(ID)
    add_standard_body(skin)
    add_headband(skin, yc=30.0)
    # scarf wrapped round the shoulders, knotted on one side with two tails
    skin.acc("scarf", "body", [-4.25, 21.75, -2.5], [8.5, 2.5, 5], lowres=("up", "down"), first=True)
    skin.acc("scarfTailR", "body", [1.0, 15.5, -3.0], [2, 6.5, 0.5], faces=("north", "south", "east", "west"),
             lowres=("east", "west"), rotation=[-8, 0, -6], pivot=[2.0, 22.0, -2.75])
    skin.acc("scarfTailL", "body", [2.5, 16.5, -3.1], [2, 6.5, 0.5], like="scarfTailR",
             rotation=[-14, 0, 10], pivot=[3.5, 23.0, -2.85])
    # the soul-firefly jar on his belt
    skin.acc("jar", "body", [2.6, 12.0, -2.8], [1.5, 1.75, 1.5], lowres=("down",))
    skin.acc("cork", "body", [2.85, 13.75, -2.55], [1, 0.5, 1], lowres=SIDES + ("up", "down"))
    add_holster(skin, "right")
    h = add_sandals(skin)
    paint_head(skin)
    paint_gear(skin)
    paint_body(skin)
    paint_arms(skin)
    paint_legs(skin, h)
    paint_sandals(skin, SANDAL, SANDAL_D, SKIN, SKIN_D)
    return skin


def chestnut(face, seed, mask=None):
    hair(face, HAIR, HAIR_D, HAIR_L, seed, mask=mask, shine=(206, 142, 86))


def paint_head(skin):
    front = skin.face("head", "north")
    skin_tone(front, SKIN, 4000, var=0.012)
    chestnut(front, 4001, mask=front.row <= 6)
    anime_eyes(front, 7, EYE_ART, {"L": LASH, "D": EYE_D, "E": EYE, "P": PUPIL,
                                   "G": WHITE, "H": EYE_L})
    front.set(11, 7, SKIN_D)
    front.stamp([
        "MWWWWM",
        ".MTTM.",
        "..MM..",
    ], {"M": MOUTH, "W": WHITE, "T": TONGUE}, top=12, left=5)
    # band-aid across his left cheek
    front.stamp(["PQQP", "PQQP"], {"P": PATCH, "Q": PATCH_D}, top=11, left=11)
    front.set(11, 12, (250, 236, 210))
    for f in ("east", "west", "south", "up"):
        face = skin.face("head", f)
        skin_tone(face, SKIN, 4010 + len(f))
        if f in ("south", "up"):
            chestnut(face, 4020 + len(f))
        else:
            ear = (face.row >= 8) & (face.row <= 11) & (np.abs(face.Z + 0.5) <= 1.5)
            chestnut(face, 4030 + len(f), mask=((face.Z > -1) | (face.row <= 6)) & ~ear)
            face.fill(SKIN_D, ear & (np.abs(face.Z + 0.5) <= 0.6) & (face.row >= 9) & (face.row <= 10))
    skin_tone(skin.face("head", "down"), SKIN_D, 4040)

    # hat layer: tousled hair with pointed locks of fringe over the band
    for face in skin.each("hat"):
        face.clear()
    chestnut(skin.face("hat", "up"), 4050)
    hf = skin.face("hat", "north")
    chestnut(hf, 4051)
    fringe = np.array([9, 8, 6, 3, 5, 3, 2, 4, 2, 2, 4, 3, 5, 6, 8, 9])
    hf.clear(hf.row > fringe[hf.col])
    for f in ("east", "west", "south"):
        face = skin.face("hat", f)
        chestnut(face, 4052 + len(f))
        bottom = 11 + (face.col % 3 == 1) - (face.col % 4 == 0)
        face.clear(face.row > bottom)
        if f != "south":
            face.clear((face.Z < -1.0) & (face.Z > -3.8) & (face.row > 5))
    paint_headband(skin)


def paint_gear(skin):
    for face in skin.each("scarf"):
        cloth(face, SCARF, 4100 + face.w, var=0.04, fold=0.12, freq=1.6)
        face.fill(SCARF_L, face.row == 0)
        face.fill(SCARF_D, face.row == face.h - 1)
    knot = skin.face("scarf", "north")
    knot.fill(SCARF_D, box(knot, 1, 11, 3, 13))        # where it's tied
    for f in ("north", "south", "east", "west"):
        face = skin.face("scarfTailR", f)
        cloth(face, SCARF, 4110 + len(f), var=0.04, fold=0.1, freq=1.3)
        face.fill(SCARF_L, (face.row % 6 == 0))
        face.fill(SCARF_D, face.row >= face.h - 2)
        face.clear((face.row == face.h - 1) & (face.col % 2 == 1))   # fringed ends
    for f in SIDES:
        face = skin.face("jar", f)
        face.fill(GLASS)
        face.fill(GLASS_D, (face.col == face.w - 1) | (face.row == face.h - 1))
        face.fill((240, 252, 255), (face.col == 0) & (face.row <= 1))
        face.set(face.h // 2, face.w // 2, FLY_C)
        face.set(face.h // 2 + 1, face.w // 2, FLY)
        face.set(face.h // 2, face.w // 2 - 1, FLY)
    skin.face("jar", "up").fill(GLASS)
    skin.face("jar", "down").fill(GLASS_D)
    for face in skin.each("cork"):
        face.fill(CORK)


def firefly(face, top, left):
    bug = [
        ".WW..WW.",
        "WWW..WWW",
        ".WWBBWW.",
        "...BB...",
        "..GGGG..",
        "..GCCG..",
        "...GG...",
    ]
    face.stamp(bug, {"W": (196, 240, 234), "B": TEAL_D, "G": FLY, "C": FLY_C}, top=top, left=left)


def paint_body(skin):
    for f in SIDES + ("up", "down"):
        cloth(skin.face("body", f), TEAL, 4200 + len(f), var=0.04, fold=0.05)
    for f in SIDES:
        face = skin.face("body", f)
        rows(face, 17, 18, TEAL_D)
        rows(face, 19, 20, (70, 58, 46))              # belt
        rows(face, 21, 23, KHAKI)
    front = skin.face("body", "north")
    # wrap-front tunic: a diagonal seam and a trim line
    for r in range(4, 17):
        c = 4 + (r - 4) // 2
        front.set(r, c, TEAL_D)
        front.set(r, c + 1, TEAL_L)
    front.fill((180, 150, 90), box(front, 19, 7, 20, 8))   # belt buckle
    firefly(skin.face("body", "south"), 6, 4)
    for face in skin.each("jacket"):
        face.clear()
    for f in SIDES:
        face = skin.face("jacket", f)
        face.fill(TEAL_D, face.row == 18)
        face.fill(TEAL_L, face.row == 17)


def paint_arms(skin):
    for arm, slv, seed in (("rightArm", "rightSleeve", 4300), ("leftArm", "leftSleeve", 4310)):
        for f in SIDES + ("up", "down"):
            skin_tone(skin.face(arm, f), SKIN, seed + len(f), var=0.02)
        for f in SIDES:
            face = skin.face(arm, f)
            cloth(face, TEAL, seed + 5 + len(f), var=0.04, fold=0.04, mask=face.row <= 7)
            rows(face, 7, 7, TEAL_D)
            wraps(face, 17, 20)
        skin.face(arm, "up").fill(TEAL)
        skin.face(arm, "down").fill(SKIN_D)
        for face in skin.each(slv):
            face.clear()
        for f in SIDES:
            face = skin.face(slv, f)
            rows(face, 6, 7, TEAL_L)
            rows(face, 7, 7, TEAL_D)


def paint_legs(skin, boot_h):
    for leg, pants, seed in (("rightLeg", "rightPants", 4400), ("leftLeg", "leftPants", 4410)):
        for f in SIDES:
            face = skin.face(leg, f)
            skin_tone(face, SKIN, seed + len(f), var=0.02)
            cloth(face, KHAKI, seed + 5 + len(f), var=0.05, fold=0.06, mask=face.row <= 9)
            rows(face, 9, 9, KHAKI_D)
        skin.face(leg, "up").fill(KHAKI)
        skin.face(leg, "down").fill(SKIN_D)
        for face in skin.each(pants):
            face.clear()
        for f in SIDES:
            face = skin.face(pants, f)
            rows(face, 8, 9, (196, 172, 124))         # rolled cuffs
            rows(face, 9, 9, KHAKI_D)
            wraps(face, 17, 19)
        # pocket on the outer side
        out = skin.face(leg, "east" if leg == "rightLeg" else "west")
        out.fill(KHAKI_D, box(out, 2, 1, 6, 6) & ~box(out, 3, 2, 5, 5))
    # patched knee
    knee = skin.face("leftPants", "north")
    knee.fill(SCARF_D, box(knee, 10, 2, 12, 5))
    knee.fill(SCARF, box(knee, 11, 3, 11, 4))
    paint_holster(skin, "right")
    clear_under_shoes(skin, boot_h)
