import os
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined
from markupsafe import Markup

from cv_builder.model import CV

TEMPLATE_NAME = "cv.html.j2"


def write_html(cv: CV, templates_dir: Path, assets_dir: Path, html_file: Path) -> None:
    """Links to stylesheets and assets are written relative to `html_file`."""

    def relative_url(target: Path) -> str:
        if not target.is_file():
            raise FileNotFoundError(target)
        return Path(os.path.relpath(target, html_file.parent)).as_posix()

    def inline_svg(asset: str) -> Markup:
        return Markup((assets_dir / asset).read_text(encoding="utf-8"))

    environment = Environment(
        loader=FileSystemLoader(templates_dir),
        autoescape=True,
        undefined=StrictUndefined,
        trim_blocks=True,
        lstrip_blocks=True,
    )
    environment.globals.update(
        asset_url=lambda asset: relative_url(assets_dir / asset),
        stylesheet_url=lambda stylesheet: relative_url(templates_dir / stylesheet),
        inline_svg=inline_svg,
    )

    html_file.parent.mkdir(parents=True, exist_ok=True)
    html_file.write_text(environment.get_template(TEMPLATE_NAME).render(cv=cv), encoding="utf-8")
