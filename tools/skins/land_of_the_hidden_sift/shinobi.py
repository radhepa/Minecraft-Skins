"""Pieces the Land of the Hidden Sift skins share: the village headband (a
navy cloth band with a wide 3D steel plate, riveted at the corners and
engraved with the village crest, a glowing rift inside a diamond, plus a
knot and two long trailing tails; rogue ninja wear theirs slashed through), open-toed shinobi sandals, bandage wraps, a
thigh holster, anime eyes and helpers for rotated accessories.
"""

import numpy as np

from paintkit import SIDES, add_footwear, gradient, rows
from skinlib import noise

BAND = (38, 50, 98)
BAND_D = (24, 32, 66)
BAND_L = (64, 80, 136)
STEEL_L = (244, 247, 252)
STEEL = (196, 204, 218)
STEEL_D = (130, 140, 160)
ETCH = (64, 70, 90)
RIFT = (90, 236, 222)
RIFT_C = (210, 255, 250)
SLASH = (40, 40, 50)
WRAP = (238, 234, 222)
WRAP_D = (200, 194, 180)
POUCH = (46, 50, 64)
POUCH_D = (30, 32, 44)
POUCH_L = (78, 84, 104)

# the village crest: a diamond split by a glowing rift, with short etched
# lines running out from its sides
PLATE_W, PLATE_H, PLATE_PX = 7, 3, 3


def _line(a, b):
    (r0, c0), (r1, c1) = a, b
    n = max(abs(r1 - r0), abs(c1 - c0))
    return {(round(r0 + (r1 - r0) * k / n), round(c0 + (c1 - c0) * k / n)) for k in range(n + 1)}


DIAMOND = (_line((1, 10), (4, 5)) | _line((4, 5), (7, 10)) | _line((7, 10), (4, 15))
           | _line((4, 15), (1, 10)) | {(4, c) for c in (2, 3, 17, 18)})
RIFT_CELLS = {(2, 10), (3, 10), (3, 9), (4, 9), (4, 10), (5, 10), (5, 11), (6, 10)}


EMBLEM = DIAMOND


def band_mask(face, yc, half, slope):
    """Texels of a face inside the headband. The band is a plane-cut strip
    round the head: its centre height is yc - slope * x."""
    return np.abs(face.Y - (yc - slope * face.X)) <= half


def add_headband(skin, yc=30.0, tilt=0.0, plate_x=0.0, tail_x=0.9):
    """Plate, knot and tails. `tilt` (degrees) drops the band towards the
    character's left (+x); `plate_x` slides the plate along it."""
    slope = np.tan(np.radians(tilt))
    py = yc - slope * plate_x
    kw = {}
    if tilt:
        kw = dict(rotation=[0, 0, tilt], pivot=[plate_x, py, -4.7])
    skin.acc("plate", "head", [plate_x - PLATE_W / 2, py - PLATE_H / 2, -4.85],
             [PLATE_W, PLATE_H, 0.35], faces=("north", "east", "west", "up", "down"),
             px=PLATE_PX, first=True, **kw)
    by = yc
    skin.acc("knot", "head", [-0.75, by - 0.75, 4.45], [1.5, 1.5, 0.6], lowres=("up", "down", "east", "west"))
    for side, x, lean in (("R", -tail_x, -10), ("L", tail_x, 12)):
        kw = dict(pivot=[x, by, 4.9], rotation=[22, 0, lean])
        origin = [x - 0.75, by - 6.5, 4.8]
        if side == "R":
            skin.acc("tailR", "head", origin, [1.5, 6.5, 0.25], faces=("north", "south"),
                     pad=("north", "south"), **kw)
        else:
            skin.acc("tailL", "head", origin, [1.5, 6.5, 0.25], like="tailR", **kw)
    skin.band = (yc, slope)


