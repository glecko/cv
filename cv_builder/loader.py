from pathlib import Path
from string import Template

import yaml
from pydantic import TypeAdapter

from cv_builder.model import CV, GameReleasePlatform, Skill, StrictModel


def load_cv(data_dir: Path) -> CV:
    catalogues = {
        "stack": _load_catalogue(data_dir / "skills.yaml", Skill),
        "game_release_platforms": _load_catalogue(
            data_dir / "game_release_platforms.yaml", GameReleasePlatform
        ),
    }
    private_values = _read_private_values(data_dir / "private.yaml")
    cv_text = Template((data_dir / "cv.yaml").read_text(encoding="utf-8")).substitute(
        private_values
    )
    return CV.model_validate(yaml.safe_load(cv_text), context=catalogues)


def _read_private_values(file: Path) -> dict[str, str]:
    if not file.exists():
        raise FileNotFoundError(
            f"{file} not found; copy private.example.yaml to private.yaml and fill its values"
        )
    return TypeAdapter(dict[str, str]).validate_python(_read_yaml(file))


def _load_catalogue(file: Path, item_type: type[StrictModel]) -> dict[str, StrictModel]:
    return TypeAdapter(dict[str, item_type]).validate_python(_read_yaml(file))


def _read_yaml(file: Path) -> object:
    return yaml.safe_load(file.read_text(encoding="utf-8"))
