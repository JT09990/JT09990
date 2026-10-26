import sqlite3
from pathlib import Path

from .models import Job

QUEUED, APPLIED, SKIPPED, FAILED = "queued", "applied", "skipped", "failed"

SCHEMA = """
CREATE TABLE IF NOT EXISTS jobs (
    source TEXT, id TEXT, title TEXT, company TEXT, location TEXT, url TEXT,
    status TEXT NOT NULL, updated_at TEXT NOT NULL DEFAULT (datetime('now')),
    PRIMARY KEY (source, id)
)
"""


class Store:
    def __init__(self, path: str | Path):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(path)
        self.db.execute(SCHEMA)

    def add(self, job: Job) -> bool:
        cur = self.db.execute(
            "INSERT OR IGNORE INTO jobs (source, id, title, company, location, url, status) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (job.source, job.id, job.title, job.company, job.location, job.url, QUEUED),
        )
        self.db.commit()
        return cur.rowcount == 1

    def queued(self) -> list[Job]:
        rows = self.db.execute(
            "SELECT source, id, title, company, location, url FROM jobs "
            "WHERE status = ? ORDER BY rowid",
            (QUEUED,),
        )
        return [Job(*r) for r in rows]

    def set_status(self, job: Job, status: str) -> None:
        self.db.execute(
            "UPDATE jobs SET status = ?, updated_at = datetime('now') WHERE source = ? AND id = ?",
            (status, job.source, job.id),
        )
        self.db.commit()

    def applied_today(self) -> int:
        return self.db.execute(
            "SELECT COUNT(*) FROM jobs WHERE status = ? AND date(updated_at) = date('now')",
            (APPLIED,),
        ).fetchone()[0]

    def counts(self) -> dict[str, int]:
        return dict(self.db.execute("SELECT status, COUNT(*) FROM jobs GROUP BY status"))
