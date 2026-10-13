"""Build skin packs from the skin scripts in tools/skins/<pack>/.

    python3 tools/build_pack.py                 # every pack
    python3 tools/build_pack.py solar_system    # just this pack

Writes textures, geometry.json, skins.json, manifest.json and texts/ into the
pack's folder (see tools/packs.py).
"""

import importlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

from packs import PACKS  # noqa: E402
from skinlib import write_geometry  # noqa: E402


def load_skin(pack, name):
    """Import tools/skins/<pack>/<name>.py."""
    return importlib.import_module(f"skins.{pack}.{name}")


def build(pack):
    cfg = PACKS[pack]
    pack_dir = os.path.join(ROOT, cfg["dir"])
    key = cfg["dir"]
    os.makedirs(os.path.join(pack_dir, "texts"), exist_ok=True)
    geometries, entries, lang = [], [], [f"skinpack.{key}={cfg['name']}"]
    for module_name in cfg["skins"]:
        mod = load_skin(pack, module_name)
        skin = mod.build()
        skin.compose().save(os.path.join(pack_dir, mod.TEXTURE))
        geometries.append(skin.geometry())
        entries.append({
            "localization_name": mod.LOC,
            "geometry": mod.ID,
            "texture": mod.TEXTURE,
            "type": "paid",
        })
        lang.append(f"skin.{key}.{mod.LOC}={mod.NAME}")
        print(f"built {mod.NAME}: {len(skin.cubes)} cubes -> {cfg['dir']}/{mod.TEXTURE}")

    def write_json(rel, data):
        with open(os.path.join(pack_dir, rel), "w") as fh:
            json.dump(data, fh, indent=2)
            fh.write("\n")

    write_geometry(os.path.join(pack_dir, "geometry.json"), geometries)
    write_json("skins.json", {
        "skins": entries,
        "serialize_name": key,
        "localization_name": key,
    })
    write_json("manifest.json", {
        "format_version": 1,
        "header": {"name": "pack.name", "uuid": cfg["header_uuid"], "version": cfg["version"]},
        "modules": [{"type": "skin_pack", "uuid": cfg["module_uuid"], "version": cfg["version"]}],
    })
    write_json(os.path.join("texts", "languages.json"), ["en_US"])
    with open(os.path.join(pack_dir, "texts", "en_US.lang"), "w") as fh:
        fh.write("\n".join(lang) + "\n")


def main():
    for pack in sys.argv[1:] or PACKS:
        build(pack)


if __name__ == "__main__":
    main()
