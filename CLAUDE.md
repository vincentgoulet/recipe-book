# Recipe book

## Principles (persistent)

1. **Current truth only.** Each recipe is the single most truthful, up-to-date version. Nothing else is kept: no history, changelogs, alternatives, earlier versions, option lists, or source commentary.
2. **Lean.** Strip anything not current. Short, plain statements. If something is superseded, delete it; don't annotate it.
3. **The user's reality wins.** What the user actually used or did replaces any suggestion from a source, outright.
4. **Never extrapolate.** Never invent ingredients, quantities, temperatures, times, steps, or servings. Unknown stays `null` / `{TBD}` (rendered `TBD`); missing steps get a `gap:` item.
5. **Convert, always.** Any input (notes, chats, screenshots) is reshaped into the data format. Conversion may restructure and condense; it may not add facts.
6. **Never final.** `status` is `draft`, `in-progress`, or `tested`; never `final`.
7. **Git is the history.** Superseded content is recoverable from git, so the working tree holds only the current state.

## Layout

```
templates/recipe.yaml          blank data template
recipes/<slug>/recipe.yaml     recipe data: the only thing to edit
recipes/<slug>/README.md       GENERATED, never edit by hand
recipes/README.md              GENERATED index
scripts/render.py              YAML → markdown: `python3 scripts/render.py` (all), `--check`,
                               or `python3 scripts/render.py FILE.yaml [-o OUT.md]`
```

After any change to a `recipe.yaml`: update `updated`, run `python3 scripts/render.py`, commit YAML and generated files together. Open questions list only current gaps worth resolving; remove them once answered.

## Git

- Work on `develop`. Commit and push freely, partial work included; something saved beats nothing.
