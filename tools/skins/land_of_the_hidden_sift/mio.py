"""Mio the Blub Keeper: a gentle ranger who looks after the Blubs of the
Sift's meadows, with one always riding on her shoulder. Long lilac hair with
soft bangs and face-framing locks, teal eyes, a meadow-flower hairpin, the
village headband worn round her neck, a cream wrap top with a teal obi tied
in a bow at the back, mesh sleeves and stockings, armguards and sandals.
"""

import numpy as np

from paintkit import SIDES, box, clear_under_shoes, cloth, gradient, hair, rows, skin_tone
from skinlib import Skin, add_standard_body, noise

from .shinobi import (EYE_SOFT, STEEL, STEEL_D, STEEL_L, add_neckband, add_sandals,
                      anime_eyes, paint_neckband, paint_sandals, wraps)

ID = "geometry.LandOfTheHiddenSift.Mio"
TEXTURE = "mio.png"
NAME = "Mio the Blub Keeper"
LOC = "Mio"
DETAILS = [
    ("blub", "Her Blub companion", {"yaw": 40, "pitch": 6, "dist": 50, "target": 26, "fov": 30}),
    ("flower", "Meadow-flower hairpin", {"yaw": -60, "pitch": 6, "dist": 50, "target": 27, "fov": 30}),
    ("back34", "Long hair + obi bow", {"yaw": 160, "pitch": 10}),
]

SKIN = (250, 222, 206)
SKIN_D = (228, 190, 174)
BLUSH = (250, 168, 178)
MOUTH = (214, 130, 136)
HAIR = (196, 168, 232)
HAIR_D = (140, 110, 190)
HAIR_L = (216, 196, 244)
LASH = (60, 36, 70)
EYE_D = (20, 100, 106)
EYE = (46, 184, 174)
EYE_L = (170, 246, 232)
WHITE = (255, 255, 255)
CREAM = (244, 236, 216)
CREAM_D = (212, 200, 176)
OBI = (40, 140, 140)
OBI_D = (24, 96, 100)
OBI_L = (84, 186, 178)
CORD = (248, 124, 138)
SHORTS = (40, 66, 84)
SHORTS_D = (26, 44, 58)
MESH = (150, 116, 124)
PETAL = (96, 214, 194)
PETAL_D = (50, 160, 150)
BLUB = (110, 190, 255)
BLUB_L = (190, 232, 255)
BLUB_D = (60, 130, 230)
BLUB_X = (40, 90, 190)
SANDAL = (64, 54, 80)
SANDAL_D = (40, 32, 52)


def build():
    skin = Skin(ID, slim=True)
    add_standard_body(skin)
    # long hair down her back and locks framing her face
    skin.acc("backHairR", "head", [-4.3, 17.5, 3.9], [4.3, 7, 0.9], lowres=("north", "up", "down", "east", "west"))
    skin.acc("backHairL", "head", [0.0, 17.5, 3.9], [4.3, 7, 0.9], lowres=("north", "up", "down", "east", "west"))
    skin.acc("lockR", "head", [-4.85, 22.5, -4.4], [1, 6, 1.4], lowres=("up", "down"))
    skin.acc("lockL", "head", [3.85, 22.5, -4.4], [1, 6, 1.4], like="lockR")
    # meadow-flower hairpin on her left side
    skin.acc("flower", "head", [4.55, 29.0, -2.5], [0.25, 2.5, 2.5], faces=("west", "east"),
             pad=("west",), same={"east": "west"})
    add_neckband(skin)
    # obi bow at the back
    skin.acc("bowKnot", "body", [-1.0, 13.5, 2.0], [2, 2, 0.75], lowres=("up", "down", "east", "west"))
    skin.acc("bowR", "body", [-3.4, 13.4, 2.2], [2.5, 2.25, 0.6], rotation=[0, 0, -14],
             pivot=[-1.0, 14.5, 2.5], lowres=("up", "down", "east", "west"))
    skin.acc("bowL", "body", [0.9, 13.4, 2.2], [2.5, 2.25, 0.6], like="bowR", rotation=[0, 0, 14],
             pivot=[1.0, 14.5, 2.5])
    # the Blub riding on her right shoulder
    skin.acc("blub", "body", [-7.6, 23.6, -1.6], [3, 2.5, 3], lowres=("down",))
    skin.acc("blubEarR", "body", [-7.1, 26.0, -0.4], [0.75, 1.5, 0.5], rotation=[0, 0, -12],
             pivot=[-6.7, 26.0, -0.15], lowres=SIDES + ("up", "down"))
    skin.acc("blubEarL", "body", [-5.85, 26.0, -0.4], [0.75, 1.5, 0.5], like="blubEarR",
             rotation=[0, 0, 12], pivot=[-5.5, 26.0, -0.15])
    h = add_sandals(skin)
    paint_head(skin)
    paint_gear(skin)
    paint_body(skin)
    paint_arms(skin)
    paint_legs(skin, h)
    paint_sandals(skin, SANDAL, SANDAL_D, SKIN, SKIN_D)
    return skin


