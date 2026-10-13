"""Neptide: deep-blue sea-king alien from Neptune with glowing aqua eyes,
gills and bioluminescent freckles, a 3D dorsal-fin crest and fin ears, a teal
scale breastplate with a pearl necklace, forearm and calf fins, wave-trimmed
trousers, webbed feet and a gold 3D trident slung across his back.
"""

import numpy as np

from paintkit import (SIDES, add_footwear, box, clear_under_shoes, cloth,
                      eye_glow, gradient, rows, skin_tone)
from skinlib import Skin, add_standard_body, noise

ID = "geometry.SolarSystem.Neptide"
TEXTURE = "neptide.png"
NAME = "Neptide"
LOC = "Neptide"
DETAILS = [
    ("face", "Glowing eyes, gills + fin crest", {"yaw": 30, "pitch": 6, "dist": 48, "target": 27, "fov": 30}),
    ("back34", "3D trident across the back", {"yaw": 150, "pitch": 10}),
    ("fins", "Forearm + calf fins, webbed feet", {"yaw": -60, "pitch": 10, "dist": 80, "target": 12, "fov": 30}),
]

SKIN = (50, 100, 206)
SKIN_L = (92, 150, 236)
SKIN_D = (30, 62, 152)
SKIN_X = (20, 40, 110)
BELLY = (120, 182, 244)
GLOW = (120, 244, 255)
GLOW_C = (226, 255, 255)
GLOW_R = (40, 170, 210)
FIN = (40, 196, 200)
FIN_L = (130, 236, 228)
FIN_D = (20, 120, 150)
ARMOR = (26, 140, 146)
ARMOR_L = (60, 186, 180)
ARMOR_D = (14, 92, 104)
GOLD = (246, 196, 72)
GOLD_L = (255, 232, 150)
GOLD_D = (186, 128, 34)
PEARL = (246, 244, 236)
PEARL_D = (196, 204, 214)
NAVY = (22, 34, 86)
NAVY_D = (14, 22, 60)
FOAM = (220, 244, 255)
KELP = (46, 120, 74)
KELP_D = (30, 86, 52)
MOUTH = (14, 20, 54)

# trident: in its own bone, tilted across the back
TRI_Z = 2.7


def build():
    skin = Skin(ID)
    add_standard_body(skin)
    # dorsal crest along the top of the head, highest at the back
    skin.acc("crestFront", "head", [-0.5, 32, -3.5], [1, 2.5, 3], lowres=("up", "down", "north", "south"))
    skin.acc("crestMid", "head", [-0.5, 32, -0.5], [1, 4.5, 3], lowres=("up", "down", "north", "south"))
    skin.acc("crestBack", "head", [-0.5, 30.5, 2.5], [1, 4.5, 2.5], lowres=("up", "down", "north", "south"))
    for side, x0 in (("Right", -5.0), ("Left", 4.5)):
        skin.acc(f"finEar{side}", "head", [x0, 26.5, -0.5], [0.5, 3.5, 3], lowres=("up", "down", "north", "south"))
        skin.acc(f"finEarTip{side}", "head", [x0, 29, 2.5], [0.5, 2, 1.5], lowres=("up", "down", "north", "south"))
    # fins on the back of the forearms and calves share one texture
    skin.acc("finArmRight", "rightArm", [-6.25, 12.5, 2], [0.5, 4.5, 2], lowres=("up", "down", "north", "south"))
    skin.acc("finArmLeft", "leftArm", [5.75, 12.5, 2], [0.5, 4.5, 2], like="finArmRight")
    skin.acc("finLegRight", "rightLeg", [-2.15, 3, 2], [0.5, 4.5, 2], like="finArmRight")
    skin.acc("finLegLeft", "leftLeg", [1.65, 3, 2], [0.5, 4.5, 2], like="finArmRight")
    # the trident, upright in its bone; the bone leans it over the shoulder
    skin.bone("trident", "body", [0, 18, TRI_Z], rotation=[0, 0, 38])
    skin.acc("shaft", "trident", [-0.375, 6, TRI_Z], [0.75, 11, 0.75], lowres=("up", "down"))
    skin.acc("shaft2", "trident", [-0.375, 17, TRI_Z], [0.75, 11, 0.75], like="shaft")
    skin.acc("pommel", "trident", [-0.75, 5, TRI_Z - 0.375], [1.5, 1, 1.5])
    skin.acc("guard", "trident", [-2.5, 28, TRI_Z - 0.125], [5, 1, 1], lowres=("up", "down"))
    skin.acc("prongMid", "trident", [-0.5, 29, TRI_Z], [1, 4.5, 0.75], lowres=("up", "down", "east", "west"))
    skin.acc("prongRight", "trident", [-2.5, 29, TRI_Z], [1, 3, 0.75], lowres=("up", "down", "east", "west"))
    skin.acc("prongLeft", "trident", [1.5, 29, TRI_Z], [1, 3, 0.75], like="prongRight")
    h = add_footwear(skin, height=2.0, length=6.0, toe=2.0, tongue=False)
    paint_head(skin)
    paint_fins(skin)
    paint_trident(skin)
    paint_body(skin)
    paint_arms(skin)
    paint_legs(skin, h)
    paint_feet(skin)
    return skin


