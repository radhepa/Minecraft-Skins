"""Render marketing/QA preview sheets.

    python3 tools/make_previews.py solar_system                # every skin + lineup
    python3 tools/make_previews.py solar_system sol saturn ... # just these skins

Needs `npm install` in tools/render and Playwright's Chromium.
Outputs go to previews/<pack>/<skin>/.
"""

import json
import os
import subprocess
import sys
import tempfile

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

from build_pack import load_skin  # noqa: E402
from packs import PACKS  # noqa: E402

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
STYLE = dict(PACKS["midnight_mischief"]["style"])  # set per pack in main()


def font(size):
    try:
        return ImageFont.truetype(FONT, size)
    except OSError:
        return ImageFont.load_default()


def backdrop(w, h):
    yy, xx = np.mgrid[0:h, 0:w]
    d = np.sqrt(((xx - w / 2) / (w * 0.7)) ** 2 + ((yy - h * 0.45) / (h * 0.7)) ** 2)
    t = np.clip(d, 0, 1)[..., None]
    bg_in, bg_out = STYLE["bg"]
    img = np.array(bg_in) * (1 - t) + np.array(bg_out) * t
    return Image.fromarray(img.astype(np.uint8), "RGB").convert("RGBA")


def crop_alpha(im, pad=20):
    box = im.getbbox()
    if not box:
        return im
    x0, y0, x1, y1 = box
    return im.crop((max(x0 - pad, 0), max(y0 - pad, 0),
                    min(x1 + pad, im.width), min(y1 + pad, im.height)))


def fit(im, w, h):
    s = min(w / im.width, h / im.height)
    return im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), Image.LANCZOS)


