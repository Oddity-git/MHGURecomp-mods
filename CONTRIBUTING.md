# Contributing

Thanks for helping grow the list.

## The easy way: submit a mod

Open a [Submit a mod](../../issues/new?template=submit-mod.yml) issue and fill in the form: the mod's GameBanana or GitHub link, the recomp version and platform you tested on, and a compatibility status. A bot reads the mod's name, author and screenshot, builds its page and card, and opens a pull request for a maintainer to review. You don't need to edit any files.

## The manual way

If you'd rather open a pull request yourself, follow these rules to keep the list useful:

1. **Links only.** Never commit mod files, game files, or extracted assets. Link to the author's own release page (GameBanana, GitHub, etc.).
2. **Tested mods only.** Only add a mod you have run with MHGU Recomp yourself, and fill in the "Tested with" table honestly.
3. **One folder per mod.** Add `mods/<mod-name>/README.md` using [TEMPLATE.md](TEMPLATE.md), with a lowercase, hyphenated folder name.
4. **Add a card** in the main [README.md](README.md), keeping the cards in alphabetical order.
5. **Credit the author.** Name them and link their profile. If you're not the author, don't re-describe the mod as your own work.
6. **Set a status.** Use 🟢 when everything works, 🟡 when some features are missing or broken, and 🔴 when the mod doesn't work. For 🟡 and 🔴, list what's wrong under "Known issues".
7. **Add a preview image (optional).** Save one screenshot as `mods/<mod-name>/preview.jpg`, cropped to 16:9 (at most 1280×720, under 500 KB; the bot crops its own images the same way). Use your own screenshot or one the author is fine with you reusing. In the main README, each mod is a card (a small HTML table with the image on the left and the details on the right). Copy an existing card; leave `No preview yet` in the image cell until there is a screenshot.
8. **Updating an entry.** If you tested a mod on a newer recomp version or another platform, add a row to its "Tested with" table instead of replacing the old one.

Open a pull request with your changes. One mod per pull request is easiest to review.

## Submitting a cheat

Use the [Submit a cheat form](../../issues/new?template=submit-cheat.yml). Only submit cheats you have tested yourself. A maintainer adds them to the Cheats section.

## Reporting a problem with a mod

Use the [Report a mod issue](../../issues/new?template=report-mod-issue.yml) form. It asks which mod, your versions and platform, and which other mods you have installed, so it's clear whether the mod, a conflict between mods, or the recomp itself is at fault. If the problem also happens with no mods installed, report it on the [MHGU Recomp issue tracker](https://github.com/morerokk/MHGURecomp/issues) instead. Mod issues stay here and are not copied to the recomp's tracker. Only a pull request that fixes the problem is sent to the recomp, and it is opened there by whoever wrote the fix.
