from urllib.parse import urljoin
from bs4 import BeautifulSoup
from app.models import Job
from app.utils import fetch, clean

BASE = "https://nea.org.np"
URL = "https://nea.org.np/en/recruitment/open"
FIELD_TERMS = ("electrical", "electronics", "power", "engineer", "hydropower", "energy", "electro-mechanical", "electromechanical", "supervisor")
EXCLUDE_TERMS = ("result", "exam center", "examination schedule", "interview examination", "approved candidate", "merit order", "equivalent certificate")

def collect():
    soup = BeautifulSoup(fetch(URL), "html.parser")
    jobs, seen = [], set()
    links = []
    for a in soup.find_all("a", href=True):
        title = clean(a.get_text(" ", strip=True))
        href = urljoin(BASE, a["href"])
        low = (title + " " + href).lower()
        if "/en/recruitment/open/advertisements/" not in href:
            continue
        if any(term in low for term in EXCLUDE_TERMS):
            continue
        if (title.lower(), href) not in seen:
            seen.add((title.lower(), href))
            links.append((title, href))

    for title, href in links:
        try:
            detail = BeautifulSoup(fetch(href), "html.parser")
            body = clean(detail.get_text(" ", strip=True))
        except Exception:
            body = title
        text = f"{title} {body}".lower()
        if not any(term in text for term in FIELD_TERMS):
            continue
        jobs.append(Job(
            source="NEA", title=title, company="Nepal Electricity Authority",
            url=href, category="Government / Electricity", description=body,
            source_id=href
        ))
    return jobs
