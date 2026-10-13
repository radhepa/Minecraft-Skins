"""Reusable painting recipes shared by every skin pack."""

import numpy as np

from skinlib import noise

SIDES = ("north", "south", "east", "west")


def cloth(face, base, seed, var=0.09, fold=0.06, freq=1.3, mask=None):
    """Fabric: base colour, per-texel value noise and soft horizontal folds."""
    old = face.rgba.copy()
    face.fill(base)
    face.shade(noise((face.h, face.w), seed, var))
    face.shade(1 + fold * np.sin(face.row * freq + face.col * 0.35 + seed))
    if mask is not None:
        face.rgba = np.where(mask[..., None], face.rgba, old)


def hair(face, base, dark, light, seed, mask=None, vertical=True, shine=None):
    """Clumped, gently wavy strands: lanes 1-3 texels wide in dark/base/light,
    a soft wave running down each lane, and optional shine highlights."""
    old = face.rgba.copy()
    rs = np.random.RandomState(seed)
    n = face.w if vertical else face.h
    lane_of, tone, phase = np.zeros(n, int), [], []
    i = 0
    while i < n:
        w = rs.choice([1, 2, 2, 3])
        lane_of[i:i + w] = len(tone)
        tone.append(rs.choice([0, 1, 1, 2]) if not tone or tone[-1] != 0 else rs.choice([1, 2]))
        phase.append(rs.rand() * 6.28)
        i += w
    tone, phase = np.array(tone), np.array(phase)
    along = face.row if vertical else face.col
    lane = lane_of[face.col] if vertical else lane_of[face.row]
    pal = np.array([dark, base, light], float)
    face.rgba[..., :3] = pal[tone[lane]]
    face.rgba[..., 3] = 255
    wave = np.sin(along * 0.85 + phase[lane])
    face.shade(1 + 0.1 * wave)
    if shine is not None:
        face.fill(shine, (wave > 0.92) & (tone[lane] == 2))
    face.shade(noise((face.h, face.w), seed + 1, 0.025))
    if mask is not None:
        face.rgba = np.where(mask[..., None], face.rgba, old)


def skin_tone(face, base, seed, var=0.03):
    face.fill(base)
    face.shade(noise((face.h, face.w), seed, var))


def rows(face, r0, r1, color, mask=None):
    m = (face.row >= r0) & (face.row <= r1)
    if mask is not None:
        m &= mask
    face.fill(color, m)


def box(face, r0, c0, r1, c1):
    return (face.row >= r0) & (face.row <= r1) & (face.col >= c0) & (face.col <= c1)


def copy_layer(skin, src, dst):
    for f in SIDES + ("up", "down"):
        if (src, f) in skin.faces and (dst, f) in skin.faces:
            skin.face(dst, f).rgba = skin.face(src, f).rgba.copy()


def sides(skin, name):
    return [skin.face(name, f) for f in SIDES]


# ------------------------------------------------------------- footwear
def add_footwear(skin, height=3.0, length=6.0, toe=1.5, tongue=True, width=4.5):
    """Chunky 3D shoes/boots on both leg bones (+ optional raised tongues)."""
    z0 = -2 - toe
    for side, x0 in (("right", -width), ("left", 0.0)):
        skin.acc(f"{side}Shoe", f"{side}Leg", [x0, 0, z0], [width, height, length],
                 lowres=("up", "down"))
        if tongue:
            cx = -2.25 if side == "right" else 2.25
            skin.acc(f"{side}Tongue", f"{side}Leg", [cx - 1, height, -3.25], [2, 1, 1])
    return height