def paint_headband(skin, half=1.15, cloth=(BAND, BAND_D, BAND_L), slashed=False):
    """Band cloth on the hat layer (call after the hair is painted), then the
    plate, knot and tails. A rogue ninja's plate is `slashed` through."""
    BAND, BAND_D, BAND_L = cloth
    yc, slope = skin.band
    for f in SIDES:
        face = skin.face("hat", f)
        m = band_mask(face, yc, half, slope)
        d = np.abs(face.Y - (yc - slope * face.X))
        face.fill(BAND, m)
        face.shade(noise((face.h, face.w), 9000 + len(f), 0.05), m)
        face.fill(BAND_L, m & (d > half - 0.5) & (face.Y > yc - slope * face.X))
        face.fill(BAND_D, m & (d > half - 0.5) & (face.Y < yc - slope * face.X))
    _paint_plate(skin, slashed)
    for face in skin.each("knot"):
        face.fill(BAND)
        face.shade(noise((face.h, face.w), 9010 + face.w, 0.06))
    knot = skin.face("knot", "south")
    knot.fill(BAND_D, (knot.col == 0) | (knot.row == knot.h - 1))
    for f in ("north", "south"):
        face = skin.face("tailR", f)
        face.fill(BAND)
        face.shade(noise((face.h, face.w), 9020 + len(f), 0.05))
        face.fill(BAND_L, face.col == 0)
        face.fill(BAND_D, face.col == face.w - 1)
        face.shade(np.where(face.row % 5 == 4, 0.88, 1.0))
        # cut, slightly frayed ends
        face.clear((face.row == face.h - 1) & (face.col != 1))


def _paint_plate(skin, slashed):
    plate = skin.face("plate", "north")
    gradient(plate, [(0, STEEL_L), (0.4, STEEL), (1, STEEL_D)])
    plate.shade(1 + 0.05 * np.sin(plate.col * 0.7 - plate.row * 1.2))
    edge = (plate.row == 0) | (plate.row == plate.h - 1) | (plate.col == 0) | (plate.col == plate.w - 1)
    plate.fill(STEEL_D, edge)
    plate.fill(STEEL_L, (plate.row == 0) & ~((plate.col == 0) | (plate.col == plate.w - 1)))
    # two rivets at each end
    for r in (2, plate.h - 3):
        for c in (1, plate.w - 2):
            plate.set(r, c, ETCH)
            plate.set(r - 1, c, STEEL_L)
    for r, c in EMBLEM:
        plate.set(r, c, ETCH)
    for r, c in RIFT_CELLS:
        plate.set(r, c, RIFT_C if c == 7 and r in (3, 5) else RIFT)
    if slashed:
        # one deep scratch straight across the crest
        mid = plate.h // 2
        plate.fill(SLASH, (plate.row == mid) & (plate.col >= 1) & (plate.col <= plate.w - 2))
        plate.fill(STEEL_L, (plate.row == mid + 1) & (plate.col >= 2) & (plate.col <= plate.w - 3))
    for f in ("east", "west", "up", "down"):
        skin.face("plate", f).fill(STEEL_D)
    skin.face("plate", "up").fill(STEEL)


