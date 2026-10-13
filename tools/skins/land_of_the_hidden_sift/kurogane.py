"""Kurogane the Soul-Bound: leader of the Soul-Infused, rogue ninja who
went too deep into the Sift's rifts and came back changed. Ash-pale skin
split by glowing soul cracks, long black hair parted down the middle and
tied in a low ponytail, glowing teal eyes shadowed in violet, her
village headband slashed through, a long high-collared coat with a soul-flame
hem and tattered tails, a chitin pauldron torn from the Carapace and two soul
wisps drifting at her shoulders.
"""

import numpy as np

from paintkit import SIDES, box, clear_under_shoes, cloth, gradient, hair, rows, skin_tone
from skinlib import Skin, add_standard_body, noise

from .shinobi import (EYE_SOFT, add_headband, add_sandals, anime_eyes, paint_headband,
                      paint_sandals, wraps)

ID = "geometry.LandOfTheHiddenSift.Kurogane"
TEXTURE = "kurogane.png"
NAME = "Kurogane the Soul-Bound"
LOC = "Kurogane"
DETAILS = [
    ("face", "Soul cracks + slashed headband", {"yaw": 18, "pitch": 4, "dist": 48, "target": 28, "fov": 30}),
    ("pauldron", "Carapace pauldron + soul wisps", {"yaw": -45, "pitch": 10, "dist": 66, "target": 22, "fov": 30}),
    ("back34", "Soul-flame coat + ponytail", {"yaw": 160, "pitch": 10}),
]

SKIN = (212, 204, 214)
SKIN_D = (176, 166, 184)
SOUL = (80, 236, 214)
SOUL_C = (214, 255, 248)
SOUL_D = (30, 150, 150)
MARK = (128, 70, 180)
MOUTH = (150, 92, 126)
HAIR = (44, 40, 62)
HAIR_D = (22, 20, 32)
HAIR_L = (86, 78, 116)
LASH = (24, 18, 32)
COAT = (36, 32, 50)
COAT_D = (20, 18, 30)
COAT_L = (62, 56, 82)
SHIRT = (66, 64, 78)
SASH = (98, 54, 140)
SASH_L = (140, 90, 186)
CHITIN = (150, 74, 46)
CHITIN_D = (86, 38, 26)
CHITIN_L = (214, 132, 82)
GLOVE = (30, 26, 38)
PANTS = (30, 28, 40)
SANDAL = (34, 30, 44)
SANDAL_D = (18, 16, 26)
SILVER = (200, 204, 216)


def build():
    skin = Skin(ID, slim=True)
    add_standard_body(skin)
    add_headband(skin, yc=30.0)
    # low ponytail tied with a violet cord
    skin.acc("tie", "head", [-0.75, 24.6, 4.35], [1.5, 1.25, 1], lowres=SIDES + ("up", "down"))
    skin.acc("ponytail", "head", [-1.0, 18.0, 4.45], [2, 6.75, 1.5], rotation=[12, 0, 0],
             pivot=[0, 24.75, 5.2], lowres=("up", "down"))
    # long coat: tattered tails behind, open flaps in front
    for side, x in (("R", -4.25), ("L", 0.0)):
        skin.acc(f"tail{side}", "body", [x, 4.0, 1.95], [4.25, 8, 0.45],
                 lowres=("north", "up", "down", "east", "west"))
    skin.acc("flapR", "body", [-4.25, 6.0, -2.4], [3.25, 6, 0.4], lowres=("south", "up", "down", "east", "west"))
    skin.acc("flapL", "body", [1.0, 6.0, -2.4], [3.25, 6, 0.4], like="flapR")
    # chitin pauldron on the left shoulder
    skin.acc("pauldron", "leftArm", [3.5, 21.25, -2.75], [4.25, 3, 5.5], rotation=[0, 0, -10],
             pivot=[5.5, 22.5, 0.0], lowres=("down",))
    # soul wisps drifting by her shoulders
    skin.acc("wisp", "body", [-9.75, 25.5, 1.5], [1.5, 3, 1.5], faces=SIDES)
    skin.acc("wisp2", "body", [8.5, 19.5, 2.5], [1.5, 3, 1.5], like="wisp")
    h = add_sandals(skin)
    paint_head(skin)
    paint_gear(skin)
    paint_body(skin)
    paint_arms(skin)
    paint_legs(skin, h)
    paint_sandals(skin, SANDAL, SANDAL_D, SKIN, SKIN_D)
    return skin


def black_hair(face, seed, mask=None):
    hair(face, HAIR, HAIR_D, HAIR_L, seed, mask=mask, shine=(120, 110, 160))


