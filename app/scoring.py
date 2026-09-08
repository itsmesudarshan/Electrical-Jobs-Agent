import re

FIELD_TERMS = [
    "electrical","electronics","power system","power engineering","hydropower",
    "renewable energy","solar","electro-mechanical","electromechanical",
    "automation","plc","instrumentation","control system","electrical design",
    "electrical maintenance","epc","substation","transmission","distribution"
]
NEGATIVE_TERMS = ["civil engineer","software engineer","frontend","backend","marketing","accountant","human resources","sales executive"]
ENTRY_TERMS = ["entry level","entry-level","fresh graduate","fresher","trainee","junior","graduate","0-2 years","0-1 year","no experience"]

def _years(text):
    nums = [int(m.group(1)) for m in re.finditer(r"(\d+)\s*\+?\s*(?:years?|yrs?)", text.lower())]
    return max(nums) if nums else None

def score(job, profile):
    text = " ".join([job.title, job.description, job.category, job.experience, job.education, job.location]).lower()
    score, reasons = 0, []
    hits = [x for x in FIELD_TERMS if x in text]
    score += min(40, len(set(hits)) * 6)
    if hits: reasons.append("Electrical/power/energy relevance detected")

    if any(x in text for x in ("electrical engineering","electronics engineering","electrical & electronics","b.e. electrical","be electrical")):
        score += 20
        reasons.append("Electrical/Electronics engineering education appears relevant")

    if any(x in text for x in ENTRY_TERMS):
        score += 20
        reasons.append("Entry-level/fresh-graduate language detected")

    exp = _years(text)
    if exp is None:
        score += 10
    elif exp <= profile["maximum_preferred_experience_years"]:
        score += 15
        reasons.append(f"Experience appears within target ({exp} year(s))")
    elif exp <= profile["maximum_preferred_experience_years"] + 2:
        score += 7
        reasons.append(f"Experience slightly above target ({exp} year(s))")
    else:
        score -= 10
        reasons.append(f"Experience appears high ({exp} year(s))")

    if any(x.lower() in text for x in profile["preferred_locations"]):
        score += 5
        reasons.append("Preferred Nepal location detected")

    if any(x in text for x in NEGATIVE_TERMS):
        score -= 25
        reasons.append("Strong non-electrical signal detected")

    return max(0, min(100, score)), reasons