def ocean_skin(face, seed, base=SKIN):
    """Deep-blue hide: soft mottling plus darker fish-like stripes."""
    skin_tone(face, base, seed, var=0.03)
    face.shade(1 + 0.05 * np.sin(face.X * 1.3 + face.Y * 0.7 + face.Z * 0.9 + seed))


def freckles(face, cells):
    for r, c in cells:
        face.set(r, c, GLOW)


def paint_head(skin):
    for f in SIDES + ("up", "down"):
        ocean_skin(skin.face("head", f), 1200 + len(f))
    front = skin.face("head", "north")
    # lighter muzzle and cheeks
    m = box(front, 10, 4, 15, 11) & ~(((front.col == 4) | (front.col == 11)) & (front.row == 10))
    gradient(front, [(0, SKIN_L), (1, (78, 134, 226))], t=np.clip((front.row - 10) / 5, 0, 1), mask=m)
    front.shade(noise((16, 16), 1201, 0.03), m)
    # heavy brow and darker crown with stripes
    gradient(front, [(0, SKIN_X), (1, SKIN)], t=np.clip(front.row / 4, 0, 1), mask=front.row <= 4)
    rows(front, 5, 5, SKIN_X, (front.col >= 1) & (front.col <= 14) & (front.col != 7) & (front.col != 8))
    # glowing eyes, angled toward the nose
    for left, flip in ((2, False), (10, True)):
        cells = [(6, 0), (6, 1), (6, 2), (6, 3), (7, 0), (7, 1), (7, 2), (7, 3), (8, 1), (8, 2), (8, 3)]
        if flip:
            cells = [(r, 3 - c) for r, c in cells]
        eye_glow(front, [(r, left + c) for r, c in cells], GLOW_C, GLOW, GLOW_R)
        for c in range(4):
            front.set(7, left + c, GLOW_C if c in ((1, 2) if not flip else (1, 2)) else GLOW)
    front.set(10, 7, SKIN_D)
    front.set(10, 8, SKIN_D)
    # grin with two little fangs
    front.stamp(["M.....M", ".MMMMM.", ".F...F."], {"M": MOUTH, "F": PEARL}, top=12, left=4)
    front.set(12, 11, MOUTH)
    freckles(front, [(9, 0), (10, 1), (9, 15), (10, 14)])
    # gills on the sides of the head, near the jaw
    for f in ("east", "west"):
        side = skin.face("head", f)
        front_cols = range(10, 14) if f == "east" else range(2, 6)
        for k, c in enumerate(front_cols):
            if k % 2 == 0:
                rows(side, 10, 14, SKIN_X, side.col == c)
                rows(side, 10, 14, SKIN_L, side.col == c + (1 if f == "east" else -1))
        side.fill(SKIN_X, (side.row <= 3) & (side.col % 4 == 1))
    back = skin.face("head", "south")
    back.fill(SKIN_X, (back.row % 4 == 1) & (back.row <= 12))
    up = skin.face("head", "up")
    up.fill(SKIN_D)
    up.fill(SKIN_X, (up.col % 4 == 1))
    for face in skin.each("hat"):
        face.clear()


def fin_membrane(face, seed, rays_vertical=True):
    """Translucent-looking fin: teal webbing between darker bony rays."""
    t = face.row / max(face.h - 1, 1)
    gradient(face, [(0, FIN_L), (0.6, FIN), (1, FIN_D)], t=t)
    lines = face.col if rays_vertical else face.row
    face.fill(FIN_D, lines % 3 == 1)
    face.shade(noise((face.h, face.w), seed, 0.04))