def crack(face, path):
    """A glowing soul crack along a list of (row, col) texels."""
    for i, (r, c) in enumerate(path):
        face.set(r, c, SOUL_C if i % 3 == 1 else SOUL)
        for dr, dc in ((0, -1), (0, 1)):
            rr, cc = r + dr, c + dc
            if 0 <= rr < face.h and 0 <= cc < face.w and (rr, cc) not in path:
                px = face.rgba[rr, cc]
                if px[3] > 0 and abs(px[0] - SOUL[0]) > 20:
                    face.rgba[rr, cc, :3] = px[:3] * 0.8 + np.array(SOUL_D) * 0.2


def paint_head(skin):
    front = skin.face("head", "north")
    skin_tone(front, SKIN, 6000, var=0.012)
    black_hair(front, 6001, mask=front.row <= 6)
    # glowing lashed eyes, violet shadow beneath
    anime_eyes(front, 8, EYE_SOFT, {"L": LASH, "W": (236, 232, 244), "D": SOUL_D, "E": SOUL,
                                    "H": SOUL_C, "G": SOUL_C})
    rows(front, 12, 12, MARK, ((front.col >= 3) & (front.col <= 5)) | ((front.col >= 10) & (front.col <= 12)))
    # a thin smirk, one corner lifted, well clear of the eye shadow
    front.set(14, 6, MOUTH)
    front.set(14, 7, MOUTH)
    front.set(13, 8, MOUTH)
    # a soul crack splitting her left cheek
    crack(front, [(13, 14), (14, 13), (14, 12), (15, 12)])
    for f in ("east", "west", "south", "up"):
        face = skin.face("head", f)
        skin_tone(face, SKIN, 6010 + len(f))
        if f in ("south", "up"):
            black_hair(face, 6020 + len(f))
        else:
            black_hair(face, 6030 + len(f), mask=(face.Z > -2.5) | (face.row <= 6))
    skin_tone(skin.face("head", "down"), SKIN_D, 6040)
    crack(skin.face("head", "west"), [(9, 2), (10, 3), (11, 3), (12, 4), (13, 4), (14, 5), (15, 5)])

    for face in skin.each("hat"):
        face.clear()
    black_hair(skin.face("hat", "up"), 6050)
    hf = skin.face("hat", "north")
    black_hair(hf, 6051)
    # parted down the middle, long locks framing the face
    fringe = np.array([14, 13, 12, 9, 7, 6, 5, 3, 3, 5, 6, 7, 9, 12, 13, 14])
    hf.clear(hf.row > fringe[hf.col])
    hf.clear((hf.row > 7) & (hf.col >= 2) & (hf.col <= 13))
    for f in ("east", "west", "south"):
        face = skin.face("hat", f)
        black_hair(face, 6052 + len(f))
        if f != "south":
            face.clear((face.Z < -1.5) & (face.Z > -4.0) & (face.row > 4))
        face.clear(face.row > 13)
    paint_headband(skin, slashed=True)
    for face in skin.each("ponytail"):
        black_hair(face, 6060 + len(face.face))
    for f in SIDES:
        face = skin.face("ponytail", f)
        face.clear((face.row == face.h - 1) & (face.col % 2 == 0))
    for face in skin.each("tie"):
        face.fill(SASH)


def soul_flames(face, base_row, seed):
    """Teal soul flames licking up from the hem, edged with a bright core."""
    rs = np.random.RandomState(seed)
    heights = np.zeros(face.w, int)
    c = 0
    while c < face.w:
        w = rs.randint(2, 4)
        tip = rs.randint(2, 5)
        for k in range(w):
            if c + k < face.w:
                heights[c + k] = max(1, tip - abs(k - (w - 1) / 2) * 1.5)
        c += w
    for c in range(face.w):
        top = base_row - heights[c]
        for r in range(max(0, top), face.h):
            t = (r - top) / max(1, face.h - top)
            face.set(r, c, SOUL_D if t < 0.25 else (SOUL if t < 0.7 else SOUL_C))


