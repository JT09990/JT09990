import argparse
import random
import time

from . import store as st
from .browser import session
from .config import HOME, load
from .matcher import matches
from .sources import REGISTRY


def _ask(question: str) -> str:
    return input(f"  Form asks: {question}\n  Your answer: ").strip()


def cmd_login(args, cfg):
    with session() as ctx:
        page = ctx.new_page()
        page.goto(REGISTRY[args.source]().login_url)
        input(f"Log in to {args.source} in the browser window, then press Enter here... ")


def cmd_search(args, cfg):
    store = st.Store(HOME / "jobs.db")
    added = 0
    with session() as ctx:
        page = ctx.new_page()
        for name in cfg.sources:
            for job in REGISTRY[name]().search(page, cfg):
                if matches(job, cfg.search) and store.add(job):
                    added += 1
                    print(f"+ [{job.source}] {job.title} @ {job.company}")
    print(f"{added} new jobs queued")


def cmd_queue(args, cfg):
    for job in st.Store(HOME / "jobs.db").queued():
        print(f"[{job.source}] {job.title} @ {job.company} ({job.location})\n    {job.url}")


def cmd_stats(args, cfg):
    store = st.Store(HOME / "jobs.db")
    print(store.counts(), f"| applied today: {store.applied_today()}/{cfg.limits.daily_cap}")


def cmd_apply(args, cfg):
    store = st.Store(HOME / "jobs.db")
    with session() as ctx:
        page = ctx.new_page()
        for job in store.queued():
            if store.applied_today() >= cfg.limits.daily_cap:
                print("Daily cap reached, stopping.")
                return
            print(f"\n[{job.source}] {job.title} @ {job.company}\n  {job.url}")
            source = REGISTRY[job.source]()
            try:
                ready = source.fill(page, job, cfg, _ask)
            except Exception as exc:
                print(f"  could not complete the form: {exc}")
                store.set_status(job, st.FAILED)
                continue
            if not ready:
                print("  no automatable application found, marking failed")
                store.set_status(job, st.FAILED)
                continue
            choice = input("  Review the form in the browser. Submit? [y/N/q] ").strip().lower()
            if choice == "q":
                return
            if choice == "y":
                source.submit(page)
                store.set_status(job, st.APPLIED)
                print("  submitted")
            else:
                store.set_status(job, st.SKIPPED)
            time.sleep(random.uniform(cfg.limits.min_delay_seconds, cfg.limits.max_delay_seconds))


def main():
    parser = argparse.ArgumentParser(prog="autoapply")
    parser.add_argument("-c", "--config", default="config.yaml")
    sub = parser.add_subparsers(dest="cmd", required=True)
    login = sub.add_parser("login", help="log in to a site once in the tool's browser profile")
    login.add_argument("source", choices=sorted(REGISTRY))
    login.set_defaults(fn=cmd_login)
    for name, fn, help_ in [
        ("search", cmd_search, "find matching jobs and queue them"),
        ("queue", cmd_queue, "list queued jobs"),
        ("apply", cmd_apply, "fill queued applications, asking before each submit"),
        ("stats", cmd_stats, "show counts and today's cap"),
    ]:
        sub.add_parser(name, help=help_).set_defaults(fn=fn)
    args = parser.parse_args()
    args.fn(args, load(args.config))
