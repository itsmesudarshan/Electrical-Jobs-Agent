import requests
from app.models import Job

URL = "https://nepalimpact.org/api/v1/opportunities"

def collect():
    r = requests.get(URL, params={"limit": 200, "offset": 0}, timeout=25)
    r.raise_for_status()
    payload = r.json()
    jobs = []
    for item in payload.get("data", []):
        text = " ".join(str(item.get(k, "")) for k in ("title","description","category","sector","location")).lower()
        terms = ("electrical","energy","solar","renewable","hydropower","power","engineer","engineering","electromechanical")
        if not any(t in text for t in terms):
            continue
        jobs.append(Job(
            source="Nepal Impact",
            title=str(item.get("title") or item.get("name") or "Untitled opportunity"),
            company=str(item.get("organization") or item.get("source") or ""),
            location=str(item.get("location") or ""),
            description=str(item.get("description") or ""),
            url=str(item.get("url") or item.get("source_url") or item.get("link") or ""),
            posted_date=str(item.get("published_at") or item.get("posted_date") or ""),
            deadline=str(item.get("deadline") or ""),
            category=str(item.get("category") or ""),
            source_id=str(item.get("id") or "")
        ))
    return jobs
