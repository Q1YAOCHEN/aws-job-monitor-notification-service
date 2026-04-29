from dataclasses import dataclass


@dataclass(frozen=True)
class JobPosting:
    job_id: str
    title: str
    company: str
    location: str
    url: str
    source: str


def parse_csv_env(value: str | None) -> list[str]:
    if not value:
        return []
    return [item.strip().lower() for item in value.split(",") if item.strip()]


def matches_filters(job: JobPosting, keywords: list[str], locations: list[str]) -> bool:
    title = job.title.lower()
    company = job.company.lower()
    location = job.location.lower()

    keyword_match = not keywords or any(keyword in title or keyword in company for keyword in keywords)
    location_match = not locations or any(place in location for place in locations)

    return keyword_match and location_match
