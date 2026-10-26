import time
from typing import Callable
from urllib.parse import quote_plus

from playwright.sync_api import Page

from ..config import Config
from ..models import Job
from . import forms
from .base import Source

MAX_STEPS = 12


class Indeed(Source):
    name = "indeed"
    login_url = "https://secure.indeed.com/auth"

    # Selectors track Indeed's current markup and will need maintenance.
    def search(self, page: Page, cfg: Config) -> list[Job]:
        jobs = []
        for kw in cfg.search.keywords:
            for loc in cfg.search.locations:
                page.goto(f"https://www.indeed.com/jobs?q={quote_plus(kw)}&l={quote_plus(loc)}")
                page.wait_for_selector("div.job_seen_beacon", timeout=15000)
                cards = page.locator("div.job_seen_beacon")
                for i in range(cards.count()):
                    card = cards.nth(i)
                    link = card.locator("a.jcs-JobTitle")
                    if not link.count():
                        continue
                    job_id = link.first.get_attribute("data-jk")
                    company = card.locator('[data-testid="company-name"]')
                    where = card.locator('[data-testid="text-location"]')
                    jobs.append(
                        Job(
                            source=self.name,
                            id=job_id,
                            title=link.first.inner_text().strip(),
                            company=company.first.inner_text().strip() if company.count() else "",
                            location=where.first.inner_text().strip() if where.count() else "",
                            url=f"https://www.indeed.com/viewjob?jk={job_id}",
                        )
                    )
        return jobs

    def fill(self, page: Page, job: Job, cfg: Config, ask: Callable[[str], str]) -> bool:
        page.goto(job.url)
        apply = page.locator("#indeedApplyButton, button[aria-label*='Apply now']")
        if not apply.count():
            return False
        apply.first.click()
        page.wait_for_url("**/smartapply.indeed.com/**", timeout=15000)
        for _ in range(MAX_STEPS):
            forms.upload_resume(page, cfg)
            forms.fill_text_fields(page, cfg, ask)
            if page.get_by_role("button", name="Submit your application").count():
                return True
            advance = page.get_by_role("button", name="Continue")
            if not advance.count():
                return False
            advance.first.click()
            time.sleep(1.5)
        return False

    def submit(self, page: Page) -> None:
        page.get_by_role("button", name="Submit your application").click()
