"""Find a screenshot for each mod and save it as a 16:9 mods/<slug>/preview.jpg.

Sources, in order: a screenshot uploaded with the submission form, the first
screenshot on the mod's GameBanana page, then the first real image in the
mod's GitHub README. Only mods without a preview.jpg are touched, so
screenshots added by hand are never overwritten. Pass slugs as arguments to
limit the run to those mods.
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
MAX_BYTES = 15 * 1024 * 1024
# Issue-form uploads only ever live on these GitHub hosts; nothing else is fetched from an issue.
UPLOAD = re.compile(
    r"https://(?:github\.com/user-attachments/(?:assets|files)/[\w./-]+"
    r"|user-images\.githubusercontent\.com/[\w./-]+)"
)
SKIP = ("shields.io", "badge", "badgen", "travis-ci", "/workflows/", "codecov", "sponsor", ".svg", "logo", "icon")


def get(url, accept=None):
    headers = dict(HEADERS, **({"Accept": accept} if accept else {}))
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=30) as r:
        return r.read(MAX_BYTES + 1)[:MAX_BYTES]


def gamebanana_image(mod_id):
    media = json.loads(get(API.format(mod_id)))["_aPreviewMedia"]["_aImages"]
    return get(f'{media[0]["_sBaseUrl"]}/{media[0]["_sFile"]}')


def readme_image_urls(markdown, owner, repo):
    """Candidate screenshot URLs from a README, in page order, without badges and icons."""
    found = re.findall(r"!\[[^\]]*\]\(\s*<?([^)\s>]+)", markdown)
    found += re.findall(r"<img[^>]+src=[\"']([^\"']+)[\"']", markdown)
    ordered = sorted(set(found), key=lambda u: markdown.find(u))
    urls = []
    for url in ordered:
        if any(bad in url.lower() for bad in SKIP):
            continue
        if not url.startswith("http"):
            url = f"https://raw.githubusercontent.com/{owner}/{repo}/HEAD/{url.lstrip('./')}"
        urls.append(url)
    return urls


def github_image(owner, repo):
    markdown = get(
        f"https://api.github.com/repos/{owner}/{repo}/readme", accept="application/vnd.github.raw"
    ).decode("utf-8", "replace")
    for url in readme_image_urls(markdown, owner, repo):
        try:
            image = Image.open(io.BytesIO(get(url)))
            if image.size[0] >= 300:  # skips tiny icons
                return get(url)
        except Exception:
            continue
    return None


def uploaded_image(text):
    found = UPLOAD.search(text or "")
    return get(found[0]) if found else None


def find_image(page_text, uploaded_text=""):
    for source in (
        lambda: uploaded_image(uploaded_text),
        lambda: (lambda m: gamebanana_image(m[1]) if m else None)(re.search(r"gamebanana\.com/mods/(\d+)", page_text)),
        lambda: (lambda m: github_image(m[1], m[2]) if m else None)(
            re.search(r"https://github\.com/([\w.-]+)/([\w.-]+?)\)", page_text)
        ),
    ):
        try:
            data = source()
        except Exception as err:  # a bad source shouldn't stop the next one
            print(f"  source failed ({err})")
            continue
        if data:
            return data
    return None


def crop_16_9(image):
    """Center-crop to 16:9 so every preview has the same shape, then cap the size."""
    width, height = image.size
    if width * 9 > height * 16:  # too wide: trim the sides
        new_width = height * 16 // 9
        left = (width - new_width) // 2
        image = image.crop((left, 0, left + new_width, height))
    else:  # too tall: trim top and bottom
        new_height = width * 9 // 16
        top = (height - new_height) // 2
        image = image.crop((0, top, width, top + new_height))
    image.thumbnail((1280, 720))
    return image


def attach(slug, data):
    """Save the image and show it on the mod's card and page."""
    image = crop_16_9(Image.open(io.BytesIO(data)).convert("RGB"))
    image.save(ROOT / "mods" / slug / "preview.jpg", quality=85)
    readme = ROOT / "README.md"
    text = readme.read_text(encoding="utf-8")
    card = re.compile(
        r'(<td align="center" width="380">)<sub>No preview yet</sub>(</td>\s*<td width="520">\s*'
        r'<h3><a href="mods/%s/README\.md">)' % re.escape(slug)
    )
    img = f'<img src="mods/{slug}/preview.jpg" width="360" alt="{slug} preview">'
    readme.write_text(card.sub(lambda m: m[1] + img + m[2], text), encoding="utf-8")
    page = ROOT / "mods" / slug / "README.md"
    body = page.read_text(encoding="utf-8")
    if "![Preview](preview.jpg)" not in body:
        page.write_text(body.replace("\n## Description", "\n![Preview](preview.jpg)\n\n## Description", 1), encoding="utf-8")
    return image.size


def main(only, uploaded_text=""):
    for page in sorted((ROOT / "mods").glob("*/README.md")):
        slug = page.parent.name
        if (only and slug not in only) or (page.parent / "preview.jpg").exists():
            continue
        data = find_image(page.read_text(encoding="utf-8"), uploaded_text if only else "")
        if not data:
            print(f"{slug}: no image found")
            continue
        try:
            size = attach(slug, data)
        except Exception as err:
            print(f"{slug}: skipped ({err})")
            continue
        print(f"{slug}: saved {size[0]}x{size[1]}")


if __name__ == "__main__":
    main(set(sys.argv[1:]))
