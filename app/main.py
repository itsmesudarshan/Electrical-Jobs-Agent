import argparse
from datetime import datetime, timezone
from app.config import SETTINGS, PROFILE
from app.sources import nea, nepal_impact, jobsnepal, kumarijob
from app.scoring import score
from app.state import load, save, mark_seen
from app.telegram import send
from app.utils import job_key, polite_sleep

def collect_all():
    jobs = []
    enabled = SETTINGS["sources"]
    collectors = []
    if enabled.get("nea"): collectors.append(("NEA", nea.collect))
    if enabled.get("nepal_impact"): collectors.append(("Nepal Impact", nepal_impact.collect))
    if enabled.get("jobsnepal"): collectors.append(("JobsNepal", jobsnepal.collect))
    if enabled.get("kumarijob"): collectors.append(("Kumari Job", kumarijob.collect))

    for name, collector in collectors:
        try:
            found = collector()
            print(f"[{name}] found {len(found)} candidate(s)")
            jobs.extend(found)
        except Exception as e:
            print(f"[{name}] ERROR: {type(e).__name__}: {e}")
        polite_sleep(SETTINGS["http"]["delay_between_requests_seconds"])

    unique = {}
    for job in jobs:
        unique[job_key(job)] = job
    return list(unique.values())

def format_message(job, score_value, reasons):
    lines = [
        f"🔔 NEW ELECTRICAL JOB — {score_value}/100", "",
        f"💼 {job.title}", f"🏢 {job.company or 'Not stated'}",
        f"📍 {job.location or 'Nepal / not stated'}",
        f"📚 {job.education or 'See vacancy'}",
        f"🧑‍💻 {job.experience or 'Not stated'}",
        f"📅 Deadline: {job.deadline or 'See vacancy'}",
        f"🌐 Source: {job.source}", "", "Assessment:"
    ]
    lines += [f"✅ {r}" for r in reasons[:5]]
    if job.url: lines += ["", f"🔗 {job.url}"]
    return "\n".join(lines)

def run(dry_run=False):
    state = load()
    jobs = collect_all()
    notified = 0
    minimum = max(SETTINGS["notification"]["minimum_score"], PROFILE["minimum_notification_score"])

    for job in jobs:
        key = job_key(job)
        value, reasons = score(job, PROFILE)
        if key in state.get("seen", {}):
            continue

        mark_seen(state, key, job)
        if value < minimum:
            continue

        message = format_message(job, value, reasons)
        print("\n" + message + "\n")
        if not dry_run:
            try:
                send(message)
                notified += 1
            except Exception as e:
                print(f"Telegram ERROR: {type(e).__name__}: {e}")

    state["last_run"] = datetime.now(timezone.utc).isoformat()
    save(state)
    print(f"Checked: {len(jobs)} | new notifications: {notified}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    run(dry_run=parser.parse_args().dry_run)
