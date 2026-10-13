"""Lunar Howler: grey werewolf with a snarling snout, glowing eyes and
pointed ears, torn plum flannel over a furry chest, ripped jeans, clawed paws
and a bushy tail.
"""

import numpy as np

from paintkit import SIDES, add_footwear, box, clear_under_shoes, cloth, hair, rows
from skinlib import Skin, add_standard_body, noise

ID = "geometry.MidnightMischief.LunarHowler"
TEXTURE = "lunar_howler.png"
NAME = "Lunar Howler"
LOC = "LunarHowler"
DETAILS = [
    ("face", "3D snout, fangs + ears", {"yaw": 35, "pitch": 6, "dist": 46, "target": 27, "fov": 30}),
    ("back34", "Bushy 3D tail", {"yaw": 150, "pitch": 8}),
    ("paws", "Clawed paw feet", {"yaw": 30, "pitch": 18, "dist": 44, "target": 6, "fov": 30}),
]

FUR = (112, 100, 96)
FUR_D = (84, 74, 72)
FUR_H = (142, 128, 122)
MUZZLE = (190, 178, 166)
MUZZLE_D = (164, 152, 140)
NOSE = (28, 22, 26)
FANG = (250, 246, 236)
EYE = (255, 212, 60)
EYE_C = (255, 246, 170)
GUM = (150, 50, 70)
EAR_IN = (170, 110, 120)
PLUM = (122, 34, 70)
PLUM_D = (88, 22, 50)
PLAID = (34, 22, 32)
DENIM = (54, 58, 76)
DENIM_D = (40, 42, 58)
DENIM_H = (72, 76, 96)
CLAW = (236, 230, 214)


def build():
    skin = Skin(ID)
    add_standard_body(skin)
    skin.acc("snout", "head", [-2, 24.5, -6.5], [4, 2.5, 2.5], lowres=("down",))
    skin.acc("snoutNose", "head", [-1, 27, -6.5], [2, 0.75, 1], px=2)
    for side, x_base, x_tip in (("Right", -4.25, -4.25), ("Left", 1.75, 2.75)):
        skin.acc(f"ear{side}", "head", [x_base, 32.25, -1], [2.5, 2.5, 1.5], lowres=("up", "down"))
        skin.acc(f"earTip{side}", "head", [x_tip, 34.75, -0.75], [1.5, 1.5, 1], lowres=("up", "down"))
    skin.acc("tailBase", "body", [-1, 12.5, 2.25], [2, 2, 2.5], lowres=("up", "down"))
    skin.acc("tail", "body", [-1.5, 9.5, 4.25], [3, 4.5, 3], lowres=("up",))
    skin.acc("tailTip", "body", [-1, 7.5, 4.75], [2, 2, 2], lowres=("up",))
    h = add_footwear(skin, height=2.5, length=6.0, toe=1.5, tongue=False)
    paint_head(skin)
    paint_extras(skin)
    paint_body(skin)
    paint_arms(skin)
    paint_legs(skin, h)
    paint_paws(skin)
    return skin


def fur(face, seed, base=FUR):
    """Shaggy fur: short strands in three tones around the base colour."""
    dark = tuple(int(v * 0.8) for v in base)
    light = tuple(min(255, int(v * 1.18)) for v in base)
    hair(face, base, dark, light, seed)


def paint_head(skin):
    for f in SIDES + ("up", "down"):
        fur(skin.face("head", f), 3100 + len(f))
    front = skin.face("head", "north")
    # heavy brow ridge + glowing eyes
    rows(front, 6, 6, FUR_D, (front.col >= 2) & (front.col <= 13))
    for r, c in ((5, 2), (5, 3), (5, 12), (5, 13)):
        front.set(r, c, FUR_D)
    eye = ["NEEC", "NNEE"]
    pal = {"N": NOSE, "E": EYE, "C": EYE_C}
    front.stamp(eye, pal, top=7, left=2)
    front.stamp(eye, pal, top=7, left=10, mirror=True)
    front.fill(MUZZLE, box(front, 9, 4, 15, 11))
    front.shade(np.where(box(front, 9, 4, 15, 11), noise((16, 16), 3101, 0.04), 1.0))
    front.fill(MUZZLE_D, box(front, 15, 4, 15, 11))
    # hat layer: shaggy mane round the face and down the back of the head
    for f in SIDES + ("up", "down"):
        fur(skin.face("hat", f), 3110 + len(f), FUR_D)
    skin.face("hat", "down").clear()
    mane = skin.face("hat", "north")
    keep = (mane.row <= 2) | (mane.col <= 1) | (mane.col >= 14)
    mane.clear(~keep)
    mane.clear((mane.row == 2) & (mane.col % 2 == 0) & (mane.col > 1) & (mane.col < 14))
    for f in ("east", "west", "south"):
        face = skin.face("hat", f)
        face.clear((face.row == 15) & (face.col % 2 == 0))


def paint_extras(skin):
    for face in skin.each("snout"):
        face.fill(MUZZLE)
        face.shade(noise((face.h, face.w), 3120 + face.w, 0.04))
    sn = skin.face("snout", "north")
    rows(sn, 0, 1, MUZZLE)
    rows(sn, 3, 3, NOSE)                                  # mouth line
    rows(sn, 4, 4, GUM, (sn.col >= 1) & (sn.col <= sn.w - 2))
    for c in (1, sn.w - 2):
        sn.set(4, c, FANG)
        sn.set(3, c, FANG)
    for c in (3, 4):
        sn.set(4, c, FANG)
    for f in ("east", "west"):
        side = skin.face("snout", f)
        rows(side, 3, 3, NOSE)
        side.fill(FANG, (side.row == 4) & (side.col == (side.w - 2 if f == "east" else 1)))
    top = skin.face("snout", "up")
    top.fill(FUR, top.row <= 1)
    for face in skin.each("snoutNose"):
        face.fill(NOSE)
    skin.face("snoutNose", "north").set(0, 1, (80, 70, 76))
    for side in ("Right", "Left"):
        for name in (f"ear{side}", f"earTip{side}"):
            for face in skin.each(name):
                fur(face, 3130 + face.w, FUR_D)
        ear = skin.face(f"ear{side}", "north")
        ear.fill(EAR_IN, box(ear, 1, 1, ear.h - 1, ear.w - 2))
    for name in ("tailBase", "tail", "tailTip"):
        for face in skin.each(name):
            fur(face, 3140 + face.w + face.h)
    for face in skin.each("tailTip"):
        face.fill(MUZZLE)
        face.shade(noise((face.h, face.w), 3150, 0.06))


