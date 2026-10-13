"""Scarecrow Sam: stitched burlap face under a wide straw hat, orange-and-
purple flannel, patched overalls, straw poking out of every cuff.
"""

import numpy as np

from paintkit import (SIDES, add_footwear, box, clear_under_shoes, cloth,
                      paint_boots, rows)
from skinlib import Skin, add_standard_body, noise

ID = "geometry.MidnightMischief.ScarecrowSam"
TEXTURE = "scarecrow_sam.png"
NAME = "Scarecrow Sam"
LOC = "ScarecrowSam"
DETAILS = [
    ("face", "3D straw hat + burlap face", {"yaw": 22, "pitch": 12, "dist": 46, "target": 28, "fov": 30}),
    ("back34", "Straw tufts + patched overalls", {"yaw": 205, "pitch": 10}),
    ("boots", "Work boots + straw cuffs", {"yaw": 35, "pitch": 14, "dist": 52, "target": 8, "fov": 30}),
]

BURLAP = (196, 160, 108)
BURLAP_D = (170, 134, 86)
BURLAP_H = (214, 182, 130)
STITCH = (70, 44, 28)
STRAW = (232, 196, 96)
STRAW_D = (204, 166, 70)
STRAW_H = (248, 222, 134)
BAND = (110, 52, 168)
BAND_D = (82, 36, 132)
FLANNEL = (214, 108, 38)
FLANNEL_D = (150, 64, 26)
PLAID = (74, 40, 92)
DENIM = (78, 94, 128)
DENIM_D = (60, 72, 102)
DENIM_H = (100, 116, 150)
PATCH_P = (126, 68, 170)
PATCH_G = (110, 150, 70)
ROPE = (184, 150, 96)
GLOVE = (126, 86, 50)

BOOTS = {"upper": (104, 70, 42), "hi": (134, 94, 60), "dark": (78, 50, 30),
         "strap": (60, 40, 26), "strap_dark": (180, 160, 130), "sole": (60, 44, 32), "sole_dark": (40, 30, 22)}


def build():
    skin = Skin(ID)
    add_standard_body(skin)
    skin.acc("hatBrim", "head", [-6.5, 32.5, -6.5], [13, 0.75, 13], px=1)
    skin.acc("hatCrown", "head", [-4, 33.25, -4], [8, 3, 8], lowres=("up", "down"))
    skin.acc("hatTip", "head", [-2.5, 36.25, -2.5], [5, 0.75, 5], px=1)
    for side, x in (("right", -8), ("left", 4)):
        skin.acc(f"{side}Straw", f"{side}Arm", [x, 11.25, -2], [4, 1, 4], inflate=0.35, lowres=("up", "down"))
    skin.acc("neckStraw", "body", [-3, 23.5, -2.75], [6, 1, 1], px=2, faces=("north", "east", "west", "up"))
    h = add_footwear(skin, height=3.5, length=5.5, toe=1.0, tongue=False)
    paint_head(skin)
    paint_hat(skin)
    paint_body(skin)
    paint_arms(skin)
    paint_legs(skin, h)
    paint_boots(skin, BOOTS, 2900, straps=(1, 3))
    return skin


def burlap(face, seed):
    face.fill(BURLAP)
    weave = ((face.row % 2 == 0) ^ (face.col % 2 == 0))
    face.shade(np.where(weave, 0.94, 1.03))
    face.shade(noise((face.h, face.w), seed, 0.05))


def straw(face, seed):
    rs = np.random.RandomState(seed)
    lane = rs.choice([0, 1, 1, 2], size=face.w)
    pal = np.array([STRAW_D, STRAW, STRAW_H], float)
    face.rgba[..., :3] = pal[lane[face.col]]
    face.rgba[..., 3] = 255
    face.shade(noise((face.h, face.w), seed + 1, 0.05))


