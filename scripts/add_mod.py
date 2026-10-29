"""Turn a "Submit a mod" issue into a mod page, a README card and a preview.

Reads the issue body from the ISSUE_BODY environment variable. Prints the new
mod's name on success; exits with an error message the workflow posts back on
the issue.
"""
import json
import os
import re
import sys
from pathlib import Path

from fetch_previews import API, ROOT, get

STATUS = {"🟢": "🟢", "🟡": "🟡", "🔴": "🔴"}
GAMEBANANA = re.compile(r"^https://(?:www\.)?gamebanana\.com/mods/(\d+)/?$")
GITHUB = re.compile(r"^https://github\.com/([\w.-]+)/([\w.-]+?)(?:\.git)?/?$")
BAD_LINK = "The mod link must be a GameBanana page (https://gamebanana.com/mods/123456) or a GitHub repository (https://github.com/owner/repo)"


def parse_form(body):
    """Return {label: value} from the '### Label' sections of an issue form."""
    fields = {}
    for label, value in re.findall(r"^### (.+?)\n\n(.*?)(?=\n### |\Z)", body.strip(), re.S | re.M):
        value = value.strip()
        fields[label.strip()] = "" if value == "_No response_" else value
    return fields


def slugify(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def classify(link):
    """Return (source, canonical url) for a GameBanana or GitHub link, or exit."""
    link = link.strip()
    if m := GAMEBANANA.match(link):
        return "GameBanana", f"https://gamebanana.com/mods/{m[1]}"
    if m := GITHUB.match(link):
        return "GitHub", f"https://github.com/{m[1]}/{m[2]}"
    sys.exit(BAD_LINK)


def mod_info(source, url):
    """Return (name, author, description) from the hosting site's public API."""
    if source == "GameBanana":
        page = json.loads(get(API.format(url.rsplit("/", 1)[1])))
        submitter = page.get("_aSubmitter") or {}
        return page["_sName"], submitter.get("_sName", "Unknown"), ""
    owner, repo = url.split("github.com/")[1].split("/")
    data = json.loads(get(f"https://api.github.com/repos/{owner}/{repo}"))
    name = data["name"].replace("-", " ").replace("_", " ")
    return (name.title() if name == name.lower() else name), data["owner"]["login"], data.get("description") or ""


def forge_card(forge):
    return f'<b>Requires <a href="mods/forge/README.md">Forge</a>:</b> {forge}<br>\n'


def forge_page(forge):
    return f"- **Requires [Forge](../forge/README.md):** {forge}\n"


def forge_text(fields):
    """'No', or 'Yes (version)' from the form's Forge fields."""
    if fields.get("Requires Forge", "No").strip() != "Yes":
        return "No"
    version = fields.get("Forge version needed", "").strip()
    return f"Yes ({version})" if version else "Yes"


def card(name, slug, status, author, source, url, version, platform, forge, with_image):
    img = (f'<img src="mods/{slug}/preview.jpg" width="360" alt="{name} preview">'
           if with_image else "<sub>No preview yet</sub>")
    return f'''<table>
<tr>
<td align="center" width="380">{img}</td>
<td width="520">
<h3><a href="mods/{slug}/README.md">{name}</a> {status}</h3>
<b>Author:</b> {author}<br>
<b>Download:</b> <a href="{url}">{source}</a><br>
{forge_card(forge)}<b>Tested recomp version:</b> {version}<br>
<b>Tested platform:</b> {platform}<br>
<a href="mods/{slug}/README.md">Install steps and details</a>
</td>
</tr>
</table>
'''


def page(name, slug, status, status_text, author, source, url, description, version, platform, issues, forge):
    preview_line = ""  # the preview is added once an image is found
    return f'''# {name}

- **Author:** {author}
- **Download:** [{source}]({url})
{forge_page(forge)}- **Mod license:** see the mod's {source} page
- **Status:** {status} {status_text}

{preview_line}## Description

{description or f'See the [{source} page]({url}) for what this mod does.'}

## Tested with

| Recomp version or commit | Tested platform |
| --- | --- |
| {version} | {platform} |

## Install

1. Download the mod from the link above.
2. Create `mods/{slug}/` in your MHGU Recomp folder.
3. Copy the mod's `romfs` and/or `exefs` folders into `mods/{slug}/`.

## Known issues

{issues or "None known."}
'''


def insert_card(readme, name, new_card):
    """Insert the card into README keeping the cards alphabetical by mod name."""
    start = readme.index("<!-- mods:start -->") + len('<!-- mods:start -->\n<div align="center">\n\n')
    end = readme.index("</div>\n<!-- mods:end -->", start)
    cards = [c.strip() + "\n" for c in re.findall(r"<table>.*?</table>\n?", readme[start:end], re.S)]
    cards.append(new_card)
    cards.sort(key=lambda c: re.search(r'<h3><a [^>]*>(.*?)</a>', c)[1].casefold())
    return readme[:start] + "\n".join(cards) + "\n" + readme[end:]


def build(fields, name, author, source, url, description="", root=ROOT):
    slug = slugify(name)
    readme_path = root / "README.md"
    readme = readme_path.read_text(encoding="utf-8")
    if f'href="{url}"' in readme or (root / "mods" / slug).exists():
        sys.exit("This mod is already in the directory.")
    status_text = fields["Compatibility"].strip()
    status = status_text[:1] if status_text[:1] in STATUS else "🟢"
    status_label = status_text[1:].strip()
    issues = fields.get("Known issues", "")
    if status != "🟢" and not issues:
        sys.exit('Please describe the problems under "Known issues" for a 🟡 or 🔴 mod.')
    version = fields["MHGU Recomp version tested"].strip()
    platform = fields["Tested platform"].strip()
    folder = root / "mods" / slug
    folder.mkdir(parents=True)
    (folder / "README.md").write_text(
        page(name, slug, status, status_label, author, source, url, description, version, platform, issues, forge_text(fields)),
        encoding="utf-8")
    readme_path.write_text(
        insert_card(readme, name, card(name, slug, status, author, source, url, version, platform, forge_text(fields), False)),
        encoding="utf-8")
    return slug


def main():
    fields = parse_form(os.environ["ISSUE_BODY"])
    source, url = classify(fields.get("Mod link", ""))
    name, author, description = mod_info(source, url)
    slug = build(fields, name, author, source, url, description)
    import fetch_previews
    fetch_previews.main({slug}, fields.get("Screenshot", ""))
    print(slug)


if __name__ == "__main__":
    main()
