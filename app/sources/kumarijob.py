from urllib.parse import urljoin
from bs4 import BeautifulSoup
from app.models import Job
from app.utils import fetch, clean

# Opt-in. Review current access terms before enabling.
SEARCH_URLS = [
    "https://www.kumarijob.com/search?search=electrical",
    "https://www.kumarijob.com/search?search=electrical%20engineer"
]

def collect():
    jobs, seen = [], set()
    for url in SEARCH_URLS:
        soup = BeautifulSoup(fetch(url), "html.parser")
        for a in soup.find_all("a", href=True):
            title = clean(a.get_text(" ", strip=True))
            href = urljoin("https://www.kumarijob.com", a["href"])
            if len(title) < 8 or not any(x in title.lower() for x in ("electrical","electronics","power","energy","engineer")):
                continue
            if href in seen:
                continue
            seen.add(href)
            jobs.append(Job(source="Kumari Job", title=title, url=href, source_id=href))
    return jobs
