import time
from typing import Callable
from urllib.parse import quote_plus

from playwright.sync_api import Page

from ..config import Config
from ..models import Job
from . import forms
from .base import Source

MODAL = '[data-test-modal-id="easy-apply-modal"], .jobs-easy-apply-modal'
MAX_STEPS = 12


class LinkedIn(Source):
    name = "linkedin"
    login_url = "https://www.linkedin.com/login"

    # Selectors track LinkedIn's current markup and will need maintenance.
    def search(self, page: Page, cfg: Config) -> list[Job]:
        jobs = []
        for kw in cfg.search.keywords:
            for loc in cfg.search.locations:
                url = (
                    "https://www.linkedin.com/jobs/search/?f_AL=true"
                    f"&keywords={quote_plus(kw)}&location={quote_plus(loc)}"
                )
                page.goto(url)
                page.wait_for_selector("li[data-occludable-job-id]", timeout=15000)
                cards = page.locator("li[data-occludable-job-id]")
                for i in range(cards.count()):
                    card = cards.nth(i)
                    job_id = card.get_attribute("data-occludable-job-id")
                    title = card.locator("a.job-card-list__title, a.job-card-container__link")
                    company = card.locator(".artdeco-entity-lockup__subtitle")
                    where = card.locator(".artdeco-entity-lockup__caption")
                    jobs.append(
                        Job(
                            source=self.name,
                            id=job_id,
                            title=title.first.inner_text().strip() if title.count() else "",
                            company=company.first.inner_text().strip() if company.count() else "",
                            location=where.first.inner_text().strip() if where.count() else "",
                            url=f"https://www.linkedin.com/jobs/view/{job_id}/",
                        )
                    )
        return jobs

    def fill(self, page: Page, job: Job, cfg: Config, ask: Callable[[str], str]) -> bool:
        page.goto(job.url)
        button = page.locator("button.jobs-apply-button")
        if not button.count():
            return False
        button.first.click()
        modal = page.locator(MODAL)
        modal.wait_for(timeout=10000)
        for _ in range(MAX_STEPS):
            forms.upload_resume(modal, cfg)
            forms.fill_text_fields(modal, cfg, ask)
            if modal.locator('button[aria-label="Submit application"]').count():
                return True
            advance = modal.locator(
                'button[aria-label="Continue to next step"], button[aria-label="Review your application"]'
            )
            if not advance.count():
                return False
            advance.first.click()
            time.sleep(1.5)
        return False

    def submit(self, page: Page) -> None:
        page.locator('button[aria-label="Submit application"]').click()
