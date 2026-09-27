#!/usr/bin/env python3
"""Render output/index.html from output/meta.json + output/*.csv using scripts/page_template.html.
Standard library only, so it can run anywhere with python3."""
import csv, json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "output"
SHEETS = ["Schedule", "Goalies", "Teams", "Skaters"]


def typed(v):
    if v == "":
        return None
    for f in (int, float):
        try:
            return f(v)
        except ValueError:
            pass
    return v


def rows(name):
    f = OUT / f"{name.lower()}.csv"
    if not f.exists() or f.stat().st_size == 0:
        return []
    with f.open(newline="") as fh:
        return [{k: typed(v) for k, v in r.items() if k != "playerId"} for r in csv.DictReader(fh)]


def main():
    tpl = (ROOT / "scripts" / "page_template.html").read_text()
    meta = json.loads((OUT / "meta.json").read_text())
    page = tpl.replace("__META__", json.dumps(meta))
    for name in SHEETS:
        page = page.replace(f"__{name.upper()}__", json.dumps(rows(name)).replace("</", "<\\/"))
    (OUT / "index.html").write_text(page)
    print(f"wrote {OUT / 'index.html'} ({len(page):,} bytes); data through {meta['data_through']}, built {meta['built_pt']} PT")


if __name__ == "__main__":
    main()