def paint_head(skin):
    for f in SIDES + ("up", "down"):
        burlap(skin.face("head", f), 2800 + len(f))
    front = skin.face("head", "north")
    button = ["DDD", "DhD", "DDD"]
    pal = {"D": (40, 30, 26), "h": (110, 96, 90)}
    front.stamp(button, pal, top=6, left=3)
    front.stamp(button, pal, top=6, left=10)
    for c in (4, 11):
        front.set(5, c - 1, STITCH)
        front.set(9, c + 1, STITCH)
    # long stitched grin
    grin = [(11, 2), (12, 3), (12, 4), (12, 5), (12, 6), (12, 7), (12, 8), (12, 9),
            (12, 10), (12, 11), (12, 12), (11, 13)]
    for r, c in grin:
        front.set(r, c, STITCH)
    for c in (4, 6, 8, 10):
        front.set(11, c, STITCH)
        front.set(13, c, STITCH)
    front.set(9, 7, (200, 110, 60))
    front.set(9, 8, (200, 110, 60))
    # rosy painted cheeks
    for c in (2, 13):
        front.set(10, c, (214, 128, 92))
    # twine cinched round the neck
    for f in SIDES:
        face = skin.face("head", f)
        rows(face, 15, 15, ROPE)
        face.fill(STITCH, (face.row == 15) & (face.col % 3 == 0))
    # hat layer: straw hair sticking out under the brim at the sides/back
    for f in SIDES + ("up", "down"):
        skin.face("hat", f).clear()
    for f in ("east", "west", "south"):
        face = skin.face("hat", f)
        straw(face, 2810 + len(f))
        rs = np.random.RandomState(2820 + len(f))
        length = 2 + rs.randint(0, 4, size=face.w)
        face.clear(face.row >= length[face.col])
    north = skin.face("hat", "north")
    straw(north, 2830)
    north.clear(~(((north.col <= 1) | (north.col >= 14)) & (north.row <= 3)))


def paint_hat(skin):
    for name in ("hatBrim", "hatCrown", "hatTip"):
        for face in skin.each(name):
            straw(face, 2840 + face.w + face.h)
    for f in SIDES:
        face = skin.face("hatCrown", f)
        rows(face, 3, 4, BAND)
        rows(face, 4, 4, BAND_D)
        if f == "east":
            face.fill(STRAW_H, box(face, 1, 5, 2, 6))
    for f in SIDES:
        face = skin.face("hatBrim", f)
        face.fill(STRAW_D, face.col % 2 == 0)
    under = skin.face("hatBrim", "down")
    under.shade(0.75)
    top = skin.face("hatBrim", "up")
    # ragged brim edge
    top.fill(STRAW_D, (top.row == 0) | (top.row == top.h - 1) | (top.col == 0) | (top.col == top.w - 1))


def flannel(face, seed):
    face.fill(FLANNEL)
    plaid_r = (face.row % 6 == 0) | (face.row % 6 == 1)
    plaid_c = (face.col % 6 == 0) | (face.col % 6 == 1)
    face.fill(FLANNEL_D, plaid_r ^ plaid_c)
    face.fill(PLAID, plaid_r & plaid_c)
    face.shade(noise((face.h, face.w), seed, 0.05))


def overalls(face, seed, mask):
    cloth(face, DENIM, seed, var=0.07, fold=0.05, freq=0.9, mask=mask)


