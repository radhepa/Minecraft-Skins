"""Moonlight Witch: long purple hair, open violet coat with a gold crescent
brooch, black pleated dress, striped stockings and chunky gold-strapped boots.
"""

import numpy as np

from paintkit import (SIDES, add_footwear, box, clear_under_shoes, cloth, hair,
                      paint_boots, rows, skin_tone)
from skinlib import Skin, add_standard_body, noise

ID = "geometry.MidnightMischief.MoonlightWitch"
TEXTURE = "moonlight_witch.png"
NAME = "Moonlight Witch"
LOC = "MoonlightWitch"
REF_BOX = (470, 90, 710, 540)  # crop of reference/midnight_mischief_lineup.webp
DETAILS = [
    ("face", "Hair + bangs (3D)", {"yaw": 22, "pitch": 8, "dist": 42, "target": 26, "fov": 30}),
    ("back34", "Long 3D hair down the back", {"yaw": 200, "pitch": 10}),
    ("boots", "Bell cuffs + platform boots", {"yaw": 35, "pitch": 14, "dist": 50, "target": 8, "fov": 30}),
]

SKIN = (124, 74, 46)
SKIN_D = (102, 58, 36)
SKIN_H = (146, 92, 60)
HAIR = (162, 98, 216)
HAIR_D = (116, 60, 170)
HAIR_L = (198, 140, 238)
HAIR_K = (230, 190, 252)
COAT = (84, 40, 134)
COAT_D = (58, 26, 98)
COAT_H = (112, 62, 166)
COAT_EDGE = (150, 96, 208)
GOLD = (244, 180, 60)
GOLD_D = (196, 128, 34)
DRESS = (34, 26, 38)
DRESS_D = (22, 16, 26)
DRESS_H = (54, 42, 58)
STRIPE = (190, 132, 228)
STRIPE_D = (34, 24, 40)
PINK = (236, 146, 206)

BOOTS = {"upper": (40, 32, 46), "hi": (66, 54, 74), "dark": (24, 18, 28),
         "strap": GOLD, "strap_dark": GOLD_D, "sole": (30, 24, 34), "sole_dark": (18, 14, 22)}


def build():
    skin = Skin(ID, slim=True)
    add_standard_body(skin)
    # long hair down the back and two locks over the coat, on the body bone
    skin.acc("hairBack", "body", [-4.5, 12, 2.5], [9, 12, 1.5],
             faces=("south", "east", "west", "down"))
    skin.acc("lockRight", "body", [-4.25, 14, -3.25], [1.5, 10, 1],
             faces=("north", "east", "west", "down"))
    skin.acc("lockLeft", "body", [2.75, 17, -3.25], [1.5, 7, 1],
             faces=("north", "east", "west", "down"))
    # bell-shaped coat cuffs riding on the arms
    skin.acc("rightCuff", "rightArm", [-7, 14, -2], [3, 2, 4], inflate=0.6)
    skin.acc("leftCuff", "leftArm", [4, 14, -2], [3, 2, 4], inflate=0.6)
    h = add_footwear(skin, height=4.0, length=5.5, toe=1.0, tongue=False)

    paint_head(skin)
    paint_hair_acc(skin)
    paint_body(skin)
    paint_arms(skin)
    paint_legs(skin, h)
    paint_boots(skin, BOOTS, 300, straps=(2, 4))
    return skin


# ===================================================================== head
BANG_BOTTOM = [15, 15, 9, 4, 3, 3, 4, 2, 3, 3, 4, 3, 4, 9, 15, 15]


