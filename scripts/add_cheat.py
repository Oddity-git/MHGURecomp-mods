"""Turn a "Submit a cheat" issue into an entry in the README's Cheats section.

Reads the issue body from the ISSUE_BODY environment variable. Prints the
cheat's name on success; exits with an error message the workflow posts back
on the issue.
"""
import html
import os
import re
import sys

from add_mod import parse_form
from fetch_previews import ROOT

START, END = "<!-- cheats:start -->", "<!-- cheats:end -->"


def clean_name(name):
    return re.sub(r"\s+", " ", name.strip().strip("[]").strip())


def clean_text(text):
    """Join a description into one paragraph, dropping leading '#' comment marks."""
    lines = [re.sub(r"^#+\s?", "", line).strip() for line in text.splitlines()]
    return " ".join(line for line in lines if line)


def clean_code(code):
    code = code.strip()
    code = re.sub(r"^```\w*\n?", "", code)
    return re.sub(r"\n?```$", "", code).strip()


def entry(fields):
    name = clean_name(fields["Cheat name"])
    code = clean_code(fields["Cheat code or link"])
    code_part = code if code.startswith("http") and "\n" not in code else None
    details = [
        f"<b>What it does:</b> {html.escape(clean_text(fields['What it does']))}",
        f"<b>Tested recomp version:</b> {html.escape(fields['MHGU Recomp version tested'].strip())}",
        f"<b>Tested platform:</b> {html.escape(fields['Tested platform'].strip())}",
    ]
    issues = clean_text(fields.get("Known issues", ""))
    if issues:
        details.append(f"<b>Known issues:</b> {html.escape(issues)}")
    body = "<br>\n".join(details)
    if code_part:
        code_block = f'<b>Cheat:</b> <a href="{html.escape(code_part)}">{html.escape(code_part)}</a>'
    else:
        code_block = f"\n```text\n[{name}]\n{code}\n```\n"
    return name, f"<details>\n<summary><b>{html.escape(name)}</b></summary>\n\n{body}\n\n{code_block}\n</details>\n"


def main():
    fields = parse_form(os.environ["ISSUE_BODY"])
    for label in ("Cheat name", "What it does", "Cheat code or link", "MHGU Recomp version tested", "Tested platform"):
        if not fields.get(label, "").strip():
            sys.exit(f'The "{label}" field is empty.')
    name, new = entry(fields)
    path = ROOT / "README.md"
    readme = path.read_text(encoding="utf-8")
    start, end = readme.index(START) + len(START), readme.index(END)
    block = readme[start:end]
    if f"<summary><b>{html.escape(name)}</b></summary>" in block:
        sys.exit("A cheat with this name is already in the directory.")
    block = re.sub(r"\s*<p align=\"center\"><sub>No cheats listed yet\.</sub></p>\s*", "\n", block)
    entries = re.findall(r"<details>.*?</details>\n?", block, re.S) + [new]
    entries.sort(key=lambda e: re.search(r"<summary><b>(.*?)</b>", e)[1].casefold())
    path.write_text(readme[:start] + "\n\n" + "\n".join(e.strip() + "\n" for e in entries) + "\n" + readme[end:], encoding="utf-8")
    print(name)


if __name__ == "__main__":
    main()
