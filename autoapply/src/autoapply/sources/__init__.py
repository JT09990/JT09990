from .base import Source
from .indeed import Indeed
from .linkedin import LinkedIn

REGISTRY: dict[str, type[Source]] = {"linkedin": LinkedIn, "indeed": Indeed}
