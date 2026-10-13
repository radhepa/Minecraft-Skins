"""Rusty: brick-red explorer alien from Mars with big green eyes, a gap-toothed
grin and dusty freckles, glowing 3D antennae, 3D dust goggles on his
forehead, a khaki utility vest over a teal tee, a 3D backpack with a little
radar dish, dusty cargo shorts and chunky hiking boots.
"""

import numpy as np

from paintkit import (SIDES, add_footwear, box, clear_under_shoes, cloth,
                      gradient, paint_boots, rows, skin_tone)
from skinlib import Skin, add_standard_body, noise

ID = "geometry.SolarSystem.Rusty"
TEXTURE = "rusty.png"
NAME = "Rusty"
LOC = "Rusty"
DETAILS = [
    ("face", "Antennae + 3D goggles", {"yaw": 28, "pitch": 6, "dist": 52, "target": 28, "fov": 30}),
    ("back34", "Backpack + radar dish", {"yaw": 150, "pitch": 12}),
    ("boots", "Cargo shorts + hiking boots", {"yaw": -30, "pitch": 12, "dist": 60, "target": 8, "fov": 30}),
]

SKIN = (204, 82, 52)
SKIN_L = (232, 120, 80)
SKIN_D = (160, 56, 38)
FRECKLE = (172, 60, 40)
EYE = (110, 214, 70)
EYE_D = (50, 140, 40)
PUPIL = (24, 30, 26)
GLOW = (190, 255, 120)
GLOW_D = (110, 214, 70)
KHAKI = (198, 170, 112)
KHAKI_D = (156, 128, 80)
KHAKI_H = (222, 198, 146)
OLIVE = (110, 116, 62)
OLIVE_D = (80, 84, 44)
TEAL = (52, 150, 150)
TEAL_D = (34, 110, 112)
BROWN = (110, 70, 40)
BROWN_D = (76, 46, 26)
BROWN_H = (146, 98, 58)
DUST = (214, 120, 76)
LENS = (240, 160, 60)
LENS_L = (255, 222, 150)
FRAME = (58, 52, 50)
STRAP = (70, 56, 46)
WHITE = (248, 244, 236)
MOUTH = (90, 24, 24)
METAL = (176, 182, 190)
METAL_D = (120, 126, 138)

BOOTS = {"upper": BROWN, "hi": BROWN_H, "dark": BROWN_D, "strap": (60, 40, 24),
         "strap_dark": METAL, "sole": (52, 40, 34), "sole_dark": (34, 26, 22)}


def build():
    skin = Skin(ID)
    add_standard_body(skin)
    for side, x, lean in (("R", -2.0, -14), ("L", 2.0, 14)):
        kw = dict(pivot=[x, 32, 0], rotation=[0, 0, lean])
        if side == "R":
            skin.acc("stalkR", "head", [x - 0.25, 32, -0.25], [0.5, 4, 0.5], lowres=("up", "down"), **kw)
            skin.acc("bulbR", "head", [x - 0.75, 36, -0.75], [1.5, 1.5, 1.5], **kw)
        else:
            skin.acc("stalkL", "head", [x - 0.25, 32, -0.25], [0.5, 4, 0.5], like="stalkR", **kw)
            skin.acc("bulbL", "head", [x - 0.75, 36, -0.75], [1.5, 1.5, 1.5], like="bulbR", **kw)
    # goggles pushed up on the forehead
    skin.acc("lensR", "head", [-3.5, 29.25, -5.0], [2.75, 2.25, 1], lowres=("up", "down", "east", "west"))
    skin.acc("lensL", "head", [0.75, 29.25, -5.0], [2.75, 2.25, 1], like="lensR")
    skin.acc("pack", "body", [-3.5, 13, 2.25], [7, 9, 3], lowres=("up", "down", "north", "east", "west"))
    skin.acc("dishPole", "body", [2, 22, 4.5], [0.5, 4, 0.5], lowres=("up", "down", "north", "south", "east", "west"))
    skin.acc("dish", "body", [0.75, 26, 4.75], [3, 0.5, 2], lowres=("north", "south", "east", "west"),
             pivot=[2.25, 26, 5.75], rotation=[-25, 0, 0])
    h = add_footwear(skin, height=3.5, length=5.5, toe=1.0, tongue=False)
    paint_head(skin)
    paint_extras(skin)
    paint_body(skin)
    paint_arms(skin)
    paint_legs(skin, h)
    paint_boots(skin, BOOTS, 5900, straps=(2, 4))
    return skin


