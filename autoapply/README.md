# autoapply

Finds jobs on LinkedIn and Indeed, fills the application forms in your own logged-in browser, and waits for your approval before every submit.

## Setup

```
pip install -e '.[dev]'
playwright install chromium
cp config.example.yaml config.yaml   # edit it
autoapply login linkedin             # log in by hand once; no credentials are stored
autoapply login indeed
```

## Use

```
autoapply search    # scrape listings, filter, queue new ones
autoapply queue     # see what is queued
autoapply apply     # fill each form, then ask: submit? [y/N/q]
autoapply stats
```

Form questions that match a regex in `answers` are filled automatically; anything else is asked in the terminal. State lives in `~/.autoapply` (override with `AUTOAPPLY_HOME`).

## Caveats

- LinkedIn and Indeed prohibit automated access in their terms, and LinkedIn restricts accounts for it. Use at your own risk; keep `daily_cap` low.
- Site selectors were written from known markup and have not been run against the live sites. Expect to adjust them in `sources/linkedin.py` and `sources/indeed.py`.
- Only text fields and resume upload are filled. Dropdowns, radios and checkboxes are left for you to complete during review.
