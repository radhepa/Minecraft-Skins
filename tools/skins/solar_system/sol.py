"""Sol the Sun King: molten-gold star alien with white-hot eyes, flame hair,
a 3D corona of rays behind his head, a crimson tunic with a blazing sun
emblem, gold pauldrons and bracers, a flame-hemmed cape and gold boots.
"""

import numpy as np

from paintkit import (SIDES, add_footwear, box, cells, clear_under_shoes, cloth,
                      copy_layer, flame_edge, gradient, rows)
from skinlib import Skin, add_standard_body, noise

ID = "geometry.SolarSystem.Sol"
TEXTURE = "sol.png"
NAME = "Sol the Sun King"
LOC = "Sol"
DETAILS = [
    ("face", "White-hot eyes + 3D corona", {"yaw": 18, "pitch": 6, "dist": 62, "target": 27, "fov": 30}),
    ("back34", "Flame-hemmed cape", {"yaw": 155, "pitch": 10}),
    ("armor", "Gold pauldrons + bracers", {"yaw": -38, "pitch": 12, "dist": 60, "target": 18, "fov": 30}),
]

MOLTEN = (255, 170, 38)
MOLTEN_L = (255, 214, 92)
MOLTEN_D = (236, 118, 18)
LANE = (240, 132, 26)
SPOT = (178, 54, 12)
WHITE_HOT = (255, 252, 226)
FLAME_Y = (255, 236, 120)
FLAME_O = (255, 150, 30)
FLAME_R = (226, 64, 20)
CRIMSON = (150, 22, 34)
CRIMSON_D = (104, 12, 24)
CRIMSON_H = (184, 40, 48)
GOLD = (250, 196, 60)
GOLD_L = (255, 232, 140)
GOLD_D = (196, 128, 26)
GOLD_X = (140, 82, 14)
RUBY = (214, 26, 52)
MOUTH = (130, 24, 10)

# corona: rays radiate from the middle of the head, just behind it
CY, CZ = 28.0, 4.6


def build():
    skin = Skin(ID)
    add_standard_body(skin)
    edges = ("east", "west", "up", "down")
    piv = [0, CY, CZ]
    skin.acc("ray", "head", [-1.25, CY + 5.0, CZ], [2.5, 3.5, 0.5], lowres=edges, pivot=piv)
    skin.acc("rayTip", "head", [-0.75, CY + 8.5, CZ], [1.5, 2.5, 0.5], lowres=edges, pivot=piv)
    skin.acc("rayShort", "head", [-0.75, CY + 5.5, CZ + 0.125], [1.5, 3, 0.5], lowres=edges, pivot=piv, rotation=[0, 0, 22.5])
    for k in range(1, 8):
        rot = [0, 0, 45 * k]
        skin.acc(f"ray{k}", "head", [-1.25, CY + 5.0, CZ], [2.5, 3.5, 0.5], like="ray", pivot=piv, rotation=rot)
        skin.acc(f"rayTip{k}", "head", [-0.75, CY + 8.5, CZ], [1.5, 2.5, 0.5], like="rayTip", pivot=piv, rotation=rot)
        skin.acc(f"rayShort{k}", "head", [-0.75, CY + 5.5, CZ + 0.125], [1.5, 3, 0.5], like="rayShort",
                 pivot=piv, rotation=[0, 0, 22.5 + 45 * k])
    skin.acc("cape3d", "body", [-4, 9.5, 2.3], [8, 14, 0.5], lowres=("north", "east", "west", "up", "down"))
    skin.acc("pauldronRight", "rightArm", [-9, 21.5, -2.5], [5, 3, 5], lowres=("down",))
    skin.acc("pauldronLeft", "leftArm", [4, 21.5, -2.5], [5, 3, 5], like="pauldronRight")
    h = add_footwear(skin, height=3.5, length=5.5, toe=1.0, tongue=False)
    paint_head(skin)
    paint_corona(skin)
    paint_body(skin)
    paint_cape(skin)
    paint_arms(skin)
    paint_legs(skin, h)
    paint_boots(skin)
    return skin


def molten(face, seed, size=4.0, lanes=True):
    """Sun-surface skin: soft bright granules with warmer lanes between."""
    centre, lane = cells(face, seed, size)
    gradient(face, [(0, (255, 196, 70)), (0.7, MOLTEN), (1, (248, 150, 30))], t=centre)
    if lanes:
        face.fill(LANE, lane)
    face.shade(noise((face.h, face.w), seed + 1, 0.02))


