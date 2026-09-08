from urllib.parse import urljoin
from bs4 import BeautifulSoup
from app.models import Job
from app.utils import fetch, clean

BASE = "https://nea.org.np"
URL = "https://nea.org.np/en/recruitment/open"
KEYWORDS = ("electrical","electric","electronics","power","engineer","hydropower","energy","electro-mechanical","supervisor")

def collect():
    soup = BeautifulSoup(fetch(URL), "html.parser")
    jobs, seen = [], set()
    for a in soup.find_all("a", href=True):
        title = clean(a.get_text(" ", strip=True))
        href = urljoin(BASE, a["href"])
        if len(title) < 8 or "/recruitment/" not in href:
            continue
        if not any(k in title.lower() for k in KEYWORDS):
            continue
        key = (title.lower(), href)
        if key in seen:
            continue
        seen.add(key)
        jobs.append(Job(source="NEA", title=title, company="Nepal Electricity Authority",
                        url=href, category="Government / Electricity", source_id=href))
    return jobs
