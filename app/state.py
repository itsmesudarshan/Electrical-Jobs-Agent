import json
from datetime import datetime, timezone
from app.config import STATE_PATH

def load():
    if not STATE_PATH.exists():
        return {"seen": {}, "last_run": None}
    try:
        return json.loads(STATE_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {"seen": {}, "last_run": None}

def save(state):
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")

def mark_seen(state, key, job):
    state.setdefault("seen", {})[key] = {
        "title": job.title, "company": job.company, "source": job.source,
        "url": job.url, "seen_at": datetime.now(timezone.utc).isoformat()
    }
