from urllib.parse import urljoin
from bs4 import BeautifulSoup
from app.models import Job
from app.utils import fetch, clean

# Opt-in. Review current access terms before enabling.
SEARCH_URLS = [
    "https://www.jobsnepal.com/search?searchword=Electrical%20Engineer",
    "https://www.jobsnepal.com/search?searchword=Electrical",
    "https://www.jobsnepal.com/search?searchword=Power%20Engineer"
]

def collect():
    jobs, seen = [], set()
    for url in SEARCH_URLS:
        soup = BeautifulSoup(fetch(url), "html.parser")
        for a in soup.find_all("a", href=True):
            title = clean(a.get_text(" ", strip=True))
            href = urljoin("https://www.jobsnepal.com", a["href"])
            if len(title) < 8 or not any(x in title.lower() for x in ("electrical","power engineer","electronics","energy")):
                continue
            if href in seen:
                continue
            seen.add(href)
            jobs.append(Job(source="JobsNepal", title=title, url=href, source_id=href))
    return jobs