def paint_head(skin):
    front = skin.face("head", "north")
    skin_tone(front, SKIN, 200)
    hair_mask = front.row <= np.array(BANG_BOTTOM)[front.col]
    hair(front, HAIR, HAIR_D, HAIR_L, 201, mask=hair_mask, shine=HAIR_K)
    # shadow under the bangs
    under = (front.row == np.array(BANG_BOTTOM)[front.col] + 1) & ~hair_mask
    front.shade(np.where(under, 0.82, 1.0))
    eye = [
        "EEE.",
        "WIPW",
        "WiIW",
    ]
    pal = {"E": (28, 18, 30), "W": (246, 240, 250), "P": (232, 214, 252),
           "I": (72, 32, 104), "i": (150, 92, 204)}
    front.stamp(eye, pal, top=7, left=3)
    front.stamp(eye, pal, top=7, left=9, mirror=True)
    front.set(6, 2, (28, 18, 30))
    front.set(6, 13, (28, 18, 30))
    front.set(10, 7, SKIN_D)
    front.set(11, 8, SKIN_D)
    front.stamp(["m....m", ".mmmm.", "..pp.."],
                {"m": (74, 36, 32), "p": (156, 84, 82)}, top=11, left=5)
    for c in (3, 4, 11, 12):
        front.set(11, c, (146, 80, 72))
    rows(front, 15, 15, SKIN_D, ~hair_mask)

    for f in ("east", "west", "south", "up"):
        face = skin.face("head", f)
        hair(face, HAIR, HAIR_D, HAIR_L, 210 + len(f), shine=HAIR_K)
    for f, front_cols in (("east", (11, 14)), ("west", (1, 4))):
        side = skin.face("head", f)
        a, b = front_cols
        skin_tone(side, SKIN, 220)
        hair(side, HAIR, HAIR_D, HAIR_L, 221 + a,
             mask=~box(side, 6, a, 15, b))
        ear = a + 1 if f == "east" else b - 2
        side.fill(SKIN_D, box(side, 8, ear, 10, ear + 1))
    bottom = skin.face("head", "down")
    skin_tone(bottom, SKIN_D, 230)
    hair(bottom, HAIR_D, HAIR_D, HAIR, 231, mask=(bottom.row <= 9) | (bottom.col <= 1) | (bottom.col >= 14))

    # hat layer: wavy volume around the head + bangs
    hat_front = skin.face("hat", "north")
    hair(hat_front, HAIR, HAIR_D, HAIR_L, 240, shine=HAIR_K)
    keep = hat_front.row <= np.array(BANG_BOTTOM)[hat_front.col] - 1
    keep |= (hat_front.col <= 1) | (hat_front.col >= 14)
    hat_front.clear(~keep)
    for f in ("east", "west", "south", "up"):
        face = skin.face("hat", f)
        hair(face, HAIR, HAIR_D, HAIR_L, 250 + len(f), shine=HAIR_K)
        if f in ("east", "west"):
            a, b = (11, 14) if f == "east" else (1, 4)
            face.clear(box(face, 6, a, 15, b))
            # curly, uneven lower edge
            face.clear((face.row == 15) & (face.col % 3 == 1))
    skin.face("hat", "down").clear()


def paint_hair_acc(skin):
    for name, seed in (("hairBack", 260), ("lockRight", 270), ("lockLeft", 280)):
        for face in skin.each(name):
            hair(face, HAIR, HAIR_D, HAIR_L, seed + face.w, shine=HAIR_K)
    back = skin.face("hairBack", "south")
    # wavy, curling ends
    rs = np.random.RandomState(7)
    ends = 21 + rs.randint(0, 3, size=back.w)
    back.clear(back.row > ends[back.col])
    back.fill(HAIR_D, back.row == ends[back.col])
    for f in ("east", "west"):
        side = skin.face("hairBack", f)
        side.clear(side.row >= 22)
    for name in ("lockRight", "lockLeft"):
        face = skin.face(name, "north")
        face.fill(HAIR_K, (face.col == 1) & (face.row % 5 == 2))
        h = face.h
        face.clear((face.row == h - 1) & (face.col == 2))


# ==================================================================== torso
def coat_panel(face, seed):
    cloth(face, COAT, seed, var=0.05, fold=0.07, freq=0.9)


def paint_body(skin):
    for layer, seed in (("body", 310), ("jacket", 320)):
        front = skin.face(layer, "north")
        coat_panel(front, seed)
        center = (front.col >= 4) & (front.col <= 11)
        cloth(front, DRESS, seed + 1, var=0.12, fold=0.0, mask=center)
        # neckline + choker
        skin_v = center & (front.row <= 2) & (abs(front.col - 7.5) <= 3 - front.row)
        front.fill(SKIN, skin_v)
        rows(front, 0, 0, SKIN, center)
        rows(front, 1, 1, COAT_H, center)
        front.set(1, 7, GOLD)
        # bodice seams, gold belt, pleated skirt
        front.fill(DRESS_H, center & ((front.col == 6) | (front.col == 9)) & (front.row >= 3) & (front.row <= 10))
        rows(front, 11, 11, GOLD, center)
        rows(front, 12, 12, GOLD_D, center)
        front.fill((60, 40, 30), box(front, 11, 7, 12, 8))
        skirt = center & (front.row >= 13)
        front.fill(DRESS_D, skirt & (front.col % 2 == 0))
        front.fill(DRESS_H, skirt & (front.col % 4 == 1))
        for r, c in ((13, 5), (14, 5), (15, 4)):
            front.set(r, c, GOLD_D)
        # fuzzy lilac coat edges + brooch + buttons
        front.fill(COAT_EDGE, ((front.col == 3) | (front.col == 12)) & (front.row % 3 != 2))
        front.fill(COAT_D, ((front.col == 3) | (front.col == 12)) & (front.row % 3 == 2))
        moon = [".GG", "G..", "G..", ".GG"]
        front.stamp(moon, {"G": GOLD}, top=4, left=13)
        front.set(4, 14, GOLD_D)
        for r in (17, 20):
            front.set(r, 12, GOLD)
            front.set(r, 3, GOLD)
        if layer == "jacket":
            front.clear(center)
            # lapels fold out at the top
            front.fill(COAT_H, box(front, 0, 2, 2, 3) | box(front, 0, 12, 2, 13))
        for f in ("east", "west", "south"):
            face = skin.face(layer, f)
            coat_panel(face, seed + len(f))
            if f == "south":
                face.fill(COAT_D, face.col == 8)
                rows(face, 0, 1, COAT_D)
            else:
                face.fill(COAT_D, face.col == 4)
        top = skin.face(layer, "up")
        coat_panel(top, seed + 9)
        bottom = skin.face(layer, "down")
        coat_panel(bottom, seed + 10)
        if layer == "jacket":
            bottom.clear((bottom.col >= 4) & (bottom.col <= 11))
        else:
            bottom.fill(DRESS_D, (bottom.col >= 4) & (bottom.col <= 11))


