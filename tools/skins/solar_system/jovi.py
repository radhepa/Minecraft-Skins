"""Jovi: friendly gas-giant cyclops from Jupiter. Cream, tan and rust bands
swirl across his whole body, his one big eye is the Great Red Spot, and the
four Galilean moons (Io, Europa, Ganymede, Callisto) float round his head.
He wears a storm-grey vest with a gold lightning bolt, 3D thundercloud
shoulder pads, a lightning belt buckle and heavy boots.
"""

import numpy as np

from paintkit import (SIDES, add_footwear, box, clear_under_shoes, cloth,
                      gradient, paint_boots, rows)
from skinlib import Skin, add_standard_body, noise

ID = "geometry.SolarSystem.Jovi"
TEXTURE = "jovi.png"
NAME = "Jovi"
LOC = "Jovi"
DETAILS = [
    ("face", "Great Red Spot eye + moons", {"yaw": 22, "pitch": 10, "dist": 60, "target": 28, "fov": 30}),
    ("clouds", "Thundercloud shoulders", {"yaw": -40, "pitch": 14, "dist": 64, "target": 20, "fov": 30}),
    ("back34", "Banded gas-giant skin", {"yaw": 150, "pitch": 10}),
]

BANDS = [(242, 230, 204), (226, 196, 150), (204, 150, 98), (178, 108, 70), (226, 196, 150),
         (242, 230, 204), (196, 140, 92), (150, 92, 62)]
SPOT = (214, 84, 52)
SPOT_L = (246, 146, 96)
SPOT_D = (160, 52, 36)
PUPIL = (40, 20, 20)
WHITE = (250, 246, 236)
MOUTH = (90, 36, 30)
STORM = (74, 80, 104)
STORM_D = (50, 54, 74)
STORM_H = (100, 108, 136)
CLOUD = (150, 156, 178)
CLOUD_L = (190, 196, 214)
CLOUD_D = (108, 114, 138)
BOLT = (255, 214, 60)
BOLT_L = (255, 244, 170)
BOLT_D = (214, 150, 30)
TROUSER = (64, 54, 50)
TROUSER_D = (44, 36, 34)

BOOTS = {"upper": (92, 70, 56), "hi": (122, 96, 76), "dark": (62, 46, 36), "strap": BOLT_D,
         "strap_dark": BOLT, "sole": (44, 36, 32), "sole_dark": (28, 22, 20)}

# Galilean moons on a tilted orbit round the head: (name, angle, size)
MOONS = [("io", 35, 2.0), ("europa", 125, 1.5), ("ganymede", 215, 2.5), ("callisto", 305, 2.0)]
ORBIT_R, ORBIT_Y = 8.0, 30.0


def build():
    skin = Skin(ID)
    add_standard_body(skin)
    skin.bone("orbit", "head", [0, ORBIT_Y, 0], rotation=[12, 0, -10])
    for name, ang, size in MOONS:
        a = np.radians(ang)
        x, z = ORBIT_R * np.sin(a), -ORBIT_R * np.cos(a)
        skin.acc(name, "orbit", [round(x - size / 2, 3), ORBIT_Y - size / 2, round(z - size / 2, 3)],
                 [size, size, size])
    skin.acc("cloudR", "rightArm", [-9.25, 21.25, -2.75], [5.5, 3.25, 5.5], lowres=("down",))
    skin.acc("cloudL", "leftArm", [3.75, 21.25, -2.75], [5.5, 3.25, 5.5], like="cloudR")
    skin.acc("puffR", "rightArm", [-8.25, 24.5, -1.5], [3, 1, 3], lowres=("down", "north", "south", "east", "west"))
    skin.acc("puffL", "leftArm", [5.25, 24.5, -1.5], [3, 1, 3], like="puffR")
    h = add_footwear(skin, height=3.5, length=6.0, toe=1.5, tongue=False, width=4.75)
    paint_head(skin)
    paint_moons(skin)
    paint_body(skin)
    paint_arms(skin)
    paint_legs(skin, h)
    paint_boots(skin, BOOTS, 6900, straps=(1, 3))
    return skin


def bands(face, seed, scale=1.0):
    """Gas-giant belts, continuous across faces (they follow model height),
    with wavy turbulent edges."""
    y = face.Y + 0.35 * np.sin(face.X * 1.1 + face.Z * 0.9 + seed * 0.1) * scale
    idx = np.floor(y / 1.5).astype(int) % len(BANDS)
    pal = np.array(BANDS, float)
    face.rgba[..., :3] = pal[idx]
    face.rgba[..., 3] = 255
    face.shade(1 + 0.05 * np.sin(face.X * 2.3 + face.Y * 0.4 + face.Z * 1.7))
    face.shade(noise((face.h, face.w), seed, 0.02))


def paint_head(skin):
    for f in SIDES + ("up", "down"):
        bands(skin.face("head", f), 6000 + len(f))
    front = skin.face("head", "north")
    # the Great Red Spot: one huge swirling eye
    eye = [
        "..WWWWWWWW..",
        ".WWSSSSSSWW.",
        "WWSLLLSSSSWW",
        "WSLSPPPPSDSW",
        "WSSSPPPPSDSW",
        "WWSSSPPSSDWW",
        ".WWSDDDDSWW.",
        "..WWWWWWWW..",
    ]
    front.fill((120, 60, 40), box(front, 2, 2, 2, 13))       # heavy brow
    front.stamp(eye, {"W": WHITE, "S": SPOT, "L": SPOT_L, "D": SPOT_D, "P": PUPIL}, top=3, left=2)
    front.set(6, 7, (255, 240, 230))                        # glint
    front.set(6, 8, (255, 240, 230))
    # big friendly grin
    front.stamp([
        "M..........M",
        ".MMMMMMMMMM.",
        ".MWWWWWWWWM.",
        "..MMMMMMMM..",
    ], {"M": MOUTH, "W": WHITE}, top=11, left=2)
    for face in skin.each("hat"):
        face.clear()


