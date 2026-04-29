from filters import JobPosting


def fetch_sample_jobs() -> list[JobPosting]:
    """Sample source for local dry-runs and Lambda test events."""
    return [
        JobPosting(
            job_id="sample-data-analyst-coop",
            title="Data Analyst Coop",
            company="Northstar Analytics Lab",
            location="Boston, MA",
            url="https://example.com/jobs/sample-data-analyst-coop",
            source="sample",
        ),
        JobPosting(
            job_id="deep-ai-agent-intern",
            title="AI Agent Engineer Intern",
            company="DEEP Measures",
            location="Cambridge, MA",
            url="https://example.com/jobs/deep-ai-agent-intern",
            source="sample",
        ),
        JobPosting(
            job_id="clear-lakes-software-intern",
            title="Software Development Intern",
            company="Clear Lakes Dental",
            location="Remote",
            url="https://example.com/jobs/clear-lakes-software-intern",
            source="sample",
        ),
        JobPosting(
            job_id="senior-sales-manager",
            title="Senior Sales Manager",
            company="Example Corp",
            location="New York, NY",
            url="https://example.com/jobs/senior-sales-manager",
            source="sample",
        ),
    ]


def fetch_jobs() -> list[JobPosting]:
    """Extend this function with approved APIs, RSS feeds, or internal job sources."""
    return fetch_sample_jobs()