def fire(face, seed, top=FLAME_Y, mid=FLAME_O, bottom=FLAME_R):
    """Flickering flame streaks: yellow at the top fading to red below."""
    rs = np.random.RandomState(seed)
    lift = rs.randint(-2, 3, size=face.w)
    t = np.clip((face.row + lift[face.col]) / max(face.h - 1, 1), 0, 1)
    gradient(face, [(0, top), (0.5, mid), (1, bottom)], t=t)
    face.shade(1 + 0.08 * np.sin(face.col * 1.7 + face.row * 0.6 + seed))
    face.shade(noise((face.h, face.w), seed, 0.03))


def paint_head(skin):
    for f in SIDES + ("up", "down"):
        molten(skin.face("head", f), 100 + len(f))
    front = skin.face("head", "north")
    molten(front, 102, size=6, lanes=False)
    # flame hairline: tongues licking down onto the forehead
    hair_edge = flame_edge(front, 110, 2, height=2, period=(3, 5), from_top=False)
    tmp = front.rgba.copy()
    fire(front, 111)
    fringe = front.row <= hair_edge[front.col]
    front.rgba = np.where(fringe[..., None], front.rgba, tmp)
    # deep glow round the eyes, then the white-hot eyes themselves
    # heavy brows, then white-hot eyes ringed in a deep ember glow
    eye = [
        "BBBBB",
        "SWWWO",
        "SWWYO",
        ".OOO.",
    ]
    pal = {"B": SPOT, "S": LANE, "W": WHITE_HOT, "Y": FLAME_Y, "O": MOLTEN_D}
    front.stamp(eye, pal, top=6, left=1)
    front.stamp(eye, pal, top=6, left=10, mirror=True)
    front.set(5, 1, SPOT)
    front.set(5, 14, SPOT)
    # nose bridge glint, cheek flares and a confident grin
    front.set(10, 7, MOLTEN_D)
    front.set(10, 8, MOLTEN_D)
    for c in (1, 2, 13, 14):
        front.set(11, c, FLAME_R)
    front.stamp(["M......M", ".MWWWWM.", "..MMMM.."], {"M": MOUTH, "W": WHITE_HOT}, top=12, left=4)
    for f in ("east", "west", "south", "up"):
        face = skin.face("head", f)
        fire(face, 120 + len(f))
        if f in ("east", "west"):
            # hair covers the top and the back half of each side
            near_front = face.col >= 8 if f == "east" else face.col < 8
            keep = (face.row <= 3) | ~near_front
            tmp = face.rgba.copy()
            molten(face, 130 + len(f))
            face.rgba = np.where(keep[..., None], tmp, face.rgba)
    up = skin.face("head", "up")
    r = np.sqrt((up.row - 7.5) ** 2 + (up.col - 7.5) ** 2) / 10.6
    gradient(up, [(0, WHITE_HOT), (0.35, FLAME_Y), (0.8, FLAME_O), (1, FLAME_R)], t=r)
    up.shade(noise((16, 16), 140, 0.04))

    # hat layer: flames licking up the sides and back, and a gold circlet
    for f in SIDES + ("up", "down"):
        skin.face("hat", f).clear()
    for f in ("east", "west", "south"):
        face = skin.face("hat", f)
        fire(face, 150 + len(f))
        edge = flame_edge(face, 160 + len(f), 9 if f == "south" else 6, height=6, period=(3, 5))
        face.clear(face.row < edge[face.col])
        if f in ("east", "west"):
            near_front = face.col >= 9 if f == "east" else face.col < 7
            face.clear(near_front & (face.row > 4))
    # no hat top: the flames are open above, and its underside would show
    # through them as a thin line over the head
    skin.face("hat", "up").clear()
    band = skin.face("hat", "north")
    rows(band, 2, 3, GOLD)
    rows(band, 2, 2, GOLD_L)
    band.stamp([".G.", "GRG", ".G."], {"G": GOLD_L, "R": RUBY}, top=1, left=6)
    band.stamp([".G.", "GRG", ".G."], {"G": GOLD_L, "R": RUBY}, top=1, left=7)
    for f in ("east", "west", "south"):
        rows(skin.face("hat", f), 2, 3, GOLD)
        rows(skin.face("hat", f), 2, 2, GOLD_L)