def wraps(face, r0, r1, mask=None):
    """Bandage wrapped round a limb between rows r0..r1."""
    m = (face.row >= r0) & (face.row <= r1)
    if mask is not None:
        m &= mask
    face.fill(WRAP, m)
    face.fill(WRAP_D, m & ((face.row + face.col // 2) % 3 == 0))
    face.shade(noise((face.h, face.w), 9100 + face.w + r0, 0.04), m)


def add_sandals(skin):
    return add_footwear(skin, height=2.0, length=5.5, toe=1.0, tongue=False, width=4.5)


def paint_sandals(skin, colour, dark, skin_col, skin_dark):
    for side in ("right", "left"):
        shoe = f"{side}Shoe"
        for f in SIDES:
            face = skin.face(shoe, f)
            face.fill(colour)
            face.shade(noise((face.h, face.w), 9200 + len(f), 0.06))
            rows(face, 0, 0, tuple(min(255, int(v * 1.25)) for v in colour))
            toes = (face.Z < -1.6) & (face.Y >= 0.5)
            face.fill(skin_col, toes)
            if f == "north":
                face.fill(skin_dark, toes & (face.col % 2 == 1) & (face.row >= 1))
            face.fill(dark, face.Y < 0.5)
            # strap across the top of the foot
            face.fill(dark, (face.Z >= -1.6) & (face.Z < -1.0) & (face.Y >= 0.5))
        up = skin.face(shoe, "up")
        up.fill(colour)
        up.fill(skin_col, up.Z < -1.6)
        skin.face(shoe, "down").fill(dark)


def add_holster(skin, side="right"):
    x = -4.9 if side == "right" else 4.15
    bone = f"{side}Leg"
    skin.acc("holster", bone, [x, 5.0, -1.5], [0.75, 3.5, 3], lowres=("up", "down", "north", "south"))


def paint_holster(skin, side="right", strap=POUCH_D):
    out = "east" if side == "right" else "west"
    for face in skin.each("holster"):
        face.fill(POUCH)
        face.shade(noise((face.h, face.w), 9300 + face.w, 0.05))
    face = skin.face("holster", out)
    rows(face, 0, 2, POUCH_L)
    rows(face, 2, 2, POUCH_D)
    face.set(2, face.w // 2, STEEL)
    face.fill(POUCH_D, (face.col == 0) | (face.col == face.w - 1))
    # bandage under the holster and its two straps round the thigh
    pants = f"{side}Pants"
    for f in SIDES:
        p = skin.face(pants, f)
        wraps(p, 6, 13)
        rows(p, 7, 7, strap)
        rows(p, 12, 12, strap)


# (suffix, width, thickness, share of the length) for each stacked tier
def rot_matrix(rot):
    """The matrix a Bedrock cube rotation [rx, ry, rz] (degrees) applies in
    model space, matching Blockbench and the game."""
    rx, ry, rz = np.radians(rot)
    c, s = np.cos, np.sin
    Rx = np.array([[1, 0, 0], [0, c(-rx), -s(-rx)], [0, s(-rx), c(-rx)]])
    Ry = np.array([[c(ry), 0, s(ry)], [0, 1, 0], [-s(ry), 0, c(ry)]])
    Rz = np.array([[c(-rz), -s(-rz), 0], [s(-rz), c(-rz), 0], [0, 0, 1]])
    return Rz @ Ry @ Rx


def aim(d):
    """Rotation [rx, 0, rz] that turns a cube's +y axis to point along d."""
    d = np.asarray(d, float) / np.linalg.norm(d)
    return [round(float(-np.degrees(np.arcsin(d[2]))), 2), 0,
            round(float(np.degrees(np.arctan2(d[0], d[1]))), 2)]


def frame_rot(x_axis, y_axis):
    """Rotation [rx, ry, rz] that turns a cube's +y axis along y_axis and
    its +x axis as close to x_axis as possible."""
    y = np.asarray(y_axis, float)
    y /= np.linalg.norm(y)
    x = np.asarray(x_axis, float)
    x = x - y * (x @ y)
    x /= np.linalg.norm(x)
    z = np.cross(x, y)
    M = np.stack([x, y, z], axis=1)
    b = -np.arcsin(np.clip(M[2, 0], -1, 1))
    if abs(M[2, 0]) > 0.9999:      # gimbal lock: fold the z turn into x
        a = 0.0
        c = np.arctan2(np.sign(np.sin(b)) * M[0, 1], M[1, 1])
    else:
        c = np.arctan2(M[2, 1], M[2, 2])
        a = np.arctan2(M[1, 0], M[0, 0])
    return [round(float(-np.degrees(c)), 2), round(float(np.degrees(b)), 2),
            round(float(-np.degrees(a)), 2)]


def anime_eyes(front, top, art, pal, lefts=(2, 9)):
    """Stamp an anime eye drawn for the character's right eye (outer corner
    on the left) and its mirror image for the left eye."""
    front.stamp(art, pal, top=top, left=lefts[0])
    front.stamp(art, pal, top=top, left=lefts[1], mirror=True)


# Faces follow the usual Minecraft skin look: no mouth or nose, just eyes.
# Palette keys: L lash, W white, D dark iris, E iris, H light iris,
# G catch-light. Each is drawn for the character's right eye (outer corner
# on the left) and mirrored for the left.
#
# EYE_SOFT: a heavy two-row lash bar that flicks out at the corner, over a
# white and a softly shaded iris (girls).
EYE_SOFT = [
    ".LLLL",
    "LLLLL",
    "LWWGD",
    ".WWEH",
]
# EYE_SHARP: a thinner lash over a narrower eye, worn under a thick brow
# (boys and men); the brow is painted separately with brows().
EYE_SHARP = [
    "LLLL",
    "WWGD",
    "WWEH",
]


def brows(front, row, colour, lefts=(2, 10), width=4, slant=False):
    """Thick straight brows; `slant` drops the inner ends a texel (a frown)."""
    for left in lefts:
        for c in range(left, left + width):
            front.set(row, c, colour)
    if slant:
        front.set(row + 1, lefts[0] + width - 1, colour)
        front.set(row + 1, lefts[1], colour)


def add_neckband(skin, y=21.25):
    """The headband worn round the neck instead: the plate sits on the
    upper chest and the cloth goes on the jacket layer."""
    skin.acc("plate", "body", [-PLATE_W / 2, y, -2.6], [PLATE_W, PLATE_H, 0.35],
             faces=("north", "east", "west", "up", "down"), px=PLATE_PX, first=True)
    skin.neckband = y


def paint_neckband(skin, cloth=(BAND, BAND_D, BAND_L), slashed=False):
    band, dark, light = cloth
    r1 = int(round((24 - skin.neckband) * 2))
    for f in SIDES:
        face = skin.face("jacket", f)
        rows(face, 0, r1 - 1, band)
        rows(face, 0, 0, light)
        rows(face, r1 - 1, r1 - 1, dark)
    _paint_plate(skin, slashed)


# ------------------------------------------------------------- faces + hair
def male_face(front, brow, eye_pal, mouth, eyes_top=8, mouth_row=13, slant=False,
              mouth_cols=(7, 9)):
    """Thick brows, EYE_SHARP eyes and a short straight mouth."""
    brows(front, eyes_top - 1, brow, slant=slant)
    anime_eyes(front, eyes_top, EYE_SHARP, eye_pal, lefts=(2, 10))
    rows(front, mouth_row, mouth_row, mouth, (front.col >= mouth_cols[0]) & (front.col <= mouth_cols[1]))


def female_face(front, eye_pal, mouth, blush=None, eyes_top=8, mouth_row=13):
    """EYE_SOFT eyes, a touch of blush and a tiny two-texel mouth."""
    anime_eyes(front, eyes_top, EYE_SOFT, eye_pal)
    if blush is not None:
        for c in (1, 2, 13, 14):
            front.set(eyes_top + 4, c, blush)
    front.set(mouth_row, 7, mouth)
    front.set(mouth_row, 8, mouth)


def hair_head(skin, painter, seed, skin_col, skin_dark, fringe, back_bottom=11,
              long_sides=False, hat_sides=True):
    """Skin and hair on the head, then a hat-layer hair shell: `fringe` gives,
    per front column, the last hat row the fringe reaches. Short hair shows
    the ear; `long_sides` keeps hair over it."""
    from paintkit import skin_tone
    front = skin.face("head", "north")
    skin_tone(front, skin_col, seed, var=0.012)
    painter(front, seed + 1, front.row <= 6)
    for f in ("east", "west", "south", "up"):
        face = skin.face("head", f)
        skin_tone(face, skin_col, seed + 10 + len(f))
        if f in ("south", "up"):
            painter(face, seed + 20 + len(f), None)
        elif long_sides:
            painter(face, seed + 30 + len(f), (face.Z > -2.5) | (face.row <= 6))
        else:
            ear = (face.row >= 8) & (face.row <= 11) & (np.abs(face.Z + 0.5) <= 1.5)
            painter(face, seed + 30 + len(f), (((face.Z > -1) & (face.row <= back_bottom)) | (face.row <= 6)) & ~ear)
            face.fill(skin_dark, ear & (np.abs(face.Z + 0.5) <= 0.6) & (face.row >= 9) & (face.row <= 10))
    if not long_sides:
        back = skin.face("head", "south")
        back.fill(skin_col, back.row > back_bottom + 1)
    skin_tone(skin.face("head", "down"), skin_dark, seed + 40)
    for face in skin.each("hat"):
        face.clear()
    painter(skin.face("hat", "up"), seed + 50, None)
    hf = skin.face("hat", "north")
    painter(hf, seed + 51, None)
    hf.clear(hf.row > np.array(fringe)[hf.col])
    for f in ("east", "west", "south"):
        face = skin.face("hat", f)
        if not hat_sides and f != "south":
            painter(face, seed + 52 + len(f), face.row <= 6)
            continue
        painter(face, seed + 52 + len(f), None)
        bottom = (back_bottom + 2 if long_sides else back_bottom) + (face.col % 4 == 1)
        face.clear(face.row > bottom)
        if f != "south":
            if long_sides:
                face.clear((face.Z < -1.5) & (face.Z > -4.0) & (face.row > 4))
            else:
                face.clear((face.Z < -1.0) & (face.Z > -3.8) & (face.row > 5))


def hair_painter(base, dark, light, shine=None):
    from paintkit import hair

    def paint(face, seed, mask):
        hair(face, base, dark, light, seed, mask=mask, shine=shine)
    return paint
