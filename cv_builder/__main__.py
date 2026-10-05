from pathlib import Path

from cv_builder.html import write_html
from cv_builder.loader import load_cv
from cv_builder.pdf import print_to_pdf

REPOSITORY_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPOSITORY_ROOT / "data"
TEMPLATES_DIR = REPOSITORY_ROOT / "templates"
ASSETS_DIR = REPOSITORY_ROOT / "assets"
BUILD_DIR = REPOSITORY_ROOT / "build"


def main() -> None:
    cv = load_cv(DATA_DIR)
    html_file = BUILD_DIR / "cv.html"
    pdf_file = BUILD_DIR / f"{cv.name}.pdf"

    write_html(cv, TEMPLATES_DIR, ASSETS_DIR, html_file)
    print_to_pdf(html_file, pdf_file)
    print(f"Wrote {pdf_file}")


if __name__ == "__main__":
    main()
