# Minecraft-Skins

Bedrock Edition skin packs with HD textures and custom 3D geometry.

| Pack | Folder | Skins |
| --- | --- | --- |
| Midnight Mischief | `MidnightMischief/` | 12 Halloween characters |
| Solar System | `SolarSystem/` | Aliens from the Sun, planets, Moon and Pluto (in progress) |

Each pack folder is the skin pack itself. You can zip it or drop it into the Marketplace submission:

| File | Purpose |
| --- | --- |
| `manifest.json` | Pack header (`skin_pack` module) |
| `skins.json` | One entry per skin: texture, custom geometry id, `paid` |
| `geometry.json` | Custom 3D geometry (format 1.12.0, per-face UVs) for every skin |
| `*.png` | 128x128 HD skin textures |
| `texts/` | `en_US.lang` names and `languages.json` |

Each skin keeps every standard player bone (`root`, `waist`, `body`, `head`, `hat`, arms, legs, sleeves, pants, `jacket`, `cape`, item bones). Vanilla animations, held items and capes keep working. 3D accessories are extra cubes on those bones, or on extra child bones (such as a tilted ring) that follow them.

> Custom geometry in skin packs only loads in Marketplace partner content. In a sideloaded or free pack, Mojang only lets you use `geometry.humanoid.custom` and `geometry.humanoid.customSlim`.

## Midnight Mischief

The first 8 skins follow the line-up art in `reference/`; the last 4 are originals in the same style.

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

## Solar System

| Skin | Home | Arms | 3D extras |
| --- | --- | --- | --- |
| Sol the Sun King | The Sun | Classic | Corona of 16 rays behind the head, flame-hemmed cape, gold pauldrons, gold boots |
| Saturna | Saturn | Slim | Tilted 16-sided ring with the Cassini gap and a tiny moon, space buns, pointed ears, flared skirt, platform boots |
| Neptide | Neptune | Classic | Gold trident across the back, dorsal-fin crest, fin ears, forearm + calf fins, webbed feet |

## Previews

`previews/<pack>/lineup.png` shows a whole pack. `previews/<pack>/<skin>/` has a turnaround, poses, 3D detail close-ups, a turntable GIF, the texture map and, where there is reference art, a side-by-side with it.

## Building

```sh
python3 tools/build_pack.py                          # every pack (or name one: solar_system)
(cd tools/render && npm install)                      # three.js for previews
python3 tools/make_previews.py solar_system           # all of a pack's skins + lineup
python3 tools/make_previews.py solar_system saturna   # just one skin
```

- `tools/packs.py` lists the packs: folder, name, manifest UUIDs, skin order and preview colours.
- `tools/skinlib.py` holds the rig (classic and slim), the HD UV layout (2 texels per unit), automatic UV packing for accessories, rotated cubes and extra bones, cubes that share one texture patch, and the geometry export.
- `tools/paintkit.py` holds shared painters: fabric, hair/fur, sneakers, boots, gradients, starfields, flames.
- `tools/skins/<pack>/<skin>.py` holds one skin's cubes and its painted texture.
- `tools/render/` is a headless three.js viewer. It reads the real `geometry.json` and PNG and follows Bedrock's per-face UV rules, including the flipped `down` face and Blockbench's rotation convention. That makes the previews match what the game draws.