def paint_sneakers(skin, pal, seed, pal_left=None, stripe=True):
    """pal keys: upper, hi, dark, lace, lace_dark, sole, sole_dark."""
    for side in ("right", "left"):
        p = pal if side == "right" or pal_left is None else pal_left
        shoe = f"{side}Shoe"
        outer = "east" if side == "right" else "west"
        for f in SIDES:
            face = skin.face(shoe, f)
            h = face.h
            face.fill(p["upper"])
            face.shade(noise((h, face.w), seed + len(f), 0.06))
            rows(face, 0, 0, p["hi"])
            rows(face, h - 3, h - 3, p["dark"])
            rows(face, h - 2, h - 2, p["sole"])
            rows(face, h - 1, h - 1, p["sole_dark"])
        toe = skin.face(shoe, "north")
        rows(toe, 1, 1, p["lace"], (toe.col >= 2) & (toe.col <= toe.w - 3))
        for f in ("east", "west"):
            face = skin.face(shoe, f)
            heel_first = f == "east"
            for c in range(face.w):
                k = c if heel_first else face.w - 1 - c
                if stripe and 3 <= k <= face.w - 4:
                    face.set(face.h - 4, c, p["lace"] if f == outer else p["lace_dark"])
                if k <= 1:
                    for r in range(0, face.h - 3):
                        face.set(r, c, p["dark"])
        heel = skin.face(shoe, "south")
        heel.fill(p["dark"], (heel.col >= 3) & (heel.col <= heel.w - 4) & (heel.row <= heel.h - 4))
        heel.set(0, heel.w // 2, p["lace"])
        top = skin.face(shoe, "up")
        top.fill(p["upper"])
        top.shade(noise((top.h, top.w), seed + 9, 0.06))
        top.fill(p["hi"], (top.col == 0) | (top.col == top.w - 1))
        for f in ("north", "up"):
            face = skin.face(shoe, f)
            face.shade(np.where(face.col == (face.w - 1 if side == "right" else 0), 0.72, 1.0))
        sole = skin.face(shoe, "down")
        sole.fill(p["sole_dark"])
        sole.fill(p["sole"], (sole.row + sole.col) % 3 == 0)
        tongue = f"{side}Tongue"
        if (tongue, "north") in skin.faces:
            for f in SIDES:
                skin.face(tongue, f).fill(p["dark"] if f != "north" else p["upper"])
            t_front = skin.face(tongue, "north")
            rows(t_front, 1, 1, p["lace"])
            t_front.set(1, 3, p["lace_dark"])
            skin.face(tongue, "up").fill(p["hi"])
            skin.face(tongue, "down").fill(p["dark"])


def paint_boots(skin, pal, seed, straps=(2, 5)):
    """Taller boots: pal keys upper, hi, dark, strap, strap_dark, sole, sole_dark."""
    for side in ("right", "left"):
        shoe = f"{side}Shoe"
        for f in SIDES:
            face = skin.face(shoe, f)
            h = face.h
            face.fill(pal["upper"])
            face.shade(noise((h, face.w), seed + len(f), 0.08))
            rows(face, 0, 0, pal["hi"])
            rows(face, h - 3, h - 3, pal["dark"])
            rows(face, h - 2, h - 1, pal["sole"])
            rows(face, h - 1, h - 1, pal["sole_dark"])
            for r in straps:
                if f == "north":
                    rows(face, r, r, pal["strap"], (face.col >= 1) & (face.col <= face.w - 2))
                    face.set(r, face.w // 2, pal["strap_dark"])
                elif f in ("east", "west"):
                    front = face.col >= face.w // 2 if f == "east" else face.col < face.w // 2
                    rows(face, r, r, pal["strap"], front)
        top = skin.face(shoe, "up")
        top.fill(pal["upper"])
        top.shade(noise((top.h, top.w), seed + 9, 0.08))
        top.fill(pal["hi"], (top.col == 0) | (top.col == top.w - 1) | (top.row == top.h - 1))
        sole = skin.face(shoe, "down")
        sole.fill(pal["sole_dark"])
        for f in ("north", "up"):
            face = skin.face(shoe, f)
            face.shade(np.where(face.col == (face.w - 1 if side == "right" else 0), 0.72, 1.0))


def clear_under_shoes(skin, height, layers=("rightPants", "leftPants")):
    """Overlay texels hidden inside the shoes would poke out; drop them."""
    cut = 24 - int(round(height * 2))
    for name in layers:
        for face in sides(skin, name):
            face.clear(face.row >= cut)
        skin.face(name, "down").clear()


def eye_glow(face, cells, core, mid, rim):
    """cells: list of (r, c); brightest in the middle, rim on the edge."""
    s = set(cells)
    for r, c in cells:
        n = sum((r + dr, c + dc) in s for dr in (-1, 0, 1) for dc in (-1, 0, 1))
        face.set(r, c, core if n >= 9 else (mid if n >= 6 else rim))


# ------------------------------------------------------------- space
def gradient(face, stops, t=None, mask=None):
    """Blend through colour stops [(pos 0..1, rgb), ...] along t (default:
    top row 0 -> bottom row 1)."""
    if t is None:
        t = face.row / max(face.h - 1, 1)
    pos = np.array([p for p, _ in stops], float)
    cols = np.array([c for _, c in stops], float)
    out = np.stack([np.interp(t, pos, cols[:, k]) for k in range(3)], -1)
    m = np.ones((face.h, face.w), bool) if mask is None else mask
    face.rgba[m, :3] = out[m]
    face.rgba[m, 3] = 255


def cells(face, seed, size=3.0):
    """Cellular pattern (like the sun's granulation). Returns (centre, edge):
    0 at a cell's centre rising to 1 at its rim, and a True mask on the thin
    lanes between cells."""
    rs = np.random.RandomState(seed)
    n = max(4, int(face.w * face.h / (size * size)))
    py, px = rs.rand(n) * (face.h + 2) - 1, rs.rand(n) * (face.w + 2) - 1
    d = np.sqrt((face.row[..., None] - py) ** 2 + (face.col[..., None] - px) ** 2)
    d.sort(-1)
    d1, d2 = d[..., 0], d[..., 1]
    return np.clip(d1 / (size * 0.75), 0, 1), (d2 - d1) < 0.9


def starfield(face, seed, density=0.04, colors=((255, 255, 255),), mask=None, twinkle=True):
    """Scatter single-texel stars, with the odd 4-point twinkle."""
    rs = np.random.RandomState(seed)
    hit = rs.rand(face.h, face.w) < density
    if mask is not None:
        hit &= mask
    for r, c in zip(*np.nonzero(hit)):
        col = colors[rs.randint(len(colors))]
        face.set(r, c, col)
        if twinkle and rs.rand() < 0.12:
            dim = tuple(int(v * 0.7) for v in col)
            for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                rr, cc = r + dr, c + dc
                if mask is None or (0 <= rr < face.h and 0 <= cc < face.w and mask[rr, cc]):
                    face.set(rr, cc, dim)


def flame_edge(face, seed, base_row, height=4, period=(3, 6), from_top=True):
    """Row index per column for a licking-flame silhouette: tongues rise
    `height` texels above base_row. Texels past the edge are what to clear."""
    rs = np.random.RandomState(seed)
    edge = np.zeros(face.w)
    c = 0
    while c < face.w:
        w = rs.randint(period[0], period[1] + 1)
        tip = rs.uniform(0.45, 1.0) * height
        xs = np.arange(w)
        edge[c:c + w] = (tip * np.sin(np.pi * (xs + 0.5) / w) ** 1.6)[:face.w - c]
        c += w
    edge = np.round(edge).astype(int)
    return base_row - edge if from_top else base_row + edge
