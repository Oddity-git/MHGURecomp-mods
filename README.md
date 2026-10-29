<h1 align="center">MHGURecomp-mods</h1>

<p align="center">
A curated directory of mods tested with <a href="https://github.com/morerokk/MHGURecomp">MHGU Recomp</a>, with links to each mod's download page, install steps, and the versions and platforms they've been tested on.<br>
This repository only holds links and notes. No mod files are hosted here: download each mod from the page its author published it on.
</p>

<h2 align="center">Mod list</h2>

<h3 align="center">Compatibility status</h3>

| Status | Meaning |
| :---: | :--- |
| 🟢 | Full compatibility: everything the mod does works with the recomp. |
| 🟡 | Partial: the mod loads, but some of its features are missing or broken. |
| 🔴 | Broken: the mod doesn't work, or crashes the game. |

<h3 align="center">Mods</h3>

| Preview (click to expand) | Mod | Status | Author | Download | Tested recomp version | Tested platform |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| <details><summary>🖼️ Preview</summary><img src="mods/better-inputs/preview.jpg" width="480" alt="better-inputs preview"></details> | [Better Inputs](mods/better-inputs/README.md) | 🟢 | Fexty12573 | [GameBanana](https://gamebanana.com/mods/689270) | TBD | Linux |
| <details><summary>🖼️ Preview</summary><img src="mods/damage-numbers/preview.jpg" width="480" alt="damage-numbers preview"></details> | [Damage Numbers](mods/damage-numbers/README.md) | 🟢 | PurplefinNeptuna | [GameBanana](https://gamebanana.com/mods/725408) | TBD | Linux |
| — | [FF14-style Damage Text](mods/ff14-damage-text/README.md) | 🟢 | Filianore | [GameBanana](https://gamebanana.com/mods/727751) | TBD | Linux |
| — | [Full DualShock Buttons](mods/dualshock-buttons/README.md) | 🟢 | Abbanon | [GameBanana](https://gamebanana.com/mods/475878) | TBD | Linux |
| — | [Key Quest Markers](mods/key-quest-markers/README.md) | 🟢 | PurplefinNeptuna | [GameBanana](https://gamebanana.com/mods/727960) | TBD | Linux |
| — | [Monster Weakness Icons](mods/weakness-icons/README.md) | 🟢 | Potobc | [GameBanana](https://gamebanana.com/mods/488552) | TBD | Linux |
| — | [Xbox Controller Layout](mods/xbox-layout/README.md) | 🟢 | ishiki | [GameBanana](https://gamebanana.com/mods/410801) | TBD | Linux |

## Installing mods

MHGU Recomp loads mods from a `mods` folder next to the recomp executable. Each mod gets its own folder:

```
mods/
└── <mod-name>/
    ├── romfs/   # replacement game data files
    └── exefs/   # exefs patches
```

Most mods only use one of the two folders. If a mod was packaged for an emulator (for example Yuzu or Ryujinx `romfs`/`exefs` layout), copy those folders into `mods/<mod-name>/`. Check the mod's page here for anything specific to it.

## Adding a mod

See [CONTRIBUTING.md](CONTRIBUTING.md). Use [TEMPLATE.md](TEMPLATE.md) for a mod's page.

## License

The list itself is released under [CC0 1.0](LICENSE). Every linked mod is the work of its author and keeps its own license.
