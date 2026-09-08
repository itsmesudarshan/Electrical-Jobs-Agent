import hashlib, re, time, requests
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "NepalElectricalJobsAgent/1.0 (personal vacancy monitoring)"}

def fetch(url, timeout=25):
    r = requests.get(url, headers=HEADERS, timeout=timeout)
    r.raise_for_status()
    return r.text

def clean(text):
    return re.sub(r"\s+", " ", text or "").strip()

def job_key(job):
    raw = "|".join([job.source.lower(), job.source_id or "", job.title.lower(), job.company.lower(), job.url.lower()])
    return hashlib.sha256(raw.encode()).hexdigest()

def polite_sleep(seconds):
    if seconds > 0:
        time.sleep(seconds)
