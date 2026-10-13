# Minecraft-Skins

## Midnight Mischief (Bedrock skin pack)

`MidnightMischief/` is the skin pack itself. You can zip it or drop it into the Marketplace submission:

| File | Purpose |
| --- | --- |
| `manifest.json` | Pack header (`skin_pack` module) |
| `skins.json` | One entry per skin: texture, custom geometry id, `paid` |
| `geometry.json` | Custom 3D geometry (format 1.12.0, per-face UVs) for every skin |
| `*.png` | 128x128 HD skin textures |
| `texts/` | `en_US.lang` names and `languages.json` |

Each skin keeps every standard player bone (`root`, `waist`, `body`, `head`, `hat`, arms, legs, sleeves, pants, `jacket`, `cape`, item bones). Vanilla animations, held items and capes keep working. 3D accessories are extra cubes on those bones.

> Custom geometry in skin packs only loads in Marketplace partner content. In a sideloaded or free pack, Mojang only lets you use `geometry.humanoid.custom` and `geometry.humanoid.customSlim`.

### Skins

Every skin has a 128x128 HD texture and its own 3D geometry. The first 8 follow the line-up art in `reference/`; the last 4 are originals in the same style.

| Skin | Arms | 3D extras |
| --- | --- | --- |
| Pumpkin Prankster | Classic | Oversized jack-o'-lantern head, chunky sneakers with tongues |
| Moonlight Witch | Slim | Long hair down the back, front locks, bell cuffs, coat tails, platform boots |
| Boo Hoodie | Classic | Bunched hood, bulky cuffs, rolled pant cuffs, sneakers |
| Velvet Vampire | Classic | Standing collar, ruffled jabot, gold cuffs, coat tails, buckled boots |
| Frankie Stitches | Classic | Neck bolts, frayed rips, sneakers |
| Midnight Kitty | Classic | Cat ears, curled tail, puffy cuffs, cargo pockets, sneakers |
| Candy Corn Cutie | Slim | Candy-corn hood + drape, hair locks, puffy cuffs, mismatched sneakers |
| Bone Chiller | Classic | Hood peak + back hood, sneakers |
| Scarecrow Sam *(original)* | Classic | Wide straw hat, straw tufts at cuffs/neck, work boots |
| Lunar Howler *(original)* | Classic | Snout with fangs, pointed ears, bushy tail, torn sleeves/hem, clawed paws |
| Mummy Wraps *(original)* | Classic | Trailing bandage strips, loose wraps, pharaoh collar |
| Batty Belle *(original)* | Slim | Bat-ear hood, scalloped bat wings, sneakers |

`previews/lineup.png` shows the whole pack. `previews/<skin>/` has a turnaround, poses, 3D detail close-ups, a turntable GIF, the texture map and, for the first 8, a side-by-side with the reference art.

## Building

```sh
python3 tools/build_pack.py                         # textures + all pack JSON
(cd tools/render && npm install)                     # three.js for previews
python3 tools/make_previews.py                       # all skins + lineup
```

- `tools/skinlib.py` holds the rig (classic and slim), the HD UV layout (2 texels per unit), automatic UV packing for accessories and the geometry export.
- `tools/paintkit.py` holds shared painters: fabric, hair/fur, sneakers, boots.
- `tools/skins/<skin>.py` holds one skin's cubes and its painted texture.
- `tools/render/` is a headless three.js viewer. It reads the real `geometry.json` and PNG and follows Bedrock's per-face UV rules, including the flipped `down` face. That makes the previews match what the game draws.
