from pathlib import Path

from playwright.sync_api import Page, sync_playwright

CSS_PIXELS_PER_MM = 96 / 25.4


class PageOverflowError(Exception):
    pass


def print_to_pdf(html_file: Path, pdf_file: Path) -> None:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page()
        page.goto(html_file.as_uri())
        page.evaluate("document.fonts.ready")
        _ensure_content_fits_on_one_page(page)
        page.pdf(path=pdf_file, prefer_css_page_size=True, print_background=True)
        browser.close()


def _ensure_content_fits_on_one_page(page: Page) -> None:
    overflow_px = page.evaluate(
        """() => Math.max(...[...document.querySelectorAll(".page > *")]
            .map(column => column.scrollHeight - column.clientHeight))"""
    )
    if overflow_px > 0:
        overflow_mm = overflow_px / CSS_PIXELS_PER_MM
        raise PageOverflowError(f"content is {overflow_mm:.1f} mm too tall to fit on one page")
