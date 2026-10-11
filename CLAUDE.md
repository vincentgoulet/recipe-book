# Recipe book

Recipes live in `recipes/<kebab-case-title>.md`, one file per recipe, built from `TEMPLATE.md`.

## Rules for adding or updating recipes

- **Never extrapolate.** Do not invent ingredients, quantities, temperatures, times, steps, or servings. If it isn't in the provided notes, it isn't in the recipe.
- **Convert, don't create.** Always reshape the provided info into the template format (split into ingredients/steps, normalize wording, order sections). Conversion may restructure; it may not add facts.
- **Mark gaps explicitly.** Missing info is `TBD`. Missing steps get a gap marker (`_[TBD: missing step(s) between N and N+1]_`). Ambiguities go under **Open questions**.
- **Unit conversions** only when exact (e.g. 1 tbsp = 15 ml); keep the original in parentheses. No guessing for cup-to-gram conversions of ingredients.
- **Recipes are never final.** `status` is `draft`, `in-progress`, or `tested` — never `final`. New notes merge into the existing file; contradictions with earlier notes go to **Open questions** rather than silently overwriting.
- **Keep the raw input.** Append each drop of source notes verbatim under **Source notes**, dated, and add a **Changelog** line. Bump `updated`.
- Leave template sections in place with `TBD` even when empty.

## Git

- Work on `develop`. Commit and push freely, partial work included; something saved beats nothing.
