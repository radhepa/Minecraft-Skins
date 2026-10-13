"""Vesper: mint-green alien from Venus, wrapped in its golden clouds. Big rose
eyes, puffy 3D cloud hair with a cloud bun, heart-tipped antennae, a coral
dress with a gold Venus-symbol pendant, a puffy 3D cloud skirt, gold bangles
and cloud boots.
"""

import numpy as np

from paintkit import (SIDES, add_footwear, box, cells, clear_under_shoes, cloth,
                      gradient, rows, skin_tone)
from skinlib import Skin, add_standard_body, noise

ID = "geometry.SolarSystem.Vesper"
TEXTURE = "vesper.png"
NAME = "Vesper"
LOC = "Vesper"
DETAILS = [
    ("face", "Cloud hair + heart antennae", {"yaw": 24, "pitch": 6, "dist": 52, "target": 28, "fov": 30}),
    ("back34", "3D cloud bun", {"yaw": 150, "pitch": 10}),
    ("skirt", "Puffy cloud skirt + boots", {"yaw": -30, "pitch": 10, "dist": 66, "target": 10, "fov": 30}),
]

SKIN = (172, 232, 198)
SKIN_D = (142, 208, 174)
SKIN_S = (120, 186, 154)
BLUSH = (255, 156, 160)
CLOUD_L = (255, 253, 240)
CLOUD = (255, 242, 200)
CLOUD_D = (248, 218, 150)
CLOUD_S = (230, 186, 116)
ROSE = (222, 64, 116)
ROSE_L = (255, 140, 176)
LASH = (60, 34, 52)
CORAL = (246, 104, 112)
CORAL_D = (206, 70, 86)
CORAL_H = (255, 146, 146)
GOLD = (250, 200, 76)
GOLD_D = (196, 140, 40)
MOUTH = (170, 60, 90)


def build():
    skin = Skin(ID, slim=True)
    add_standard_body(skin)
    lo = ("down",)
    # cloud hair: a big bun at the back, a puff on top and two at the temples
    skin.acc("cloudBun", "head", [-3.5, 25.5, 4.25], [7, 5.5, 2.5], lowres=lo)
    skin.acc("cloudBunTop", "head", [-2.5, 31, 4.25], [5, 1.5, 2], lowres=lo)
    skin.acc("cloudTopA", "head", [-3.75, 32.25, -2.75], [3.5, 2, 3.5], lowres=lo)
    skin.acc("cloudTopB", "head", [-0.75, 32.25, -1.0], [4, 2.5, 4], lowres=lo)
    skin.acc("cloudTopC", "head", [0.75, 32.25, -3.25], [3.5, 2, 3.5], like="cloudTopA")
    skin.acc("cloudSideR", "head", [-5.25, 29, -3], [1.5, 3.5, 4], lowres=lo)
    skin.acc("cloudSideL", "head", [3.75, 29, -3], [1.5, 3.5, 4], like="cloudSideR")
    # heart antennae
    for side, x, lean in (("R", -2.5, -16), ("L", 2.5, 16)):
        piv = [x, 33.5, 0]
        kw = dict(pivot=piv, rotation=[0, 0, lean])
        if side == "R":
            skin.acc("stalkR", "head", [x - 0.25, 33.5, -0.25], [0.5, 3, 0.5], lowres=("up", "down"), **kw)
            skin.acc("heartR", "head", [x - 1.25, 36.25, -0.25], [2.5, 2.5, 0.5], px=2, faces=("north", "south"), pad=("north", "south"), **kw)
        else:
            skin.acc("stalkL", "head", [x - 0.25, 33.5, -0.25], [0.5, 3, 0.5], like="stalkR", **kw)
            skin.acc("heartL", "head", [x - 1.25, 36.25, -0.25], [2.5, 2.5, 0.5], like="heartR", **kw)
    skin.acc("cloudSkirt", "body", [-4.5, 10.5, -2.5], [9, 3, 5], lowres=("up", "down"))
    h = add_footwear(skin, height=3.0, length=5.0, toe=1.0, tongue=False, width=4.25)
    paint_head(skin)
    paint_clouds(skin)
    paint_body(skin)
    paint_arms(skin)
    paint_legs(skin, h)
    paint_boots(skin)
    return skin


