# Recipe book

Recipe **data** and **output** are separate:

```
templates/recipe.yaml              blank data template (field reference)
recipes/<slug>/recipe.yaml         the recipe data — the only thing to edit
recipes/<slug>/sources/            raw source files (screenshots, photos, PDFs), kept as-is
recipes/<slug>/README.md           GENERATED markdown — never edit by hand
recipes/README.md                  GENERATED index
scripts/render.py                  YAML → markdown (`python3 scripts/render.py`, `--check` to verify)
```

After any change to a `recipe.yaml`, run `python3 scripts/render.py` and commit the YAML and generated files together. Output layout and formatting live only in `render.py`.

## Rules for adding or updating recipes

- **Never extrapolate.** Do not invent ingredients, quantities, temperatures, times, steps, or servings. If it isn't in the provided notes, it isn't in the recipe.
- **Convert, don't create.** Always reshape the provided info into the data format (split into ingredients/steps, normalize wording, order sections). Conversion may restructure; it may not add facts.
- **Mark gaps explicitly.** Unknown fields stay `null` / empty (rendered as `TBD`). Inline unknowns use `{TBD}`. Missing steps get a `gap:` item. Ambiguities go in `open_questions`.
- **Unit conversions** only when exact (e.g. 1 tbsp = 15 ml); keep the original in parentheses. No guessing for cup-to-gram conversions of ingredients.
- **Recipes are never final.** `status` is `draft`, `in-progress`, or `tested` — never `final` (render.py rejects it). New notes merge into the existing data; contradictions with earlier notes go to `open_questions` rather than silently overwriting.
- **Keep the raw input.** Add each drop of source notes under `sources` (verbatim `text`, and/or `files` saved in `recipes/<slug>/sources/`), with a date, plus a `changelog` entry. Bump `updated`. Text cut off or illegible in a file source is `TBD`, never guessed.
- **Multiple versions in one source** (e.g. original vs scaled quantities): use the latest version for `ingredients`, keep the others in a `tables` entry, and put any conflicts in `open_questions`.

## Git

- Work on `develop`. Commit and push freely, partial work included; something saved beats nothing.
