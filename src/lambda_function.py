import json
import os
from typing import Any

from filters import JobPosting, matches_filters, parse_csv_env
from job_sources import fetch_jobs
from notifier import ConsoleNotifier, SnsNotifier
from storage import MemorySeenJobStore, SeenJobStore


def is_dry_run(event: dict[str, Any] | None = None) -> bool:
    event = event or {}
    env_value = os.getenv("DRY_RUN", "false").lower()
    return bool(event.get("dry_run")) or env_value in {"1", "true", "yes"}


def get_store(dry_run: bool):
    if dry_run:
        return MemorySeenJobStore()

    table_name = os.environ["DYNAMODB_TABLE"]
    return SeenJobStore(table_name)


def get_notifier(dry_run: bool):
    if dry_run:
        return ConsoleNotifier()

    topic_arn = os.environ["SNS_TOPIC_ARN"]
    return SnsNotifier(topic_arn)


def find_new_matches(jobs: list[JobPosting], store, keywords: list[str], locations: list[str]) -> list[JobPosting]:
    matches = []
    for job in jobs:
        if not matches_filters(job, keywords=keywords, locations=locations):
            continue
        if store.mark_seen(job):
            matches.append(job)
    return matches


def lambda_handler(event: dict[str, Any] | None, context: Any) -> dict[str, Any]:
    dry_run = is_dry_run(event)
    keywords = parse_csv_env(os.getenv("KEYWORDS", "software intern,ai intern,data analyst"))
    locations = parse_csv_env(os.getenv("LOCATIONS", "boston,cambridge,remote"))

    store = get_store(dry_run)
    notifier = get_notifier(dry_run)

    jobs = fetch_jobs()
    new_matches = find_new_matches(jobs, store=store, keywords=keywords, locations=locations)
    notifier.send(new_matches)

    response = {
        "dry_run": dry_run,
        "jobs_checked": len(jobs),
        "new_matches": len(new_matches),
        "matches": [job.__dict__ for job in new_matches],
    }
    print(json.dumps(response, indent=2))
    return response


if __name__ == "__main__":
    result = lambda_handler({"dry_run": True}, None)
    print(json.dumps(result, indent=2))