def cloud(face, seed, size=4.0):
    """Billowing cloud puffs: each puff is bright on top and warms to gold
    underneath, with a soft golden crease where puffs overlap."""
    rs = np.random.RandomState(seed)
    n = max(3, int(face.w * face.h / (size * size)))
    py, px = rs.rand(n) * (face.h + 2) - 1, rs.rand(n) * (face.w + 2) - 1
    d = np.sqrt((face.row[..., None] - py) ** 2 + (face.col[..., None] - px) ** 2)
    order = np.argsort(d, -1)
    near = order[..., 0]
    d1 = np.take_along_axis(d, order[..., :1], -1)[..., 0]
    d2 = np.take_along_axis(d, order[..., 1:2], -1)[..., 0]
    dy = face.row - py[near]
    t = np.clip(0.35 + dy / (size * 1.2), 0, 1)
    gradient(face, [(0, CLOUD_L), (0.45, CLOUD), (0.8, CLOUD_D), (1, CLOUD_S)], t=t)
    crease = ((d2 - d1) < 0.8) & (dy > 0)
    face.fill(CLOUD_D, crease)
    face.shade(noise((face.h, face.w), seed + 1, 0.015))


BANGS = [6, 5, 4, 3, 4, 5, 4, 3, 3, 4, 5, 4, 3, 4, 5, 6]


def paint_head(skin):
    front = skin.face("head", "north")
    skin_tone(front, SKIN, 3000, var=0.02)
    bangs = front.row <= np.array(BANGS)[front.col]
    tmp = front.rgba.copy()
    cloud(front, 3001)
    front.rgba = np.where(bangs[..., None], front.rgba, tmp)
    front.shade(np.where((front.row == np.array(BANGS)[front.col] + 1) & ~bangs, 0.9, 1.0))
    eye = [
        "LLLL.",
        "WRRRL",
        "RHRRL",
        "RRPP.",
        ".PPP.",
    ]
    pal = {"L": LASH, "W": (255, 255, 255), "R": ROSE, "H": (255, 236, 244), "P": ROSE_L}
    front.stamp(eye, pal, top=6, left=2)
    front.stamp(eye, pal, top=6, left=9, mirror=True)
    front.set(5, 1, LASH)
    front.set(5, 14, LASH)
    for c in (2, 3, 12, 13):
        front.set(11, c, BLUSH)
    # little heart freckle and a sweet smile
    front.stamp(["M..M", ".MM."], {"M": MOUTH}, top=12, left=6)
    front.set(10, 12, CORAL)
    for f in ("east", "west", "south", "up"):
        face = skin.face("head", f)
        skin_tone(face, SKIN, 3010 + len(f))
        if f in ("south", "up"):
            cloud(face, 3020 + len(f))
        else:
            near_front = face.col >= 12 if f == "east" else face.col <= 3
            tmp = face.rgba.copy()
            cloud(face, 3030 + len(f))
            keep = ~near_front | (face.row <= 4)
            face.rgba = np.where(keep[..., None], face.rgba, tmp)
    skin_tone(skin.face("head", "down"), SKIN_D, 3040)
    for face in skin.each("hat"):
        face.clear()
    # a few wisps on the hat layer over the bangs
    hat = skin.face("hat", "north")
    cloud(hat, 3050)
    hat.clear(hat.row > np.array(BANGS)[hat.col] - 2)
    for f in ("east", "west"):
        face = skin.face("hat", f)
        cloud(face, 3060 + len(f))
        near_front = face.col >= 12 if f == "east" else face.col <= 3
        face.clear(near_front | (face.row >= 13) | ((face.row == 12) & (face.col % 2 == 0)))
    back = skin.face("hat", "south")
    cloud(back, 3070)
    back.clear((back.row >= 14) | ((back.row == 13) & (back.col % 3 == 0)))


def puff_edges(face):
    """Round off a cloud cube's silhouette by nicking its corners."""
    for r, c in ((0, 0), (0, face.w - 1), (face.h - 1, 0), (face.h - 1, face.w - 1)):
        face.clear((face.row == r) & (face.col == c))


def paint_clouds(skin):
    for name in ("cloudBun", "cloudBunTop", "cloudTopA", "cloudTopB", "cloudSideR"):
        for face in skin.each(name):
            cloud(face, 3100 + face.w * 3 + face.h)
        for f in SIDES:
            if (name, f) in skin.faces:
                puff_edges(skin.face(name, f))
    bun = skin.face("cloudBun", "south")
    # scalloped bottom edge
    bun.clear((bun.row == bun.h - 1) & (bun.col % 4 == 0))
    for f in ("north", "south"):
        heart = skin.face("heartR", f)
        heart.clear()
        heart.stamp(["CC.CC", "CHCCC", "CCCCC", ".CCC.", "..C.."],
                    {"C": CORAL, "H": CORAL_H}, top=0, left=0)
    for face in skin.each("stalkR"):
        gradient(face, [(0, CORAL_H), (1, SKIN_D)])