def paint_corona(skin):
    for name, base_t in (("ray", 0.0), ("rayTip", 0.55), ("rayShort", 0.2)):
        for face in skin.each(name):
            span = 1.0 - base_t
            t = base_t + span * (face.row / max(face.h - 1, 1))
            # rays point up in their own frame: row 0 is the outer tip
            gradient(face, [(0, FLAME_R), (0.45, FLAME_O), (1, FLAME_Y)], t=1 - t)
            face.shade(noise((face.h, face.w), 180 + face.w + face.h, 0.04))
        for f in ("north", "south"):
            face = skin.face(name, f)
            # bright core line up the middle of each ray
            mid = (face.col == face.w // 2) | (face.col == (face.w - 1) // 2)
            face.fill(FLAME_Y if name == "ray" else (255, 206, 90), mid & (face.row >= 1))
    # darker tip corners so each ray reads as pointed
    for name in ("rayTip", "rayShort"):
        for f in ("north", "south"):
            face = skin.face(name, f)
            face.fill(FLAME_R, (face.row == 0) & ((face.col == 0) | (face.col == face.w - 1)))


def sun_emblem(face, top, left):
    emblem = [
        "....Y....",
        ".Y..Y..Y.",
        "..YGGGY..",
        "..GWWWG..",
        "YYGWWWGYY",
        "..GWWWG..",
        "..YGGGY..",
        ".Y..Y..Y.",
        "....Y....",
    ]
    face.stamp(emblem, {"Y": GOLD, "G": GOLD_L, "W": WHITE_HOT}, top=top, left=left)


def tunic(face, seed):
    cloth(face, CRIMSON, seed, var=0.05, fold=0.04)


def paint_body(skin):
    front = skin.face("body", "north")
    tunic(front, 200)
    # V neck showing molten skin
    neck = (front.row <= 4) & (abs(front.col - 7.5) <= 4.5 - front.row)
    tmp = front.rgba.copy()
    molten(front, 201)
    front.rgba = np.where(neck[..., None], front.rgba, tmp)
    sun_emblem(front, 5, 4)
    # gold belt with a ruby buckle
    for f in SIDES:
        face = skin.face("body", f) if f != "north" else front
        if f != "north":
            tunic(face, 210 + len(f))
        rows(face, 17, 18, GOLD)
        rows(face, 17, 17, GOLD_L)
        rows(face, 19, 19, GOLD_X)
        rows(face, 23, 23, GOLD)
    front.stamp(["GGGG", "GRRG", "GGGG"], {"G": GOLD_D, "R": RUBY}, top=16, left=6)
    cloth(skin.face("body", "up"), CRIMSON_D, 220)
    cloth(skin.face("body", "down"), CRIMSON_D, 221)

    # jacket: gold trim down the V and along the tunic's skirt
    for face in skin.each("jacket"):
        face.clear()
    jk = skin.face("jacket", "north")
    v = abs(jk.col - 7.5) == np.floor(4.5 - jk.row) + 0.5
    jk.fill(GOLD, v & (jk.row <= 4))
    jk.fill(GOLD_L, (jk.row == 0) & ((jk.col <= 2) | (jk.col >= 13)))
    for f in SIDES:
        face = skin.face("jacket", f)
        hem = flame_edge(face, 230 + len(f), 22, height=2, period=(2, 4))
        face.fill(GOLD, (face.row >= hem[face.col]) & (face.row >= 20))
        face.fill(GOLD_L, face.row == hem[face.col])


def paint_cape(skin):
    for face in skin.each("cape3d"):
        cloth(face, CRIMSON_D, 240 + face.w, var=0.05, fold=0.03)
    back = skin.face("cape3d", "south")
    cloth(back, CRIMSON, 250, var=0.06, fold=0.05, freq=0.9)
    # soft vertical folds
    back.shade(1 + 0.08 * np.sin(back.col * 1.1))
    # flame hem: gold-to-red fire licking up from the bottom
    edge = flame_edge(back, 251, 19, height=6, period=(3, 5))
    flames = back.row >= edge[back.col]
    tmp = back.rgba.copy()
    fire(back, 252, top=FLAME_Y, mid=FLAME_O, bottom=FLAME_R)
    t = np.clip((back.row - edge[back.col]) / 8, 0, 1)
    gradient(back, [(0, FLAME_R), (0.5, FLAME_O), (1, FLAME_Y)], t=t, mask=flames)
    back.rgba = np.where(flames[..., None], back.rgba, tmp)
    # ragged bottom: tongues of flame instead of a straight edge
    cut = flame_edge(back, 253, back.h - 1, height=2, period=(2, 3))
    back.clear(back.row > cut[back.col])
    # gold clasp line along the shoulders
    rows(back, 0, 0, GOLD)
    sun_emblem(back, 4, 4)
    inner = skin.face("cape3d", "north")
    inner.clear(inner.row == inner.h - 1)


def paint_pauldrons(skin):
    for face in skin.each("pauldronRight"):
        gradient(face, [(0, GOLD_L), (0.5, GOLD), (1, GOLD_D)])
        face.shade(noise((face.h, face.w), 300 + face.w, 0.04))
        rows(face, face.h - 1, face.h - 1, GOLD_X)
    for f in SIDES:
        face = skin.face("pauldronRight", f)
        face.stamp(["R"], {"R": RUBY}, top=2, left=face.w // 2)
        face.set(1, face.w // 2, GOLD_L)
    up = skin.face("pauldronRight", "up")
    gradient(up, [(0, GOLD), (0.5, GOLD_L), (1, GOLD)], t=up.col / (up.w - 1))
    up.shade(noise((up.h, up.w), 305, 0.04))
    up.fill(RUBY, (up.row == up.h // 2) & (up.col == up.w // 2))


def paint_arms(skin):
    paint_pauldrons(skin)
    for arm, slv, seed in (("rightArm", "rightSleeve", 310), ("leftArm", "leftSleeve", 320)):
        for f in SIDES + ("up", "down"):
            molten(skin.face(arm, f), seed + len(f))
        for face in skin.each(slv):
            face.clear()
        # gold bracers on the forearms (raised on the sleeve layer)
        for f in SIDES:
            face = skin.face(slv, f)
            m = (face.row >= 12) & (face.row <= 19)
            gradient(face, [(0, GOLD_L), (0.4, GOLD), (1, GOLD_D)],
                     t=np.clip((face.row - 12) / 7, 0, 1), mask=m)
            rows(face, 12, 12, GOLD_L)
            rows(face, 19, 19, GOLD_X)
            rows(face, 15, 16, GOLD_D, m & (face.col % 3 == 1))
            if f in ("north", "south"):
                face.stamp(["R", "R"], {"R": RUBY}, top=15, left=face.w // 2)
        hand = skin.face(arm, "down")
        hand.shade(0.92)


def paint_legs(skin, boot_h):
    for leg, pants, outer, seed in (("rightLeg", "rightPants", "east", 400), ("leftLeg", "leftPants", "west", 410)):
        for f in SIDES:
            face = skin.face(leg, f)
            cloth(face, CRIMSON_D, seed + len(f), var=0.05, fold=0.05)
            if f == outer:
                face.fill(GOLD, (face.col == 3) | (face.col == 4))
                face.fill(GOLD_L, face.col == 3)
            rows(face, 0, 0, GOLD_X)
        skin.face(leg, "up").fill(CRIMSON_D)
        skin.face(leg, "down").fill(CRIMSON_D)
        for face in skin.each(pants):
            face.clear()
        # gold knee guards with a ruby stud on the trouser layer
        knee = skin.face(pants, "north")
        knee.fill(GOLD, box(knee, 8, 1, 11, 6))
        knee.fill(GOLD_L, box(knee, 8, 1, 8, 6))
        knee.fill(GOLD_D, box(knee, 11, 1, 11, 6))
        knee.set(9, 3, RUBY)
        knee.set(9, 4, RUBY)
    clear_under_shoes(skin, boot_h)


def paint_boots(skin):
    for side in ("right", "left"):
        shoe = f"{side}Shoe"
        for face in skin.each(shoe):
            gradient(face, [(0, GOLD_L), (0.35, GOLD), (1, GOLD_D)])
            face.shade(noise((face.h, face.w), 500 + face.w, 0.04))
        for f in SIDES:
            face = skin.face(shoe, f)
            rows(face, 0, 0, GOLD_L)
            rows(face, face.h - 2, face.h - 1, GOLD_X)
            rows(face, face.h - 3, face.h - 3, GOLD_D)
            # flame trim round the ankle cuff
            edge = flame_edge(face, 510 + len(f) + (side == "left"), 3, height=2, period=(2, 3))
            flame = face.row <= edge[face.col]
            face.fill(FLAME_O, flame & (face.row >= 1))
            face.fill(FLAME_R, flame & (face.row >= 2))
        toe = skin.face(shoe, "north")
        toe.stamp(["R"], {"R": RUBY}, top=4, left=toe.w // 2)
        skin.face(shoe, "down").fill(GOLD_X)
        top = skin.face(shoe, "up")
        top.fill(GOLD_L, (top.col == 0) | (top.col == top.w - 1))
