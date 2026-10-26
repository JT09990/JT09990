from contextlib import contextmanager

from playwright.sync_api import sync_playwright

from .config import HOME


@contextmanager
def session():
    # Persistent profile: you log in once by hand, no credentials are stored by this tool.
    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(str(HOME / "browser-profile"), headless=False)
        try:
            yield ctx
        finally:
            ctx.close()