# ===================================================================== arms
def paint_arms(skin):
    for arm, slv, cuff, outer, seed in (("rightArm", "rightSleeve", "rightCuff", "east", 400),
                                        ("leftArm", "leftSleeve", "leftCuff", "west", 420)):
        for layer, s in ((arm, seed), (slv, seed + 7)):
            for f in SIDES:
                face = skin.face(layer, f)
                hand = face.row >= 19
                coat_panel(face, s + len(f))
                rows(face, 16, 16, COAT_EDGE)
                rows(face, 17, 17, GOLD)
                rows(face, 18, 18, GOLD_D)
                skin_tone_mask(face, hand, s)
                if layer == slv:
                    face.clear(hand)
            o = skin.face(layer, outer)
            if arm == "rightArm":
                star = [".P.", "PPP", ".P."]
                o.stamp(star, {"P": PINK}, top=4, left=2)
                o.set(5, 3, (255, 210, 240))
            skin.face(layer, "east" if outer == "west" else "west").shade(0.9)
            coat_panel(skin.face(layer, "up"), s + 9)
            bottom = skin.face(layer, "down")
            if layer == arm:
                skin_tone(bottom, SKIN_D, s + 10)
            else:
                bottom.clear()
        for f in SIDES:
            face = skin.face(cuff, f)
            coat_panel(face, seed + 30 + len(f))
            rows(face, 0, 0, COAT_EDGE)
            rows(face, face.h - 1, face.h - 1, GOLD)
        coat_panel(skin.face(cuff, "up"), seed + 40)
        bottom = skin.face(cuff, "down")
        bottom.fill(GOLD_D)
        bottom.clear(box(bottom, 1, 1, bottom.h - 2, bottom.w - 2))


def skin_tone_mask(face, mask, seed):
    tone = np.array(SKIN, float) * noise((face.h, face.w), seed + 77, 0.03)[..., None]
    face.rgba[mask, :3] = tone[mask]
    face.rgba[mask, 3] = 255
    face.shade(np.where(face.row == 19, 0.85, 1.0))


# ===================================================================== legs
def paint_legs(skin, boot_h):
    for leg, pants, outer, seed in (("rightLeg", "rightPants", "east", 500),
                                    ("leftLeg", "leftPants", "west", 520)):
        for f in SIDES:
            face = skin.face(leg, f)
            cloth(face, DRESS, seed + len(f), var=0.12, fold=0.0)
            face.fill(DRESS_D, (face.row <= 3) & (face.col % 2 == 0))
            rows(face, 4, 5, SKIN)
            face.shade(np.where(face.row == 4, 0.8, 1.0))
            for r in range(6, 24):
                rows(face, r, r, STRIPE if (r // 2) % 2 == 0 else STRIPE_D)
            face.shade(noise((face.h, face.w), seed + 9 + len(f), 0.05))
        skin.face(leg, "up").fill(DRESS_D)
        skin.face(leg, "down").fill(STRIPE_D)

        # overlay: pleated skirt flare + coat tails hanging round the outside
        for f in SIDES:
            face = skin.face(pants, f)
            coat_panel(face, seed + 30 + len(f))
            face.fill(COAT_EDGE, face.row == 14)
            face.clear(face.row > 14)
            if f == "north":
                outer_cols = face.col <= 1 if leg == "rightLeg" else face.col >= 6
                skirt = (face.row <= 3) & ~outer_cols
                face.fill(DRESS, skirt)
                face.fill(DRESS_D, skirt & (face.col % 2 == 0))
                face.fill(COAT_EDGE, (face.col == (2 if leg == "rightLeg" else 5)) & (face.row <= 14))
                face.clear(~outer_cols & ~skirt & (face.col != (2 if leg == "rightLeg" else 5)))
            elif f != outer and f != "south":
                skirt = face.row <= 3
                face.fill(DRESS, skirt)
                face.clear(~skirt)
        skin.face(pants, "up").clear()
        skin.face(pants, "down").clear()
    clear_under_shoes(skin, boot_h)
