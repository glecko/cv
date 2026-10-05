from typing import Self

from pydantic import BaseModel, ConfigDict, ValidationInfo, field_validator


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class Skill(StrictModel):
    name: str
    icon: str


class GameReleasePlatform(StrictModel):
    name: str
    icon: str
    label: str = ""


class ContactChannel(StrictModel):
    icon: str
    text: str
    url: str


class Language(StrictModel):
    name: str
    level: str
    flag: str


class TimelineItem(StrictModel):
    period: str
    description: str | None = None
    stack: list[Skill] = []
    game_release_platforms: list[GameReleasePlatform] = []
    visible: bool = True
    collapsed: bool = False

    @field_validator("stack", "game_release_platforms", mode="before")
    @classmethod
    def resolve_tags(cls, tags: list[str], info: ValidationInfo) -> list[StrictModel]:
        catalogue: dict[str, StrictModel] = info.context[info.field_name]
        unknown_tags = [tag for tag in tags if tag not in catalogue]
        if unknown_tags:
            raise ValueError(f"unknown {info.field_name} tags: {unknown_tags}")
        return [catalogue[tag] for tag in tags]

    @classmethod
    def only_visible(cls, items: list[Self]) -> list[Self]:
        return [item for item in items if item.visible]


class Project(TimelineItem):
    name: str
    client: str | None = None
    logo: str | None = None


class Entry(TimelineItem):
    title: str
    organization: str | None = None
    location: str | None = None
    logo: str | None = None
    projects: list[Project] = []

    @field_validator("projects")
    @classmethod
    def drop_hidden_projects(cls, projects: list[Project]) -> list[Project]:
        return Project.only_visible(projects)


class Section(StrictModel):
    title: str
    icon: str
    extra_css_classes: list[str] = []
    entries: list[Entry]

    @field_validator("entries")
    @classmethod
    def drop_hidden_entries(cls, entries: list[Entry]) -> list[Entry]:
        return Entry.only_visible(entries)


class CV(StrictModel):
    name: str
    title: str
    photo: str
    profile: list[str]
    contact: list[ContactChannel]
    languages: list[Language]
    sections: list[Section]