def lilac(face, seed, mask=None):
    hair(face, HAIR, HAIR_D, HAIR_L, seed, mask=mask, shine=(236, 226, 255))


def paint_head(skin):
    front = skin.face("head", "north")
    skin_tone(front, SKIN, 5000, var=0.012)
    lilac(front, 5001, mask=front.row <= 6)
    anime_eyes(front, 8, EYE_SOFT, {"L": LASH, "W": WHITE, "D": EYE_D, "E": EYE, "H": EYE_L,
                                    "G": EYE_L})
    for c in (1, 2, 13, 14):
        front.set(12, c, BLUSH)
    # a tiny soft mouth
    front.set(13, 7, MOUTH)
    front.set(13, 8, MOUTH)
    for f in ("east", "west", "south", "up"):
        face = skin.face("head", f)
        skin_tone(face, SKIN, 5010 + len(f))
        if f in ("south", "up"):
            lilac(face, 5020 + len(f))
        else:
            lilac(face, 5030 + len(f), mask=(face.Z > -2.5) | (face.row <= 6))
    skin_tone(skin.face("head", "down"), SKIN_D, 5040)

    for face in skin.each("hat"):
        face.clear()
    lilac(skin.face("hat", "up"), 5050)
    hf = skin.face("hat", "north")
    lilac(hf, 5051)
    # soft bangs, parted a little off centre, with longer side pieces
    fringe = np.array([13, 12, 8, 7, 7, 6, 7, 5, 4, 6, 7, 7, 7, 8, 12, 13])
    hf.clear(hf.row > fringe[hf.col])
    hf.clear((hf.row > fringe[hf.col] - 1) & (hf.col % 3 == 0) & (hf.col > 1) & (hf.col < 14))
    for f in ("east", "west", "south"):
        face = skin.face("hat", f)
        lilac(face, 5052 + len(f))
        if f != "south":
            face.clear((face.Z < -1.5) & (face.Z > -4.0) & (face.row > 4))
    for k, part in enumerate(("backHairR", "backHairL")):
        for face in skin.each(part):
            lilac(face, 5060 + 7 * k + len(face.face))
        back = skin.face(part, "south")
        tips = 12 + ((back.col + k) % 4 == 1) + ((back.col + k) % 4 == 2) - ((back.col + 2 * k) % 5 == 0)
        back.clear(back.row > tips)
    for face in skin.each("lockR"):
        lilac(face, 5070 + len(face.face))
        face.clear((face.row == face.h - 1) & (face.col % 2 == 0))


