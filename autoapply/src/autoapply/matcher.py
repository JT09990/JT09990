from .config import Search
from .models import Job


def matches(job: Job, search: Search) -> bool:
    title = job.title.lower()
    if search.title_include and not any(t.lower() in title for t in search.title_include):
        return False
    haystack = f"{title} {job.company} {job.description}".lower()
    return not any(x.lower() in haystack for x in search.exclude)
