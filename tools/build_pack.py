"""Build the Midnight Mischief skin pack from the skin scripts in tools/skins.

    python3 tools/build_pack.py

Writes textures, geometry.json, skins.json, manifest.json and texts/ into
MidnightMischief/.
"""

import importlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "skins"))

from skinlib import write_geometry  # noqa: E402

PACK_DIR = os.path.join(os.path.dirname(HERE), "MidnightMischief")
PACK_KEY = "MidnightMischief"
PACK_NAME = "Midnight Mischief"
HEADER_UUID = "f89add21-039f-463f-8e28-3761edc22e6e"
MODULE_UUID = "57655c99-c40a-46b7-99b5-f1cfdbc2343b"
VERSION = [1, 0, 0]

# Order here is the order skins appear in the in-game picker.
SKINS = ["pumpkin_prankster", "moonlight_witch", "boo_hoodie", "velvet_vampire", "frankie_stitches", "midnight_kitty", "candy_corn_cutie", "bone_chiller", "scarecrow_sam", "lunar_howler", "mummy_wraps", "batty_belle"]


def main():
    os.makedirs(os.path.join(PACK_DIR, "texts"), exist_ok=True)
    geometries, entries, lang = [], [], [f"skinpack.{PACK_KEY}={PACK_NAME}"]
    for module_name in SKINS:
        mod = importlib.import_module(module_name)
        skin = mod.build()
        skin.compose().save(os.path.join(PACK_DIR, mod.TEXTURE))
        geometries.append(skin.geometry())
        entries.append({
            "localization_name": mod.LOC,
            "geometry": mod.ID,
            "texture": mod.TEXTURE,
            "type": "paid",
        })
        lang.append(f"skin.{PACK_KEY}.{mod.LOC}={mod.NAME}")
        print(f"built {mod.NAME}: {len(skin.cubes)} cubes -> {mod.TEXTURE}")

    write_geometry(os.path.join(PACK_DIR, "geometry.json"), geometries)
    write_json("skins.json", {
        "skins": entries,
        "serialize_name": PACK_KEY,
        "localization_name": PACK_KEY,
    })
    write_json("manifest.json", {
        "format_version": 1,
        "header": {"name": "pack.name", "uuid": HEADER_UUID, "version": VERSION},
        "modules": [{"type": "skin_pack", "uuid": MODULE_UUID, "version": VERSION}],
    })
    write_json(os.path.join("texts", "languages.json"), ["en_US"])
    with open(os.path.join(PACK_DIR, "texts", "en_US.lang"), "w") as fh:
        fh.write("\n".join(lang) + "\n")


def write_json(rel, data):
    with open(os.path.join(PACK_DIR, rel), "w") as fh:
        json.dump(data, fh, indent=2)
        fh.write("\n")


if __name__ == "__main__":
    main()
