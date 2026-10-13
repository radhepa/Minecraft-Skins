"""Jubei the Archivist: the village elder who keeps every scroll the Hidden
Sift has ever written, and remembers the ones that were lost. Bald on top
with a ring of white hair, bushy white brows, round spectacles, a long
white beard, a plum scholar's robe with gold trim and a sash stuffed with
scrolls, a bundle of scrolls strapped to his back and a gnarled walking cane.
"""

import numpy as np

from paintkit import SIDES, box, clear_under_shoes, cloth, rows, skin_tone
from skinlib import Skin, add_standard_body, noise

from .shinobi import EYE_SHARP, add_sandals, anime_eyes, hair_head, hair_painter, paint_sandals

ID = "geometry.LandOfTheHiddenSift.Jubei"
TEXTURE = "jubei.png"
NAME = "Jubei the Archivist"
LOC = "Jubei"
DETAILS = [
    ("face", "Spectacles + long beard", {"yaw": 22, "pitch": 4, "dist": 52, "target": 25, "fov": 30}),
    ("back34", "Bundle of scrolls", {"yaw": 160, "pitch": 14}),
    ("cane", "Walking cane", {"yaw": 50, "pitch": 4, "dist": 70, "target": 9, "fov": 30}),
]

SKIN = (232, 192, 160)
SKIN_D = (204, 160, 128)
WRINKLE = (196, 150, 120)
HAIR = (236, 236, 240)
HAIR_D = (184, 186, 196)
HAIR_L = (252, 252, 255)
LASH = (60, 44, 36)
EYE_D = (60, 64, 76)
EYE = (100, 108, 124)
EYE_L = (150, 160, 176)
WHITE = (246, 246, 244)
MOUTH = (176, 120, 104)
FRAME = (176, 136, 60)
ROBE = (92, 52, 98)
ROBE_D = (64, 34, 70)
ROBE_L = (124, 78, 130)
GOLD = (222, 178, 86)
GOLD_D = (170, 128, 52)
PAPER = (236, 224, 192)
PAPER_D = (206, 190, 150)
SEAL = (180, 60, 50)
WOOD = (110, 78, 50)
WOOD_D = (76, 52, 32)
GETA = (120, 84, 52)
GETA_D = (84, 56, 34)


def build():
    skin = Skin(ID)
    add_standard_body(skin)
    # long white beard hanging from his chin
    skin.acc("beard", "head", [-3.0, 19.5, -4.55], [6, 5, 1.25], lowres=("up", "down", "south"))
    # bundle of scrolls strapped to his back, ends showing
    skin.acc("bundle", "body", [-3.5, 14.0, 2.1], [7, 6.5, 2.5], lowres=("north", "down"), first=True)
    skin.acc("scrollA", "body", [-2.6, 20.5, 2.4], [1.5, 2.5, 1.5], lowres=SIDES + ("down",))
    skin.acc("scrollB", "body", [0.9, 20.5, 2.9], [1.5, 1.75, 1.5], like="scrollA")
    # two scrolls tucked in his sash
    skin.acc("tucked", "body", [1.2, 12.4, -2.7], [1.25, 4, 1.25], lowres=SIDES + ("up", "down"),
             rotation=[0, 0, -18], pivot=[1.8, 14, -2.0])
    # walking cane in his right hand
    skin.acc("cane", "rightArm", [-6.4, 0.0, -0.4], [0.8, 13, 0.8], lowres=SIDES + ("up", "down"))
    skin.acc("knob", "rightArm", [-6.75, 12.6, -0.75], [1.5, 1.25, 1.5], lowres=SIDES + ("up", "down"))
    h = add_sandals(skin)
    paint_head(skin)
    paint_gear(skin)
    paint_body(skin)
    paint_arms(skin)
    paint_legs(skin, h)
    paint_sandals(skin, GETA, GETA_D, SKIN, SKIN_D)
    return skin


def white(face, seed, mask=None):
    hair_painter(HAIR, HAIR_D, HAIR_L)(face, seed, mask)


