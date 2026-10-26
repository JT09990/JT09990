from dataclasses import dataclass


@dataclass
class Job:
    source: str
    id: str
    title: str
    company: str
    location: str
    url: str
    description: str = ""
