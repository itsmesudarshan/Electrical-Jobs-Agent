from dataclasses import dataclass, asdict

@dataclass
class Job:
    source: str
    title: str
    company: str = ""
    location: str = ""
    description: str = ""
    url: str = ""
    posted_date: str = ""
    deadline: str = ""
    category: str = ""
    experience: str = ""
    education: str = ""
    source_id: str = ""

    def to_dict(self):
        return asdict(self)
