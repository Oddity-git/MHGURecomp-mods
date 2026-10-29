"""Fetch each GameBanana mod's first screenshot as mods/<slug>/preview.jpg.

Only mods without a preview.jpg are touched, so screenshots added by hand are
never overwritten. Pass slugs as arguments to limit the run to those mods.
"""
import io
import json
import re
import sys
import urllib.request
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
API = "https://gamebanana.com/apiv11/Mod/{}/ProfilePage"
HEADERS = {"User-Agent": "MHGURecomp-mods preview fetcher"}


def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=HEADERS), timeout=30) as r:
        return r.read()


def first_image_url(mod_id):
    media = json.loads(get(API.format(mod_id)))["_aPreviewMedia"]["_aImages"]
    return f'{media[0]["_sBaseUrl"]}/{media[0]["_sFile"]}'


def update_card(slug):
    readme = ROOT / "README.md"
    text = readme.read_text(encoding="utf-8")
    card = re.compile(
        r'(<td align="center" width="380">)<sub>No preview yet</sub>(</td>\s*<td width="520">\s*'
        r'<h3><a href="mods/%s/README\.md">)' % re.escape(slug)
    )
    img = f'<img src="mods/{slug}/preview.jpg" width="360" alt="{slug} preview">'
    readme.write_text(card.sub(lambda m: m[1] + img + m[2], text), encoding="utf-8")


def main(only):
    for page in sorted((ROOT / "mods").glob("*/README.md")):
        slug = page.parent.name
        dest = page.parent / "preview.jpg"
        if (only and slug not in only) or dest.exists():
            continue
        found = re.search(r"gamebanana\.com/mods/(\d+)", page.read_text(encoding="utf-8"))
        if not found:
            continue
        try:
            image = Image.open(io.BytesIO(get(first_image_url(found[1])))).convert("RGB")
        except Exception as err:  # keep going so one bad mod doesn't block the rest
            print(f"{slug}: skipped ({err})")
            continue
        image.thumbnail((1280, 1280))
        image.save(dest, quality=85)
        update_card(slug)
        print(f"{slug}: saved {image.size[0]}x{image.size[1]}")


if __name__ == "__main__":
    main(set(sys.argv[1:]))
