"""Stamp local CSS and JS references with a content hash (?v=...) so browsers fetch new copies after a deploy.
Run from the repository root after changing any file in assets/css or assets/js: python3 scripts/stamp.py
"""
import hashlib, re, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGES = ["index.html", "capability-statement.html", "slick-sheet.html", "404.html"]
PAT = re.compile(r'((?:href|src)=")(/?assets/(?:css|js)/[A-Za-z0-9._-]+)(\?v=[0-9a-f]+)?(")')
def stamp(m):
    rel = m.group(2).lstrip("/")
    digest = hashlib.sha256((ROOT / rel).read_bytes()).hexdigest()[:10]
    return f'{m.group(1)}{m.group(2)}?v={digest}{m.group(4)}'
for name in PAGES:
    p = ROOT / name
    before = p.read_text(encoding="utf-8")
    after = PAT.sub(stamp, before)
    if after != before:
        p.write_text(after, encoding="utf-8")
        print("stamped", name)