def paint_body(skin):
    front = skin.face("body", "north")
    cloth(front, CORAL, 3200, var=0.04, fold=0.03)
    # heart-shaped neckline
    neck = np.zeros((24, 16), bool)
    for r in range(5):
        half = [7, 7, 6, 4, 2][r]
        neck[r, 8 - half:8 + half] = True
    neck[3:5, 7:9] = False
    tmp = front.rgba.copy()
    skin_tone(front, SKIN, 3201)
    front.rgba = np.where(neck[..., None], front.rgba, tmp)
    # Venus symbol pendant
    front.stamp([".GG.", "G..G", "G..G", ".GG.", "GGGG", ".GG."], {"G": GOLD}, top=4, left=6)
    front.set(3, 7, GOLD_D)
    front.set(3, 8, GOLD_D)
    for f in ("east", "west", "south"):
        face = skin.face("body", f)
        cloth(face, CORAL, 3210 + len(f), var=0.04, fold=0.03)
        rows(face, 0, 1, SKIN)
    for f in SIDES:
        face = skin.face("body", f)
        rows(face, 15, 16, GOLD)
        rows(face, 16, 16, GOLD_D)
    front.stamp([".C.C.", "CCCCC", ".CCC.", "..C.."], {"C": CORAL_H}, top=14, left=6)
    front.stamp([".D.D.", "DDDDD", ".DDD.", "..D.."], {"D": CORAL_D}, top=15, left=6)
    skin_tone(skin.face("body", "up"), SKIN, 3220)
    cloth(skin.face("body", "down"), CORAL_D, 3221)
    for face in skin.each("jacket"):
        face.clear()
    # little heart pattern on the bodice overlay
    jk = skin.face("jacket", "north")
    for r, c in ((7, 2), (10, 12), (12, 3)):
        jk.stamp(["H.H", ".H."], {"H": CORAL_H}, top=r, left=c)

    for face in skin.each("cloudSkirt"):
        cloud(face, 3230 + face.w + face.h)
    for f in SIDES:
        face = skin.face("cloudSkirt", f)
        face.clear((face.row == face.h - 1) & (face.col % 3 == 1))
        face.clear((face.row == 0) & (face.col % 4 == 0))


def paint_arms(skin):
    for arm, slv, seed in (("rightArm", "rightSleeve", 3300), ("leftArm", "leftSleeve", 3310)):
        for f in SIDES + ("up", "down"):
            skin_tone(skin.face(arm, f), SKIN, seed + len(f))
        for f in SIDES:
            face = skin.face(arm, f)
            cloth(face, CORAL, seed + 10 + len(f), var=0.04, fold=0.03, mask=face.row <= 3)
            rows(face, 15, 15, GOLD)
            rows(face, 17, 17, GOLD_D)
        skin.face(arm, "up").fill(CORAL)
        for face in skin.each(slv):
            face.clear()
        # puffy cloud sleeve caps
        for f in SIDES + ("up",):
            face = skin.face(slv, f)
            cloud(face, seed + 20 + len(f))
            if f != "up":
                face.clear(face.row >= 6)
                face.clear((face.row == 5) & (face.col % 2 == 0))
        skin.face(slv, "down").clear()


def paint_legs(skin, boot_h):
    for leg, pants, seed in (("rightLeg", "rightPants", 3400), ("leftLeg", "leftPants", 3410)):
        for f in SIDES:
            face = skin.face(leg, f)
            skin_tone(face, SKIN, seed + len(f))
            face.fill(CORAL, face.row <= 2)
        skin.face(leg, "up").fill(CORAL_D)
        skin.face(leg, "down").fill(SKIN_D)
        for face in skin.each(pants):
            face.clear()
        # fluffy cloud cuffs over the boot tops
        for f in SIDES:
            face = skin.face(pants, f)
            cloud(face, seed + 20 + len(f))
            face.clear((face.row < 15) | (face.row >= 19))
            face.clear((face.row == 15) & (face.col % 2 == 0))
    clear_under_shoes(skin, boot_h)
    for leg, pants in (("rightLeg", "rightPants"), ("leftLeg", "leftPants")):
        for f in SIDES:
            face = skin.face(leg, f)
            face.fill(CLOUD_D, face.row >= 15)


def paint_boots(skin):
    for side in ("right", "left"):
        shoe = f"{side}Shoe"
        for face in skin.each(shoe):
            cloud(face, 3500 + face.w + face.h)
        for f in SIDES:
            face = skin.face(shoe, f)
            rows(face, face.h - 2, face.h - 2, GOLD)
            rows(face, face.h - 1, face.h - 1, GOLD_D)
        toe = skin.face(shoe, "north")
        toe.stamp([".C.C.", "CCCCC", ".CCC.", "..C.."], {"C": CORAL}, top=0, left=toe.w // 2 - 2)
        skin.face(shoe, "down").fill(GOLD_D)