def flannel(face, seed):
    face.fill(PLUM)
    pr = (face.row % 5 == 0)
    pc = (face.col % 5 == 0)
    face.fill(PLUM_D, pr ^ pc)
    face.fill(PLAID, pr & pc)
    face.shade(noise((face.h, face.w), seed, 0.05))


def torn_edge(face, base_row, seed):
    """Ragged hem: per-column cut-off row around base_row."""
    rs = np.random.RandomState(seed)
    return base_row + rs.randint(-1, 2, size=face.w)


def paint_body(skin):
    front = skin.face("body", "north")
    chest = (front.col >= 5) & (front.col <= 10)
    fur(front, 3201, MUZZLE)
    tmp = front.rgba.copy()
    flannel(front, 3200)
    front.rgba = np.where(chest[..., None], tmp, front.rgba)
    # buttons hang off where the shirt burst open
    for r in (6, 11, 16):
        front.set(r, 4, (220, 210, 190))
    for c in (4, 11):
        rows(front, 0, 23, PLUM_D, front.col == c)
    for f in ("east", "west", "south"):
        flannel(skin.face("body", f), 3210 + len(f))
    back = skin.face("body", "south")
    # claw-rip across the back of the shirt
    for i in range(3):
        for r in range(6, 15):
            c = 4 + i * 3 + (r - 6) // 3
            back.set(r, c, FUR)
    for f in ("up", "down"):
        flannel(skin.face("body", f), 3220 + len(f))
    # torn hem on the overlay
    for f in SIDES:
        face = skin.face("jacket", f)
        flannel(face, 3230 + len(f))
        cut = torn_edge(face, 21, 3240 + len(f))
        face.clear(face.row > cut[face.col])
        if f == "north":
            face.clear((face.col >= 5) & (face.col <= 10))
    skin.face("jacket", "up").clear()
    skin.face("jacket", "down").clear()


def paint_arms(skin):
    for arm, slv, seed in (("rightArm", "rightSleeve", 3300), ("leftArm", "leftSleeve", 3310)):
        for f in SIDES:
            face = skin.face(arm, f)
            flannel(face, seed + len(f))
            forearm = face.row >= 11
            tmp = face.rgba.copy()
            fur(face, seed + 5 + len(f))
            face.rgba = np.where(forearm[..., None], face.rgba, tmp)
            if f == "north":
                for c in (1, 3, 5, 7):
                    face.set(23, c, CLAW)
        flannel(skin.face(arm, "up"), seed + 7)
        paw = skin.face(arm, "down")
        fur(paw, seed + 8, FUR_D)
        for c in (1, 3, 5, 7):
            paw.set(paw.h - 1, c, CLAW)
        # ragged sleeve ends torn off at the elbow
        for f in SIDES:
            face = skin.face(slv, f)
            flannel(face, seed + 20 + len(f))
            cut = torn_edge(face, 10, seed + 30 + len(f))
            face.clear(face.row > cut[face.col])
        skin.face(slv, "up").clear()
        skin.face(slv, "down").clear()


def paint_legs(skin, paw_h):
    for leg, pants, seed in (("rightLeg", "rightPants", 3400), ("leftLeg", "leftPants", 3410)):
        for f in SIDES:
            face = skin.face(leg, f)
            cloth(face, DENIM, seed + len(f), var=0.08, fold=0.06, freq=0.8)
            face.fill(DENIM_H, (face.row % 6 == 3) & (face.col % 3 == 1))
            cut = torn_edge(face, 14, seed + 9 + len(f))
            shin = face.row > cut[face.col]
            tmp = face.rgba.copy()
            fur(face, seed + 5 + len(f))
            face.rgba = np.where(shin[..., None], face.rgba, tmp)
            face.fill((210, 214, 226), face.row == cut[face.col])
        skin.face(leg, "up").fill(DENIM_D)
        skin.face(leg, "down").fill(FUR_D)
        for face in skin.each(pants):
            face.clear()
        front = skin.face(pants, "north")
        knee = box(front, 7, 2, 9, 5)
        front.fill((210, 214, 226), knee & (front.row != 8))
        front.fill(FUR, knee & (front.row == 8))
    clear_under_shoes(skin, paw_h)


def paint_paws(skin):
    for side in ("right", "left"):
        shoe = f"{side}Shoe"
        for face in skin.each(shoe):
            fur(face, 3500 + face.w + face.h)
        toe = skin.face(shoe, "north")
        rows(toe, toe.h - 1, toe.h - 1, FUR_D)
        for c in range(1, toe.w, 2):
            toe.set(toe.h - 1, c, CLAW)
            toe.set(toe.h - 2, c, CLAW)
            if c + 1 < toe.w:
                toe.set(0, c + 1, FUR_D)
        sole = skin.face(shoe, "down")
        sole.fill(NOSE)
        top = skin.face(shoe, "up")
        top.fill(FUR_D, top.col % 2 == 0)