def red_skin(face, seed, base=SKIN):
    skin_tone(face, base, seed, var=0.03)
    rs = np.random.RandomState(seed + 7)
    face.fill(FRECKLE, rs.rand(face.h, face.w) < 0.04)


def dusty(face, seed, amount=0.08):
    """Rust-red dust settling toward the bottom of a fabric face."""
    rs = np.random.RandomState(seed)
    t = face.row / max(face.h - 1, 1)
    face.fill(DUST, rs.rand(face.h, face.w) < amount * t * t)


def paint_head(skin):
    for f in SIDES + ("up", "down"):
        red_skin(skin.face("head", f), 5000 + len(f))
    front = skin.face("head", "north")
    skin_tone(front, SKIN, 5001, var=0.025)
    front.fill(SKIN_L, box(front, 10, 3, 14, 12))
    front.shade(noise((16, 16), 5002, 0.03), box(front, 10, 3, 14, 12))
    # big round green eyes
    eye = [
        ".PPP.",
        "PWEEP",
        "PEEDP",
        "PEDDP",
        ".PPP.",
    ]
    pal = {"P": PUPIL, "W": WHITE, "E": EYE, "D": EYE_D}
    front.stamp(eye, pal, top=6, left=2)
    front.stamp(eye, pal, top=6, left=9, mirror=True)
    # gap-toothed grin
    front.stamp(["M......M", ".MWW.WWM", "..MMMM.."], {"M": MOUTH, "W": WHITE}, top=11, left=4)
    front.set(12, 8, MOUTH)
    for r, c in ((10, 2), (11, 3), (10, 4), (10, 11), (11, 12), (10, 13)):
        front.set(r, c, FRECKLE)
    # goggle strap round the head on the hat layer
    for face in skin.each("hat"):
        face.clear()
    for f in SIDES:
        face = skin.face("hat", f)
        rows(face, 3, 5, STRAP)
        rows(face, 3, 3, (96, 80, 66))
        if f in ("east", "west"):
            buckle = face.col == face.w // 2
            face.fill(METAL, buckle & (face.row >= 3) & (face.row <= 5))
    hf = skin.face("hat", "north")
    hf.clear((hf.row >= 3) & (hf.row <= 5) & (((hf.col >= 1) & (hf.col <= 6)) | ((hf.col >= 9) & (hf.col <= 14))))


