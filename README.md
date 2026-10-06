# Portfolio

Nicola Jade Feldmann's portfolio. Static site, hosted on GitHub Pages.

## How it is put together

Every page is a standalone HTML file with its styles inside it, so any single file can be opened or previewed on its own.

- `index.html` is the home page.
- `all-work.html` lists every project, one line each.
- `work/<slug>.html` is one case study each.
- `_build/content.py` holds all the words. Edit the words here.
- `_build/build.py` holds the design and the page templates. Run `python3 _build/build.py` from the repo root to regenerate every page.

## Adding a case study

1. Add a new entry to `CASES` in `_build/content.py` (copy an existing one).
2. Run `python3 _build/build.py`.
3. Commit `index.html`, `all-work.html` and the new `work/<slug>.html`.

## Rules for the words

First person. British spelling. No client names, prices, figures, IDs or links. No em or en dashes.