def paint_body(skin):
    for f in SIDES + ("up", "down"):
        flannel(skin.face("body", f), 2850 + len(f))
    front = skin.face("body", "north")
    bib = box(front, 8, 3, 23, 12) | (front.row >= 18)
    straps = box(front, 0, 3, 7, 4) | box(front, 0, 11, 7, 12)
    overalls(front, 2860, bib | straps)
    front.set(8, 3, (220, 200, 150))
    front.set(8, 12, (220, 200, 150))
    front.fill(PATCH_P, box(front, 11, 8, 14, 11))
    for r, c in ((11, 8), (11, 11), (14, 8), (14, 11), (12, 7), (13, 12)):
        front.set(r, c, STITCH)
    rows(front, 17, 17, ROPE)
    front.fill(STITCH, (front.row == 17) & (front.col % 4 == 1))
    for f in ("east", "west", "south"):
        face = skin.face("body", f)
        lower = face.row >= 18
        overalls(face, 2870 + len(f), lower)
        rows(face, 17, 17, ROPE)
    back = skin.face("body", "south")
    for r in range(0, 18):
        for c in (3 + r // 3, 12 - r // 3):
            back.set(r, c, DENIM)
    back.fill(PATCH_G, box(back, 19, 9, 21, 12))
    # flannel is bulky: copy to the overlay so the shirt has depth at the
    # sides and back, but keep the overalls flat on the base
    jk = skin.face("jacket", "north")
    jk.clear()
    for f in ("east", "west"):
        side = skin.face("jacket", f)
        flannel(side, 2880 + len(f))
        side.clear(side.row >= 17)
    for f in ("south", "up", "down"):
        skin.face("jacket", f).clear()
    straw_bits = skin.face("neckStraw", "north")
    for face in skin.each("neckStraw"):
        straw(face, 2890 + face.w)
    straw_bits.clear((straw_bits.row == 0) & (straw_bits.col % 3 == 1))


def paint_arms(skin):
    for arm, slv, straw_cube, seed in (("rightArm", "rightSleeve", "rightStraw", 2900),
                                       ("leftArm", "leftSleeve", "leftStraw", 2910)):
        for f in SIDES:
            face = skin.face(arm, f)
            flannel(face, seed + len(f))
            glove = face.row >= 20
            face.fill(GLOVE, glove)
            face.shade(np.where(glove, noise((24, 8), seed + 3, 0.06), 1.0))
            rows(face, 18, 19, FLANNEL_D)
            face.fill(STITCH, (face.row == 22) & (face.col % 3 == 1))
        flannel(skin.face(arm, "up"), seed + 7)
        skin.face(arm, "down").fill(GLOVE)
        for face in skin.each(slv):
            face.clear()
        for f in SIDES:
            face = skin.face(straw_cube, f)
            straw(face, seed + 20 + len(f))
            face.clear((face.row == face.h - 1) & (face.col % 2 == 1))
        skin.face(straw_cube, "up").clear()
        skin.face(straw_cube, "down").clear()
        # straw spilling out of the shirt cuff
        for f in SIDES:
            face = skin.face(arm, f)
            face.fill(STRAW, (face.row == 19) & (face.col % 2 == 0))


def paint_legs(skin, boot_h):
    patches = {"rightLeg": ("north", PATCH_G, (8, 2, 11, 5)), "leftLeg": ("east", PATCH_P, (4, 1, 7, 4))}
    for leg, pants, seed in (("rightLeg", "rightPants", 3000), ("leftLeg", "leftPants", 3010)):
        for f in SIDES:
            face = skin.face(leg, f)
            cloth(face, DENIM, seed + len(f), var=0.07, fold=0.05, freq=0.9)
            face.fill(DENIM_D, face.col == (4 if f in ("east", "west") else 0))
            face.fill(DENIM_H, (face.row % 5 == 1) & (face.col % 4 == 2))
        pf, pc, (r0, c0, r1, c1) = patches[leg]
        face = skin.face(leg, pf)
        face.fill(pc, box(face, r0, c0, r1, c1))
        for r, c in ((r0, c0), (r0, c1), (r1, c0), (r1, c1)):
            face.set(r, c, STITCH)
        skin.face(leg, "up").fill(DENIM_D)
        skin.face(leg, "down").fill(DENIM_D)
        # rolled cuffs with straw poking out
        for f in SIDES:
            face = skin.face(pants, f)
            face.clear()
            cloth(face, DENIM_H, seed + 20 + len(f), var=0.04, fold=0.0, mask=(face.row >= 14) & (face.row <= 16))
            face.fill(STRAW, (face.row == 13) & (face.col % 3 == 1))
        skin.face(pants, "up").clear()
        skin.face(pants, "down").clear()
    clear_under_shoes(skin, boot_h)