def paint_extras(skin):
    for face in skin.each("stalkR"):
        gradient(face, [(0, SKIN_L), (1, SKIN_D)])
    for face in skin.each("bulbR"):
        face.fill(GLOW_D)
        face.fill(GLOW, (face.row == 0) | (face.col == 0))
        face.set(0, 0, (240, 255, 220))
    for f in ("north", "south", "east", "west", "up", "down"):
        if ("lensR", f) not in skin.faces:
            continue
        face = skin.face("lensR", f)
        face.fill(FRAME)
    lens = skin.face("lensR", "north")
    lens.fill(LENS, box(lens, 1, 1, lens.h - 2, lens.w - 2))
    lens.fill(LENS_L, box(lens, 1, 1, 1, 2))
    lens.set(2, 1, LENS_L)
    for face in skin.each("pack"):
        cloth(face, OLIVE, 5100 + face.w + face.h, var=0.05, fold=0.03)
    back = skin.face("pack", "south")
    back.fill(OLIVE_D, box(back, 0, 0, 3, back.w - 1))
    rows(back, 4, 4, OLIVE_D)
    back.fill(KHAKI, box(back, 9, 2, 15, back.w - 3))
    back.fill(KHAKI_D, box(back, 9, 2, 9, back.w - 3))
    back.set(12, back.w // 2, METAL)
    # mars patch: a little red planet
    back.stamp([".RR.", "RLRR", "RRRD", ".DD."], {"R": SKIN, "L": SKIN_L, "D": SKIN_D}, top=4, left=back.w // 2 - 2)
    for face in skin.each("dishPole"):
        face.fill(METAL_D)
    for face in skin.each("dish"):
        face.fill(METAL)
    up = skin.face("dish", "up")
    up.fill(METAL)
    up.fill((220, 226, 234), (up.row + up.col) % 3 == 0)
    up.set(up.h // 2, up.w // 2, GLOW)
    skin.face("dish", "down").fill(METAL_D)


def paint_body(skin):
    for f in SIDES + ("up", "down"):
        face = skin.face("body", f)
        cloth(face, TEAL, 5200 + len(f), var=0.05, fold=0.04)
    front = skin.face("body", "north")
    neck = (front.row <= 1) & (front.col >= 5) & (front.col <= 10)
    front.fill(SKIN, neck)
    # cargo shorts waist + belt
    for f in SIDES:
        face = skin.face("body", f)
        cloth(face, KHAKI, 5210 + len(f), var=0.05, fold=0.03, mask=face.row >= 20)
        rows(face, 19, 20, BROWN)
        rows(face, 20, 20, BROWN_D)
    front.fill(METAL, box(front, 19, 7, 20, 8))
    # utility vest on the jacket layer
    for face in skin.each("jacket"):
        face.clear()
    for f in SIDES:
        face = skin.face("jacket", f)
        cloth(face, KHAKI, 5220 + len(f), var=0.05, fold=0.03)
        face.clear(face.row >= 19)
        dusty(face, 5230 + len(f), 0.1)
    jk = skin.face("jacket", "north")
    jk.clear((jk.col >= 6) & (jk.col <= 9))
    jk.fill(KHAKI_D, (jk.col == 5) | (jk.col == 10))
    for left in (1, 11):
        for top in (5, 11):
            jk.fill(KHAKI_D, box(jk, top, left, top + 4, left + 3))
            jk.fill(KHAKI_H, box(jk, top, left, top, left + 3))
            jk.set(top + 1, left + 1, METAL)
    # red planet badge on the chest pocket
    jk.stamp([".RR.", "RLRR", ".RR."], {"R": SKIN, "L": SKIN_L}, top=6, left=11)
    skin.face("jacket", "up").fill(KHAKI)
    skin.face("jacket", "up").clear(box(skin.face("jacket", "up"), 2, 4, 6, 11))
    skin.face("jacket", "down").clear()


def paint_arms(skin):
    for arm, slv, seed in (("rightArm", "rightSleeve", 5300), ("leftArm", "leftSleeve", 5310)):
        for f in SIDES + ("up", "down"):
            red_skin(skin.face(arm, f), seed + len(f))
        for f in SIDES:
            face = skin.face(arm, f)
            cloth(face, TEAL, seed + 10 + len(f), var=0.05, fold=0.03, mask=face.row <= 6)
            rows(face, 16, 17, BROWN)       # leather wrist cuff
            face.set(16, face.w // 2, METAL)
        skin.face(arm, "up").fill(TEAL)
        for face in skin.each(slv):
            face.clear()
        # rolled sleeve cuff
        for f in SIDES:
            face = skin.face(slv, f)
            rows(face, 5, 7, TEAL_D)
            rows(face, 5, 5, TEAL)


def paint_legs(skin, boot_h):
    for leg, pants, outer, seed in (("rightLeg", "rightPants", "east", 5400), ("leftLeg", "leftPants", "west", 5410)):
        for f in SIDES:
            face = skin.face(leg, f)
            red_skin(face, seed + len(f))
            cloth(face, KHAKI, seed + 10 + len(f), var=0.05, fold=0.04, mask=face.row <= 9)
            # grey hiking socks above the boots
            sock = face.row >= 14
            face.fill((200, 196, 186), sock)
            face.fill((170, 166, 158), sock & (face.row % 2 == 0))
        skin.face(leg, "up").fill(KHAKI)
        skin.face(leg, "down").fill(BROWN_D)
        for face in skin.each(pants):
            face.clear()
        # cargo pockets on the shorts layer
        for f in SIDES:
            face = skin.face(pants, f)
            cloth(face, KHAKI, seed + 20 + len(f), var=0.05, fold=0.04)
            face.clear(face.row >= 10)
            rows(face, 9, 9, KHAKI_D)
            dusty(face, seed + 30 + len(f), 0.12)
        side = skin.face(pants, outer)
        side.fill(KHAKI_D, box(side, 3, 1, 8, 6))
        side.fill(KHAKI_H, box(side, 3, 1, 3, 6))
        side.set(4, 3, METAL)
        skin.face(pants, "up").clear()
        skin.face(pants, "down").clear()
    clear_under_shoes(skin, boot_h)
