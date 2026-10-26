from typing import Callable

from playwright.sync_api import Locator, Page

from ..answers import resolve
from ..config import Config

TEXT_FIELDS = "input[type=text], input[type=tel], input[type=email], input[type=number], textarea"


def _label(scope: Locator, field: Locator) -> str:
    aria = field.get_attribute("aria-label")
    if aria:
        return aria
    fid = field.get_attribute("id")
    if fid:
        label = scope.locator(f'label[for="{fid}"]')
        if label.count():
            return label.first.inner_text().strip()
    return field.get_attribute("name") or field.get_attribute("placeholder") or ""


def _builtin(label: str, cfg: Config) -> str | None:
    p, text = cfg.profile, label.lower()
    if "first name" in text:
        return p.first_name
    if "last name" in text:
        return p.last_name
    if "email" in text:
        return p.email
    if "phone" in text or "mobile" in text:
        return p.phone
    return None


def fill_text_fields(scope: Locator | Page, cfg: Config, ask: Callable[[str], str]) -> None:
    fields = scope.locator(TEXT_FIELDS)
    for i in range(fields.count()):
        field = fields.nth(i)
        if not field.is_visible() or field.input_value():
            continue
        label = _label(scope, field)
        if not label:
            continue
        value = _builtin(label, cfg)
        if value is None:
            value = resolve(label, cfg.answers, ask)
        field.fill(value)


def upload_resume(scope: Locator | Page, cfg: Config) -> None:
    upload = scope.locator("input[type=file]")
    if upload.count():
        upload.first.set_input_files(cfg.profile.resume_path)
