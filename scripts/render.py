#!/usr/bin/env python3
"""Render recipes/<slug>/recipe.yaml into recipes/<slug>/README.md (+ recipes/README.md index).

Usage:
  python3 scripts/render.py           # render everything
  python3 scripts/render.py --check   # exit 1 if any rendered file is out of date
  python3 scripts/render.py FILE.yaml [-o OUT.md]   # convert one file (stdout by default)

Missing data (null / empty) renders as TBD. The renderer never fills anything in.
"""
import argparse
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
RECIPES = ROOT / "recipes"
STATUSES = {"draft", "in-progress", "tested"}
TBD = "TBD"
HEADER = "<!-- Generated from recipe.yaml by scripts/render.py. Edit the YAML, not this file. -->"


def val(x):
    if x is None or x == "" or x == []:
        return TBD
    return str(x).replace("{TBD}", TBD).strip()


def bullets(items):
    return [f"- {val(i)}" for i in items] if items else [f"- {TBD}"]


def ingredient_line(i):
    if i.get("qty") in (None, ""):
        line = val(i.get("name"))
    else:
        line = " ".join(p for p in (val(i["qty"]), i.get("unit") or "", val(i.get("name"))) if p)
    if i.get("prep"):
        line += f", {val(i['prep'])}"
    if i.get("optional"):
        line += " *(optional)*"
    if i.get("note"):
        line += f" — {val(i['note'])}"
    return f"- {line}"


def cell(x):
    return "—" if x is None else str(x).replace("|", "\\|")


def render(r, slug):
    status = r.get("status") or "draft"
    if status not in STATUSES:
        raise ValueError(f"{slug}: status must be one of {sorted(STATUSES)}, got {status!r}")
    t = r.get("time") or {}
    out = [HEADER, "", f"# {val(r.get('title'))}", ""]
    out += [
        f"**Status:** {status} · **Servings:** {val(r.get('servings'))}  ",
        f"**Prep:** {val(t.get('prep'))} · **Cook:** {val(t.get('cook'))} · **Total:** {val(t.get('total'))}  ",
        f"**Tags:** {', '.join(r.get('tags') or []) or TBD} · **Created:** {val(r.get('created'))} · **Updated:** {val(r.get('updated'))}",
        "",
        "> Living recipe: incomplete by design and never final. `TBD` means not provided yet.",
        "",
        "## Summary", "", val(r.get("summary")), "",
        "## Equipment", "", *bullets(r.get("equipment")), "",
        "## Ingredients", "",
    ]
    groups = r.get("ingredients") or []
    if not groups:
        out += [f"- {TBD}", ""]
    for g in groups:
        if g.get("group"):
            out += [f"### {g['group']}", ""]
        out += [ingredient_line(i) for i in g.get("items") or []] or [f"- {TBD}"]
        out.append("")

    out += ["## Steps", ""]
    sections = r.get("steps") or []
    if not sections:
        out += [f"1. {TBD}", ""]
    n = 0
    for s in sections:
        if s.get("section"):
            out += [f"### {s['section']}", ""]
        for st in s.get("items") or []:
            if "gap" in st:
                out.append(f"- _[TBD: {st['gap'] or 'missing step(s)'}]_")
                continue
            n += 1
            out.append(f"{n}. {val(st.get('text'))}")
            pad = " " * len(f"{n}. ")
            out += [f"{pad}- {val(d)}" for d in st.get("details") or []]
        out.append("")

    if r.get("notes"):
        out += ["## Notes", "", *bullets(r["notes"]), ""]
    for tb in r.get("tables") or []:
        cols = tb["columns"]
        out += [f"### {tb['title']}", "", "| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
        out += ["| " + " | ".join(cell(c) for c in row) + " |" for row in tb.get("rows") or []]
        if tb.get("footnote"):
            out += ["", tb["footnote"]]
        out.append("")

    out += ["## Open questions", "", *bullets(r.get("open_questions")), ""]

    out += ["## Sources", ""]
    srcs = r.get("sources") or []
    if not srcs:
        out += [f"- {TBD}", ""]
    for s in srcs:
        out += [f"### {val(s.get('date'))}: {val(s.get('description'))}", ""]
        if s.get("text"):
            out += ["> " + l if l else ">" for l in s["text"].rstrip().splitlines()] + [""]
        files = s.get("files") or []
        for f in files:
            out.append(f"- [{Path(f['path']).name}]({f['path']})" + (f": {f['caption']}" if f.get("caption") else ""))
        if files:
            out.append("")

    out += ["## Changelog", ""]
    out += [f"- {val(c.get('date'))}: {val(c.get('text'))}" for c in r.get("changelog") or []] or [f"- {TBD}"]
    return "\n".join(out).rstrip() + "\n"


def index(entries):
    out = [HEADER, "", "# Recipes", "", "| Recipe | Status | Updated |", "|---|---|---|"]
    out += [f"| [{val(r.get('title'))}]({slug}/) | {r.get('status') or 'draft'} | {val(r.get('updated'))} |"
            for slug, r in entries]
    return "\n".join(out) + "\n"


def main():
    ap = argparse.ArgumentParser(description="Render recipe YAML to markdown.")
    ap.add_argument("file", nargs="?", type=Path, help="convert a single recipe.yaml instead of the whole book")
    ap.add_argument("-o", "--output", type=Path, help="with FILE: write here instead of stdout")
    ap.add_argument("--check", action="store_true", help="exit 1 if any rendered file is out of date")
    args = ap.parse_args()

    if args.file:
        r = yaml.safe_load(args.file.read_text()) or {}
        slug = args.file.parent.name if args.file.name == "recipe.yaml" else args.file.stem
        md = render(r, slug)
        if args.output:
            args.output.write_text(md)
        else:
            sys.stdout.write(md)
        return

    check = args.check
    outputs, entries = {}, []
    for y in sorted(RECIPES.glob("*/recipe.yaml")):
        slug = y.parent.name
        r = yaml.safe_load(y.read_text()) or {}
        entries.append((slug, r))
        outputs[y.parent / "README.md"] = render(r, slug)
    outputs[RECIPES / "README.md"] = index(entries)

    stale = [p for p, text in outputs.items() if not p.exists() or p.read_text() != text]
    if check:
        for p in stale:
            print(f"out of date: {p.relative_to(ROOT)}")
        sys.exit(1 if stale else 0)
    for p in stale:
        p.write_text(outputs[p])
        print(f"wrote {p.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
