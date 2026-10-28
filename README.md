# MHGURecomp-mods

A curated directory of mods tested with [MHGU Recomp](https://github.com/morerokk/MHGURecomp), with links to each mod's download page, install steps, and the versions and platforms they're confirmed to work on.

This repository only holds links and notes. No mod files are hosted here: download each mod from the page its author published it on.

## Mod list

| Mod | Author | Download | Tested recomp version | Platform | Notes |
| --- | --- | --- | --- | --- | --- |
| [MH4U port to MHGU](mods/mh4u-port/README.md) | Scrimas | [GitHub](https://github.com/Scrimas/MH4U-port-to-MHGU) | TBD | TBD | |

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