def sheet(cells, labels, title, cell=(520, 700), cols=None):
    cols = cols or len(cells)
    rows = (len(cells) + cols - 1) // cols
    head = 90
    W, H = cell[0] * cols, cell[1] * rows + head
    out = backdrop(W, H)
    d = ImageDraw.Draw(out)
    size = 40
    while size > 18 and d.textlength(title, font=font(size)) > W - 40:
        size -= 2
    d.text((W // 2, 46), title, fill=STYLE["title"], font=font(size), anchor="mm")
    for i, (im, lab) in enumerate(zip(cells, labels)):
        cx, cy = (i % cols) * cell[0], head + (i // cols) * cell[1]
        im = fit(crop_alpha(im), cell[0] - 40, cell[1] - 80)
        out.alpha_composite(im, (cx + (cell[0] - im.width) // 2, cy + (cell[1] - 60 - im.height) // 2))
        d.text((cx + cell[0] // 2, cy + cell[1] - 34), lab, fill=STYLE["label"], font=font(26), anchor="mm")
    return out.convert("RGB")


def render(geometry, identifier, texture, shots, outdir):
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as fh:
        json.dump(shots, fh)
    subprocess.run(["node", os.path.join(HERE, "render", "render.mjs"), identifier,
                    texture, outdir, fh.name, geometry], check=True, stdout=subprocess.DEVNULL)
    os.unlink(fh.name)
    return {s["name"]: Image.open(os.path.join(outdir, s["name"] + ".png")).convert("RGBA")
            for s in shots}


def texture_sheet(texture, title):
    tex = Image.open(texture).convert("RGBA")
    scale = 6
    n = tex.width
    yy, xx = np.mgrid[0:n * scale, 0:n * scale]
    chk = ((xx // 12 + yy // 12) % 2)[..., None]
    bg = np.where(chk, [64, 60, 72, 255], [44, 40, 52, 255]).astype(np.uint8)
    big = tex.resize((n * scale, n * scale), Image.NEAREST)
    canvas = Image.fromarray(bg, "RGBA")
    canvas.alpha_composite(big)
    out = backdrop(canvas.width + 80, canvas.height + 130)
    out.alpha_composite(canvas, (40, 90))
    d = ImageDraw.Draw(out)
    d.text((out.width // 2, 46), title, fill=STYLE["title"], font=font(36), anchor="mm")
    return out.convert("RGB")


VIEW = {"dist": 110, "target": 18}


def skin_previews(pack, name):
    cfg = PACKS[pack]
    mod = load_skin(pack, name)
    texture = os.path.join(ROOT, cfg["dir"], mod.TEXTURE)
    geometry = os.path.join(ROOT, cfg["dir"], "geometry.json")
    out = os.path.join(ROOT, "previews", pack, name)
    os.makedirs(out, exist_ok=True)
    raw = os.path.join(tempfile.gettempdir(), "skin_shots_" + name)

    shots = [
        {"name": "hero", "yaw": 26, "pitch": 7},
        {"name": "front", "yaw": 0, "pitch": 3},
        {"name": "right", "yaw": 90, "pitch": 3},
        {"name": "back", "yaw": 180, "pitch": 3},
        {"name": "left", "yaw": 270, "pitch": 3},
        {"name": "back34", "yaw": 215, "pitch": 12},
        {"name": "walk", "yaw": -32, "pitch": 6, "poseName": "walk"},
        {"name": "wave", "yaw": 20, "pitch": 6, "poseName": "wave"},
    ]
    shots = [dict(VIEW, **s) for s in shots]
    details = [dict(VIEW, name="detail_" + key, **cam) for key, _, cam in mod.DETAILS]
    spin = [dict(VIEW, name=f"spin{i:02d}", yaw=i * 15, pitch=8) for i in range(24)]
    ims = render(geometry, mod.ID, texture, shots + details + spin, raw)

    title = f"{cfg['name']} - {mod.NAME}"
    sheet([ims[k] for k in ("front", "right", "back", "left")],
          ["Front", "Right", "Back", "Left"], title + " - Turnaround").save(
        os.path.join(out, "turnaround.png"))
    sheet([ims[k] for k in ("hero", "walk", "wave", "back34")],
          ["Idle", "Walking", "Waving", "Back 3/4"], title + " - In-game poses").save(
        os.path.join(out, "poses.png"))
    sheet([ims["detail_" + key] for key, _, _ in mod.DETAILS],
          [label for _, label, _ in mod.DETAILS],
          title + " - 3D details", cell=(620, 640)).save(os.path.join(out, "details.png"))
    texture_sheet(texture, f"{mod.TEXTURE} (128x128 HD)").save(os.path.join(out, "texture.png"))

    hero = backdrop(900, 1200)
    hero.alpha_composite(ims["hero"])
    hero.convert("RGB").save(os.path.join(out, "hero.png"))

    ref_box = getattr(mod, "REF_BOX", None)
    if ref_box:
        ref = Image.open(os.path.join(ROOT, cfg["reference"]))
        ref = ref.convert("RGBA").crop(ref_box)
        sheet([ref, ims["hero"]], ["Reference art", "Built skin (render)"],
              title + " - Reference vs build", cell=(640, 860)).save(
            os.path.join(out, "vs_reference.png"))

    frames = []
    for i in range(24):
        f = backdrop(450, 600)
        f.alpha_composite(ims[f"spin{i:02d}"].resize((450, 600), Image.LANCZOS))
        frames.append(f.convert("RGB").convert("P", palette=Image.ADAPTIVE, colors=255))
    frames[0].save(os.path.join(out, "turntable.gif"), save_all=True,
                   append_images=frames[1:], duration=110, loop=0)
    print("previews written to", out)
    return mod, ims["hero"]


def lineup(pack, entries, cols=6):
    """Pack key art: every skin's hero render in a grid with its name."""
    cw, ch = 400, 600
    rows_n = (len(entries) + cols - 1) // cols
    W, H = cw * cols, ch * rows_n + 150
    out = backdrop(W, H)
    d = ImageDraw.Draw(out)
    d.text((W // 2, 75), PACKS[pack]["name"].upper(), fill=STYLE["title"], font=font(72), anchor="mm")
    for i, (mod, im) in enumerate(entries):
        cx, cy = (i % cols) * cw, 150 + (i // cols) * ch
        im = fit(crop_alpha(im), cw - 40, ch - 90)
        out.alpha_composite(im, (cx + (cw - im.width) // 2, cy + (ch - 60 - im.height) // 2))
        d.text((cx + cw // 2, cy + ch - 36), mod.NAME, fill=STYLE["label"], font=font(28), anchor="mm")
    out.convert("RGB").save(os.path.join(ROOT, "previews", pack, "lineup.png"))


def main():
    if not sys.argv[1:] or sys.argv[1] not in PACKS:
        sys.exit("usage: make_previews.py <pack> [skin ...]   packs: " + ", ".join(PACKS))
    pack, names = sys.argv[1], sys.argv[2:]
    STYLE.update(PACKS[pack]["style"])
    entries = [skin_previews(pack, n) for n in names or PACKS[pack]["skins"]]
    if not names:
        n = len(entries)
        lineup(pack, entries, cols=5 if n > 6 and n % 5 == 0 else min(6, n))
        print(f"lineup written to previews/{pack}/lineup.png")


if __name__ == "__main__":
    main()
