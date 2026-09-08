import requests
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from app.models import Job

URL = "https://nepalimpact.org/api/v1/opportunities"
FIELD_TERMS = ("electrical", "electronics", "power system", "power engineering", "hydropower", "renewable energy", "solar", "energy engineer", "electro-mechanical", "electromechanical", "instrumentation", "automation", "plc", "control engineer", "electrical engineer")

def _expired(value):
    if not value:
        return False
    text = str(value).strip()
    candidates = [
        "%Y-%m-%d", "%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%dT%H:%M:%S.%f%z",
        "%Y-%m-%dT%H:%M:%S", "%d/%m/%Y", "%m/%d/%Y"
    ]
    dt = None
    for fmt in candidates:
        try:
            dt = datetime.strptime(text, fmt)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            break
        except ValueError:
            pass
    if dt is None:
        try:
            dt = parsedate_to_datetime(text)
        except Exception:
            return False
    return dt < datetime.now(dt.tzinfo)

def collect():
    r = requests.get(URL, params={"limit": 200, "offset": 0, "type": "job"}, timeout=25)
    r.raise_for_status()
    payload = r.json()
    jobs = []
    for item in payload.get("data", []):
        deadline = str(item.get("deadline") or "").strip()
        if _expired(deadline):
            continue
        text = " ".join(str(item.get(k, "")) for k in ("title", "description", "category", "sector", "location", "type")).lower()
        if not any(t in text for t in FIELD_TERMS):
            continue
        jobs.append(Job(
            source="Nepal Impact",
            title=str(item.get("title") or item.get("name") or "Untitled opportunity"),
            company=str(item.get("organization") or item.get("source") or ""),
            location=str(item.get("location") or ""),
            description=str(item.get("description") or ""),
            url=str(item.get("url") or item.get("source_url") or item.get("link") or ""),
            posted_date=str(item.get("published_at") or item.get("posted_date") or ""),
            deadline=deadline,
            category=str(item.get("category") or ""),
            source_id=str(item.get("id") or "")
        ))
    return jobs
