from abc import ABC, abstractmethod
from typing import Callable

from playwright.sync_api import Page

from ..config import Config
from ..models import Job


class Source(ABC):
    name: str
    login_url: str

    @abstractmethod
    def search(self, page: Page, cfg: Config) -> list[Job]: ...

    @abstractmethod
    def fill(self, page: Page, job: Job, cfg: Config, ask: Callable[[str], str]) -> bool:
        """Open the application and fill it in. True when it is ready to submit."""

    @abstractmethod
    def submit(self, page: Page) -> None: ...