def paint_moons(skin):
    for name, _, _ in MOONS:
        for face in skin.each(name):
            if name == "io":
                face.fill((240, 214, 90))
                rs = np.random.RandomState(6101 + face.w)
                face.fill((214, 120, 50), rs.rand(face.h, face.w) < 0.25)
                face.fill((250, 240, 170), rs.rand(face.h, face.w) < 0.15)
            elif name == "europa":
                face.fill((236, 230, 218))
                face.fill((176, 120, 84), (face.row + 2 * face.col) % 5 == 0)
            elif name == "ganymede":
                face.fill((150, 140, 128))
                face.fill((196, 188, 174), (face.row * 3 + face.col) % 4 == 0)
                face.fill((110, 100, 92), (face.row + face.col) % 5 == 2)
            else:
                face.fill((96, 82, 70))
                rs = np.random.RandomState(6102 + face.w)
                face.fill((220, 214, 204), rs.rand(face.h, face.w) < 0.12)
            face.shade(noise((face.h, face.w), 6110 + face.w, 0.04))
            # round it off: lit centre, darker rim
            d = np.maximum(abs(face.row - (face.h - 1) / 2), abs(face.col - (face.w - 1) / 2))
            face.shade(np.where(d >= (face.w - 1) / 2 - 0.01, 0.78, 1.08))


def storm_cloud(face, seed):
    """Dark thundercloud lumps lit from above."""
    t = np.clip(face.row / max(face.h - 1, 1) + 0.25 * np.sin(face.col * 1.4 + seed), 0, 1)
    gradient(face, [(0, CLOUD_L), (0.45, CLOUD), (1, CLOUD_D)], t=t)
    face.shade(noise((face.h, face.w), seed, 0.03))


def lightning(face, top, left, scale=1):
    bolt = [
        "..BB",
        ".BB.",
        "BBBB",
        "..BB",
        ".BB.",
        ".B..",
    ]
    face.stamp(bolt, {"B": BOLT}, top=top, left=left)


def paint_body(skin):
    for f in SIDES + ("up", "down"):
        bands(skin.face("body", f), 6200 + len(f))
    for face in skin.each("jacket"):
        face.clear()
    # open storm vest on the jacket layer
    for f in SIDES:
        face = skin.face("jacket", f)
        cloth(face, STORM, 6210 + len(f), var=0.04, fold=0.04)
        face.clear(face.row >= 19)
        rows(face, 18, 18, STORM_D)
    jk = skin.face("jacket", "north")
    jk.clear((jk.col >= 5) & (jk.col <= 10))
    jk.fill(STORM_H, (jk.col == 4) | (jk.col == 11))
    big_bolt = [
        "...BBB",
        "..BBL.",
        ".BBL..",
        "BBBBBB",
        "...BB.",
        "..BB..",
        ".BB...",
        ".B....",
    ]
    back = skin.face("jacket", "south")
    back.stamp(big_bolt, {"B": BOLT, "L": BOLT_L}, top=5, left=5)
    lightning(jk, 6, 0)
    # belt with a lightning buckle on the body
    for f in SIDES:
        face = skin.face("body", f)
        rows(face, 19, 20, STORM_D)
        rows(face, 21, 23, TROUSER)
    front = skin.face("body", "north")
    front.stamp(["BBBB", "BLLB", "BBBB"], {"B": BOLT_D, "L": BOLT}, top=18, left=6)
    skin.face("jacket", "up").clear()
    skin.face("jacket", "down").clear()


def paint_arms(skin):
    for face in skin.each("cloudR"):
        storm_cloud(face, 6300 + face.w + len(face.face))
    for f in SIDES:
        face = skin.face("cloudR", f)
        lightning(face, 1, face.w // 2 - 2)
        face.clear((face.row == face.h - 1) & (face.col % 3 == 0))
    for face in skin.each("puffR"):
        storm_cloud(face, 6310)
    for arm, slv, seed in (("rightArm", "rightSleeve", 6400), ("leftArm", "leftSleeve", 6410)):
        for f in SIDES + ("up", "down"):
            bands(skin.face(arm, f), seed + len(f))
        for face in skin.each(slv):
            face.clear()
        # storm-grey wrist bands with a gold stud
        for f in SIDES:
            face = skin.face(slv, f)
            rows(face, 15, 18, STORM)
            rows(face, 15, 15, STORM_H)
            rows(face, 18, 18, STORM_D)
            face.set(16, face.w // 2, BOLT)


def paint_legs(skin, boot_h):
    for leg, pants, outer, seed in (("rightLeg", "rightPants", "east", 6500), ("leftLeg", "leftPants", "west", 6510)):
        for f in SIDES:
            face = skin.face(leg, f)
            cloth(face, TROUSER, seed + len(f), var=0.05, fold=0.05)
            if f == outer:
                # zig-zag lightning stripe down the outside seam
                for r in range(face.h):
                    c = 3 + ((r // 3) % 2)
                    face.set(r, c, BOLT)
        skin.face(leg, "up").fill(TROUSER)
        skin.face(leg, "down").fill(TROUSER_D)
        for face in skin.each(pants):
            face.clear()
    clear_under_shoes(skin, boot_h)
