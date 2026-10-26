from autoapply.answers import resolve
from autoapply.config import Search
from autoapply.matcher import matches
from autoapply.models import Job
from autoapply.store import APPLIED, Store

JOB = Job("linkedin", "1", "Senior Python Developer", "Acme", "Remote", "http://x")


def test_matches_title_include():
    assert matches(JOB, Search(keywords=["x"], title_include=["python"]))
    assert not matches(JOB, Search(keywords=["x"], title_include=["java"]))


def test_matches_exclude_hits_title_company_description():
    assert not matches(JOB, Search(keywords=["x"], exclude=["acme"]))
    assert matches(JOB, Search(keywords=["x"], exclude=["intern"]))


def test_resolve_uses_pattern_before_asking():
    answers = {"years.*experience": "5"}
    assert resolve("How many Years of experience?", answers, lambda q: "ask") == "5"
    assert resolve("Favourite colour", answers, lambda q: "ask") == "ask"


def test_store_dedupes_and_tracks_status(tmp_path):
    store = Store(tmp_path / "jobs.db")
    assert store.add(JOB)
    assert not store.add(JOB)
    assert store.queued() == [JOB]
    store.set_status(JOB, APPLIED)
    assert store.queued() == []
    assert store.applied_today() == 1
