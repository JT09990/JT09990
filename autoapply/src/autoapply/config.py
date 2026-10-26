import os
from dataclasses import dataclass, field
from pathlib import Path

import yaml

HOME = Path(os.environ.get("AUTOAPPLY_HOME", Path.home() / ".autoapply"))


@dataclass
class Profile:
    first_name: str
    last_name: str
    email: str
    phone: str
    resume_path: str


@dataclass
class Search:
    keywords: list[str]
    locations: list[str] = field(default_factory=lambda: ["Remote"])
    title_include: list[str] = field(default_factory=list)
    exclude: list[str] = field(default_factory=list)


@dataclass
class Limits:
    daily_cap: int = 15
    min_delay_seconds: float = 4
    max_delay_seconds: float = 11


@dataclass
class Config:
    profile: Profile
    search: Search
    limits: Limits
    sources: list[str]
    answers: dict[str, str]


def load(path: str | Path) -> Config:
    raw = yaml.safe_load(Path(path).expanduser().read_text())
    profile = Profile(**raw["profile"])
    profile.resume_path = str(Path(profile.resume_path).expanduser())
    return Config(
        profile=profile,
        search=Search(**raw["search"]),
        limits=Limits(**raw.get("limits", {})),
        sources=raw.get("sources", ["linkedin", "indeed"]),
        answers=raw.get("answers", {}),
    )