def paint_gear(skin):
    for side in ("R", "L"):
        face = skin.face(f"tail{side}", "south")
        cloth(face, COAT, 6100 + len(side), var=0.04, fold=0.05)
        soul_flames(face, face.h - 3, 6110 + ord(side))
        # tattered hem
        rs = np.random.RandomState(6120 + ord(side))
        cut = rs.rand(face.w) < 0.4
        face.clear((face.row == face.h - 1) & cut)
        for f in ("north", "up", "down", "east", "west"):
            skin.face(f"tail{side}", f).fill(COAT_D)
    flap = skin.face("flapR", "north")
    cloth(flap, COAT, 6130, var=0.04, fold=0.05)
    soul_flames(flap, flap.h - 3, 6131)
    flap.fill(COAT_L, flap.col == flap.w - 1)
    for f in ("south", "up", "down", "east", "west"):
        skin.face("flapR", f).fill(COAT_D)
    for face in skin.each("pauldron"):
        gradient(face, [(0, CHITIN_L), (0.5, CHITIN), (1, CHITIN_D)])
        face.shade(noise((face.h, face.w), 6140 + face.w, 0.03))
    up = skin.face("pauldron", "up")
    # three overlapping shell plates, each glossy at its leading edge
    t = (up.col % 4) / 3
    gradient(up, [(0, CHITIN_L), (0.35, CHITIN), (1, CHITIN_D)], t=t)
    up.fill((246, 196, 140), (up.col % 4 == 0) & (up.row % 5 == 2))
    for f in SIDES:
        face = skin.face("pauldron", f)
        face.fill(CHITIN_D, (face.col % 4 == 3) | (face.row == face.h - 1))
    crack(up, [(1, 2), (2, 3), (3, 3), (4, 4), (5, 5), (6, 5), (7, 6), (8, 7)])
    for face in skin.each("wisp"):
        # a teardrop flame: bright core at the bottom, a flickering tip
        gradient(face, [(0, SOUL_D), (0.45, SOUL), (1, SOUL_C)], t=face.row / max(1, face.h - 1))
        face.clear((face.row <= 2) & (face.col != face.w // 2))
        face.clear((face.row == 0) & (face.face in ("east", "south")))
        face.fill(SOUL_C, (face.row >= face.h - 3) & (face.col == face.w // 2))


def flame_emblem(face, top, left):
    art = [
        "....S...",
        "...SS...",
        "..SSCS..",
        "..SCCS.S",
        ".SSCCSSS",
        ".SCCCCS.",
        "SSCCCCSS",
        ".SSCCSS.",
        "..SSSS..",
    ]
    face.stamp(art, {"S": SOUL, "C": SOUL_C}, top=top, left=left)


def paint_body(skin):
    for f in SIDES + ("up", "down"):
        cloth(skin.face("body", f), COAT, 6200 + len(f), var=0.04, fold=0.05)
    for f in SIDES:
        face = skin.face("body", f)
        rows(face, 18, 19, SASH)
        rows(face, 18, 18, SASH_L)
        rows(face, 20, 23, COAT)
    front = skin.face("body", "north")
    # open front over a dark shirt, with a silver clasp at the chest
    front.fill(SHIRT, box(front, 0, 6, 17, 9))
    front.fill(COAT_L, box(front, 0, 5, 23, 5) | box(front, 0, 10, 23, 10))
    front.fill(SILVER, box(front, 5, 6, 5, 9))
    crack(front, [(1, 7), (2, 8), (3, 8)])
    flame_emblem(skin.face("body", "south"), 5, 4)
    for face in skin.each("jacket"):
        face.clear()
    # tall collar with a teal lining
    for f in SIDES:
        face = skin.face("jacket", f)
        face.fill(COAT_L, face.row <= 2)
        face.fill(SOUL_D, face.row == 0)
    jk = skin.face("jacket", "north")
    jk.clear(box(jk, 0, 5, 2, 10))


def paint_arms(skin):
    for arm, slv, seed in (("rightArm", "rightSleeve", 6300), ("leftArm", "leftSleeve", 6310)):
        for f in SIDES + ("up", "down"):
            cloth(skin.face(arm, f), COAT, seed + len(f), var=0.04, fold=0.05)
        for f in SIDES:
            face = skin.face(arm, f)
            rows(face, 17, 17, SOUL_D)
            rows(face, 18, 23, GLOVE if arm == "leftArm" else SKIN)
        if arm == "rightArm":
            for f in SIDES:
                face = skin.face(arm, f)
                cloth(face, COAT, seed + 20 + len(f), var=0.04, fold=0.05, mask=face.row <= 16)
                rows(face, 17, 17, SOUL_D)
                crack(face, [(18, 1), (19, 2), (20, 2), (21, 1), (22, 2)])
        skin.face(arm, "down").fill(GLOVE if arm == "leftArm" else SKIN_D)
        for face in skin.each(slv):
            face.clear()
        for f in SIDES:
            face = skin.face(slv, f)
            rows(face, 15, 17, COAT_L)
            rows(face, 17, 17, SOUL)


def paint_legs(skin, boot_h):
    for leg, pants, seed in (("rightLeg", "rightPants", 6400), ("leftLeg", "leftPants", 6410)):
        for f in SIDES:
            cloth(skin.face(leg, f), PANTS, seed + len(f), var=0.05, fold=0.07, freq=0.9)
        skin.face(leg, "up").fill(PANTS)
        skin.face(leg, "down").fill(PANTS)
        for face in skin.each(pants):
            face.clear()
        for f in SIDES:
            face = skin.face(pants, f)
            wraps(face, 15, 19)
            face.shade(0.55, (face.row >= 15) & (face.row <= 19))
    clear_under_shoes(skin, boot_h)
