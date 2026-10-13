"""Every skin pack in this repo.

Each pack has its skin scripts in tools/skins/<key>/, its built files in
<dir>/ and its previews in previews/<key>/. The skin list order is the order
skins appear in the in-game picker.
"""

PACKS = {
    "midnight_mischief": {
        "dir": "MidnightMischief",
        "name": "Midnight Mischief",
        "header_uuid": "f89add21-039f-463f-8e28-3761edc22e6e",
        "module_uuid": "57655c99-c40a-46b7-99b5-f1cfdbc2343b",
        "version": [1, 0, 0],
        "skins": ["pumpkin_prankster", "moonlight_witch", "boo_hoodie", "velvet_vampire",
                  "frankie_stitches", "midnight_kitty", "candy_corn_cutie", "bone_chiller",
                  "scarecrow_sam", "lunar_howler", "mummy_wraps", "batty_belle"],
        "reference": "reference/midnight_mischief_lineup.webp",
        # preview styling: backdrop centre/edge, title colour, label colour
        "style": {"bg": ((58, 24, 64), (24, 9, 28)), "title": (236, 200, 255),
                  "label": (255, 170, 70)},
    },
    "solar_system": {
        "dir": "SolarSystem",
        "name": "Solar System",
        "header_uuid": "4b7b6c14-5d28-4b59-8c7d-bf0b130d8f6a",
        "module_uuid": "6c4d82ac-a74a-485d-9575-b220ce2b81af",
        "version": [1, 0, 0],
        "skins": ["sol", "saturna", "neptide"],
        "style": {"bg": ((26, 34, 74), (6, 7, 22)), "title": (196, 220, 255),
                  "label": (255, 204, 92)},
    },
}
