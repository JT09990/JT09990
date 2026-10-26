import re
from typing import Callable


def resolve(question: str, answers: dict[str, str], ask: Callable[[str], str]) -> str:
    for pattern, value in answers.items():
        if re.search(pattern, question, re.I):
            return value
    return ask(question)
