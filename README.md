# CV

A script for generating my CV: content lives in YAML and the layout in HTML/CSS.
Headless Chromium prints it to a one-page A4 PDF.

## Setup

Requires [uv](https://docs.astral.sh/uv/) for dependency management.

```sh
uv sync
uv run playwright install chromium
```

Next, copy `data/private.example.yaml` to `data/private.yaml` and fill in your values. These are values that won't be git-versioned.

## Build

```sh
uv run python -m cv_builder
```

This writes `build/Alejandro Muelas.pdf`, along with `build/cv.html` for previewing layout changes in a browser.

## Credits

Icons by [Font Awesome](https://fontawesome.com) (CC BY 4.0) and [Simple Icons](https://simpleicons.org) (CC0).
Company logos are trademarks of their respective owners.
Typeface: [Carlito](https://github.com/googlefonts/carlito) (SIL OFL 1.1).