def paint_head(skin):
    hair_head(skin, white, 13000, SKIN, SKIN_D, [-1] * 16, back_bottom=12)
    # bald on top: skin over the crown, white hair only round the sides and back
    front = skin.face("head", "north")
    skin_tone(front, SKIN, 13001, var=0.012)
    up = skin.face("head", "up")
    skin_tone(up, SKIN, 13002, var=0.012)
    up.shade(1.04, (np.abs(up.row - 7) < 3) & (np.abs(up.col - 6) < 2))       # shine
    for f in ("east", "west", "south"):
        face = skin.face("head", f)
        old = face.rgba.copy()
        skin_tone(face, SKIN, 13003 + len(f), var=0.012)
        face.rgba = np.where((face.row >= 4)[..., None], old, face.rgba)
    for face in skin.each("hat"):
        face.clear()
    for f in ("east", "west", "south"):
        face = skin.face("hat", f)
        white(face, 13010 + len(f), (face.row >= 5) & (face.row <= 12))
        if f != "south":
            face.clear(face.Z < -1.5)
    # forehead lines, bushy brows, round spectacles
    for c in range(4, 12):
        front.set(3, c, WRINKLE)
        if 5 <= c <= 10:
            front.set(5, c, WRINKLE)
    for left in (1, 10):
        for c in range(left, left + 5):
            front.set(7, c, HAIR_D)
            front.set(6, c, HAIR) if c % 2 == 0 else None
    anime_eyes(front, 8, EYE_SHARP, {"L": LASH, "W": WHITE, "D": EYE_D, "E": EYE, "H": EYE_L,
                                     "G": EYE_L}, lefts=(2, 10))
    for left in (1, 9):
        rows(front, 8, 8, FRAME, (front.col >= left) & (front.col <= left + 5))
        rows(front, 11, 11, FRAME, (front.col >= left + 1) & (front.col <= left + 4))
        for r in (9, 10):
            front.set(r, left, FRAME)
            front.set(r, left + 5, FRAME)
    front.set(8, 7, FRAME)
    front.set(8, 8, FRAME)
    for r, c in ((9, 0), (9, 15)):
        front.set(r, c, WRINKLE)
    # moustache and the top of the beard
    rows(front, 12, 15, HAIR, (front.col >= 4) & (front.col <= 11))
    front.fill(HAIR_D, (front.row == 12) & ((front.col == 4) | (front.col == 11)))
    front.fill(MOUTH, (front.row == 13) & (front.col >= 7) & (front.col <= 8))
    for face in skin.each("beard"):
        white(face, 13020 + len(face.face))
    b = skin.face("beard", "north")
    taper = np.abs(b.col + 0.5 - b.w / 2) > (b.w / 2) * (1 - 0.06 * np.maximum(b.row - 4, 0))
    b.clear(taper)
    b.clear((b.row == b.h - 1) & (b.col % 2 == 0))


def paint_gear(skin):
    for face in skin.each("bundle"):
        face.fill(PAPER_D)
    for f in ("south", "east", "west", "up"):
        face = skin.face("bundle", f)
        face.fill(PAPER)
        # rolled scroll ends
        if f in ("south", "up"):
            face.fill(PAPER_D, (face.col % 4 == 3) | ((face.row % 4 == 3) & (f == "south")))
            face.fill(SEAL, (face.col % 4 == 1) & (face.row % 4 == 1))
        face.fill(WOOD_D, (face.row == face.h // 2) if f != "up" else (face.col == face.w // 2))
    for face in skin.each("scrollA"):
        face.fill(PAPER)
        face.fill(SEAL, face.row == 1)
    skin.face("scrollA", "up").fill(PAPER_D)
    for face in skin.each("tucked"):
        face.fill(PAPER)
        face.fill(GOLD, face.row == 0)
    for face in skin.each("cane"):
        face.fill(WOOD)
        face.fill(WOOD_D, face.row % 3 == 1)
    for face in skin.each("knob"):
        face.fill(WOOD_D)
        face.fill(WOOD, face.row == 0)


def paint_body(skin):
    for f in SIDES + ("up", "down"):
        cloth(skin.face("body", f), ROBE, 13300 + len(f), var=0.04, fold=0.05)
    front = skin.face("body", "north")
    # wrapped collar edged in gold, crossing left over right
    for r in range(0, 12):
        c = 3 + r // 2
        front.set(r, c, GOLD)
        front.set(r, 12 - r // 2, GOLD)
    front.fill(WHITE, box(front, 0, 5, 3, 10) & ~box(front, 2, 5, 3, 5) & ~box(front, 2, 10, 3, 10))
    for f in SIDES:
        face = skin.face("body", f)
        rows(face, 15, 18, GOLD)
        rows(face, 15, 15, GOLD_D)
        rows(face, 18, 18, GOLD_D)
    for face in skin.each("jacket"):
        face.clear()


def paint_arms(skin):
    for arm, slv, seed in (("rightArm", "rightSleeve", 13400), ("leftArm", "leftSleeve", 13410)):
        for f in SIDES + ("up", "down"):
            cloth(skin.face(arm, f), ROBE, seed + len(f), var=0.04, fold=0.06)
        for f in SIDES:
            face = skin.face(arm, f)
            rows(face, 21, 23, SKIN)
        skin.face(arm, "down").fill(SKIN_D)
        for face in skin.each(slv):
            face.clear()
        for f in SIDES:
            face = skin.face(slv, f)
            # wide sleeve cuffs with gold trim
            rows(face, 16, 20, ROBE_L)
            rows(face, 19, 20, GOLD)


def paint_legs(skin, boot_h):
    for leg, pants, seed in (("rightLeg", "rightPants", 13500), ("leftLeg", "leftPants", 13510)):
        for f in SIDES:
            cloth(skin.face(leg, f), ROBE_D, seed + len(f), var=0.04, fold=0.05)
        skin.face(leg, "up").fill(ROBE_D)
        skin.face(leg, "down").fill(ROBE_D)
        for face in skin.each(pants):
            face.clear()
        # the robe's skirt falls to his ankles
        for f in SIDES:
            face = skin.face(pants, f)
            cloth(face, ROBE, seed + 9 + len(f), var=0.04, fold=0.05, mask=face.row <= 18)
            face.fill(GOLD, face.row == 18)
    clear_under_shoes(skin, boot_h)