def paint_gear(skin):
    fl = skin.face("flower", "west")
    fl.clear()
    fl.stamp([
        ".PP.",
        "PCCP",
        "PCCP",
        ".PP.",
    ] if fl.w == 4 else [
        "..P..",
        ".PPP.",
        "PPCPP",
        ".PPP.",
        "..P..",
    ], {"P": PETAL, "C": CORD})
    fl.fill(PETAL_D, (fl.rgba[..., 3] > 0) & (fl.row == fl.h - 1))
    for name in ("bowKnot", "bowR"):
        for face in skin.each(name):
            cloth(face, OBI, 5100 + face.w, var=0.04, fold=0.08, freq=1.5)
            face.fill(OBI_L, face.row == 0)
            face.fill(OBI_D, face.row == face.h - 1)
    skin.face("bowKnot", "south").fill(CORD, box(skin.face("bowKnot", "south"), 1, 0, 2, 3))
    # the Blub: round blue jelly with a glossy top, big eyes and tiny ears
    for face in skin.each("blub"):
        gradient(face, [(0, BLUB_L), (0.4, BLUB), (1, BLUB_D)])
        if face.face == "up":
            face.fill(BLUB_L)
            face.fill(WHITE, box(face, 1, 1, 1, 2))
        if face.face == "down":
            face.fill(BLUB_D)
        if face.face in SIDES:
            face.fill(BLUB_X, face.row == face.h - 1)
            face.fill((236, 248, 255), (face.row == 1) & (face.col == 1))
    bf = skin.face("blub", "north")
    bf.stamp(["E..E", "E..E", ".mm."], {"E": (20, 26, 50), "m": BLUB_X}, top=1, left=1)
    bf.set(1, 1, WHITE)
    bf.set(1, 4, WHITE)
    for face in skin.each("blubEarR"):
        face.fill(BLUB)


def paint_body(skin):
    for f in SIDES + ("up", "down"):
        cloth(skin.face("body", f), CREAM, 5200 + len(f), var=0.03, fold=0.05)
    for f in SIDES:
        face = skin.face("body", f)
        rows(face, 11, 16, OBI)
        rows(face, 11, 11, OBI_L)
        rows(face, 16, 16, OBI_D)
        rows(face, 13, 13, CORD)
        rows(face, 17, 23, SHORTS)
        rows(face, 17, 17, SHORTS_D)
    front = skin.face("body", "north")
    # wrap top: the left panel crosses over the right
    for r in range(6, 11):
        c = 3 + (r - 6)
        front.set(r, c, CREAM_D)
        front.set(r, 15 - c, CREAM_D)
    front.fill(SKIN, box(front, 6, 6, 7, 9) & ~((front.row == 7) & ((front.col == 6) | (front.col == 9))))
    front.fill(CORD, box(front, 13, 10, 15, 11))     # cord knot
    for face in skin.each("jacket"):
        face.clear()
    paint_neckband(skin)


def mesh(face, mask):
    face.fill(MESH, mask & (((face.row + face.col) % 4 == 0) | ((face.row - face.col) % 4 == 0)))


def paint_arms(skin):
    for arm, slv, seed in (("rightArm", "rightSleeve", 5300), ("leftArm", "leftSleeve", 5310)):
        for f in SIDES + ("up", "down"):
            skin_tone(skin.face(arm, f), SKIN, seed + len(f), var=0.02)
        for f in SIDES:
            face = skin.face(arm, f)
            cloth(face, CREAM, seed + 5 + len(f), var=0.03, fold=0.04, mask=face.row <= 6)
            rows(face, 6, 6, CREAM_D)
            mesh(face, (face.row >= 7) & (face.row <= 14))
            rows(face, 15, 19, OBI_D)
            rows(face, 15, 15, OBI_L)
            rows(face, 17, 17, STEEL)
        skin.face(arm, "up").fill(CREAM)
        skin.face(arm, "down").fill(SKIN_D)
        for face in skin.each(slv):
            face.clear()
        for f in SIDES:
            face = skin.face(slv, f)
            rows(face, 5, 6, CREAM)
            rows(face, 6, 6, CORD)
            rows(face, 16, 18, STEEL_D)
            rows(face, 16, 16, STEEL_L)


def paint_legs(skin, boot_h):
    for leg, pants, seed in (("rightLeg", "rightPants", 5400), ("leftLeg", "leftPants", 5410)):
        for f in SIDES:
            face = skin.face(leg, f)
            skin_tone(face, SKIN, seed + len(f), var=0.02)
            cloth(face, SHORTS, seed + 5 + len(f), var=0.04, fold=0.05, mask=face.row <= 4)
            mesh(face, (face.row >= 6) & (face.row <= 15))
            rows(face, 5, 5, MESH)
        skin.face(leg, "up").fill(SHORTS)
        skin.face(leg, "down").fill(SKIN_D)
        for face in skin.each(pants):
            face.clear()
        for f in SIDES:
            face = skin.face(pants, f)
            rows(face, 3, 4, SHORTS_D)
            wraps(face, 16, 19)
    clear_under_shoes(skin, boot_h)