def paint_fins(skin):
    for name in ("crestFront", "crestMid", "crestBack"):
        for face in skin.each(name):
            fin_membrane(face, 1300 + face.w + face.h)
        for f in ("east", "west"):
            face = skin.face(name, f)
            # scalloped top edge between the rays
            face.clear((face.row == 0) & (face.col % 3 != 1))
            face.fill(FIN_L, (face.row == 1) & (face.col % 3 != 1))
    for side in ("Right", "Left"):
        for name in (f"finEar{side}", f"finEarTip{side}"):
            for face in skin.each(name):
                fin_membrane(face, 1310 + face.w, rays_vertical=False)
            for f in ("east", "west"):
                face = skin.face(name, f)
                back_col = 0 if f == "east" else face.w - 1
                face.clear((face.col == back_col) & (face.row % 2 == 0))
    for face in skin.each("finArmRight"):
        fin_membrane(face, 1320, rays_vertical=False)
    for f in ("east", "west"):
        face = skin.face("finArmRight", f)
        tip_col = 0 if f == "east" else face.w - 1
        face.clear((face.col == tip_col) & (face.row % 3 != 1))


def paint_trident(skin):
    for name in ("shaft", "pommel", "guard", "prongMid", "prongRight"):
        for face in skin.each(name):
            gradient(face, [(0, GOLD_L), (0.5, GOLD), (1, GOLD_D)], t=face.col / max(face.w - 1, 1))
            face.shade(noise((face.h, face.w), 1400 + face.w + face.h, 0.04))
    for f in SIDES:
        sh = skin.face("shaft", f)
        sh.fill(GOLD_D, sh.row % 6 == 0)            # wrapped grip bands
        sh.fill(PEARL, (sh.row % 6 == 3) & (sh.col == 0))
    for name in ("prongMid", "prongRight"):
        for f in ("north", "south"):
            p = skin.face(name, f)
            p.fill(GOLD_L, p.row <= 1)
            p.clear((p.row == 0) & (p.col != p.w // 2) & (p.col != (p.w - 1) // 2))
    g = skin.face("guard", "north")
    g.fill(PEARL, (g.col == g.w // 2) | (g.col == g.w // 2 - 1))
    skin.face("guard", "south").rgba = g.rgba.copy()
    for face in skin.each("pommel"):
        face.fill(PEARL)
        face.shade(noise((face.h, face.w), 1410, 0.04))


def scales(face, base, light, dark, seed, mask=None):
    """Overlapping scale arches in rows."""
    old = face.rgba.copy()
    face.fill(base)
    face.shade(noise((face.h, face.w), seed, 0.04))
    r, c = face.row, face.col
    off = (r // 3) % 2 * 2
    cc = (c + off) % 4
    face.fill(dark, (r % 3 == 2) & (cc != 0))
    face.fill(dark, (cc == 0) & (r % 3 != 0))
    face.fill(light, (r % 3 == 0) & (cc == 2))
    if mask is not None:
        face.rgba = np.where(mask[..., None], face.rgba, old)


def paint_body(skin):
    for f in SIDES:
        face = skin.face("body", f)
        ocean_skin(face, 1500 + len(f))
        if f == "north":
            face.fill(BELLY, box(face, 0, 4, 23, 11))
            face.shade(noise((24, 16), 1501, 0.03), box(face, 0, 4, 23, 11))
    ocean_skin(skin.face("body", "up"), 1502)
    ocean_skin(skin.face("body", "down"), 1503)
    # breastplate + belt on the jacket layer
    for face in skin.each("jacket"):
        face.clear()
    jk = skin.face("jacket", "north")
    plate = (jk.row >= 3) & (jk.row <= 15)
    scales(jk, ARMOR, ARMOR_L, ARMOR_D, 1510, mask=plate)
    jk.fill(GOLD, (jk.row == 3) & plate)
    jk.fill(GOLD_D, (jk.row == 15))
    # pearl necklace dipping onto the chest
    for c in range(3, 13):
        r = 1 + int(round(1.6 - abs(c - 7.5) * 0.35))
        jk.set(r + 1, c, PEARL if c % 2 else PEARL_D)
    jk.stamp(["GPG", ".G."], {"G": GOLD, "P": GLOW}, top=4, left=6)
    jk.stamp(["GPG", ".G."], {"G": GOLD, "P": GLOW}, top=4, left=7)
    # trident emblem
    emblem = ["Y.Y.Y", "Y.Y.Y", "YYYYY", "..Y..", "..Y..", "..Y.."]
    jk.stamp(emblem, {"Y": GOLD}, top=7, left=5)
    # kelp sash and pearl clasp
    for f in SIDES:
        face = skin.face("jacket", f)
        if f != "north":
            scales(face, ARMOR, ARMOR_L, ARMOR_D, 1520 + len(f), mask=(face.row >= 3) & (face.row <= 15))
            rows(face, 3, 3, GOLD)
            rows(face, 15, 15, GOLD_D)
        rows(face, 16, 18, KELP)
        rows(face, 18, 18, KELP_D)
        face.fill(KELP_D, (face.row >= 16) & (face.row <= 17) & (face.col % 3 == 0))
    jk.stamp(["PP", "PP"], {"P": PEARL}, top=16, left=7)
    # sash ends hanging down one hip, ragged like seaweed
    for r in range(19, 23):
        for c in (10, 11):
            if not (r == 22 and c == 11):
                jk.set(r, c, KELP if (r + c) % 2 else KELP_D)
    skin.face("jacket", "up").clear()
    skin.face("jacket", "down").clear()


def paint_arms(skin):
    for arm, slv, seed in (("rightArm", "rightSleeve", 1600), ("leftArm", "leftSleeve", 1610)):
        for f in SIDES + ("up", "down"):
            face = skin.face(arm, f)
            ocean_skin(face, seed + len(f))
            if f in SIDES:
                scales(face, SKIN_L, BELLY, SKIN, seed + 5 + len(f), mask=(face.row >= 13) & (face.row <= 19))
        freckles(skin.face(arm, "north"), [(4, 2), (6, 5), (8, 3)])
        skin.face(arm, "down").fill(SKIN_L)
        for face in skin.each(slv):
            face.clear()
        # gold shoulder guard + bracer cuffs with a pearl
        for f in SIDES:
            face = skin.face(slv, f)
            rows(face, 0, 3, ARMOR)
            face.fill(ARMOR_L, (face.row == 0))
            rows(face, 4, 4, GOLD)
            rows(face, 11, 12, GOLD)
            rows(face, 11, 11, GOLD_L)
            rows(face, 20, 20, GOLD)
            face.fill(GOLD_D, (face.row == 12) & (face.col % 2 == 0))
            if f == "north":
                face.set(11, face.w // 2, PEARL)
        up = skin.face(slv, "up")
        up.fill(ARMOR)
        up.fill(ARMOR_L, (up.col + up.row) % 4 == 0)


def waves(face, base_row):
    """A curling white wave crest along base_row."""
    for c in range(face.w):
        k = c % 6
        dr = (0, -1, -1, -2, -1, 0)[k]
        face.set(base_row + dr, c, FOAM)
        if k in (2, 3):
            face.set(base_row + dr + 1, c, (150, 200, 240))


def paint_legs(skin, foot_h):
    for leg, pants, seed in (("rightLeg", "rightPants", 1700), ("leftLeg", "leftPants", 1710)):
        for f in SIDES:
            face = skin.face(leg, f)
            cloth(face, NAVY, seed + len(f), var=0.05, fold=0.05)
            lower = face.row >= 15
            gradient(face, [(0, (34, 64, 150)), (1, (50, 104, 196))], t=np.clip((face.row - 15) / 5, 0, 1), mask=lower)
            waves(face, 15)
        skin.face(leg, "up").fill(NAVY)
        skin.face(leg, "down").fill(SKIN_L)
        for face in skin.each(pants):
            face.clear()
        knee = skin.face(pants, "north")
        knee.fill(GOLD, box(knee, 8, 1, 10, 6))
        knee.fill(GOLD_L, box(knee, 8, 1, 8, 6))
        knee.set(9, 3, PEARL)
        knee.set(9, 4, PEARL)
    clear_under_shoes(skin, foot_h)


def paint_feet(skin):
    for side in ("right", "left"):
        foot = f"{side}Shoe"
        for face in skin.each(foot):
            ocean_skin(face, 1800 + face.w, SKIN)
        toe = skin.face(foot, "north")
        # webbed toes with pale claws
        for c in range(toe.w):
            if c % 3 == 1:
                toe.set(toe.h - 1, c, PEARL)
            elif c % 3 == 0:
                toe.set(toe.h - 2, c, SKIN_X)
        top = skin.face(foot, "up")
        top.fill(SKIN_D, (top.col % 3 == 0) & (top.row >= top.h - 3))
        top.fill(FIN, (top.col % 3 == 2) & (top.row >= top.h - 2))
        skin.face(foot, "down").fill(SKIN_X)
        for f in ("east", "west"):
            face = skin.face(foot, f)
            face.fill(SKIN_D, face.row == face.h - 1)
