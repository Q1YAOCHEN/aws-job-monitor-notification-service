from filters import JobPosting


def format_job_message(jobs: list[JobPosting]) -> str:
    lines = ["New job matches found:", ""]
    for job in jobs:
        lines.extend(
            [
                f"{job.title} - {job.company}",
                f"Location: {job.location}",
                f"Source: {job.source}",
                f"URL: {job.url}",
                "",
            ]
        )
    return "\n".join(lines).strip()


class SnsNotifier:
    def __init__(self, topic_arn: str):
        import boto3

        self.topic_arn = topic_arn
        self.client = boto3.client("sns")

    def send(self, jobs: list[JobPosting]) -> None:
        if not jobs:
            return
        self.client.publish(
            TopicArn=self.topic_arn,
            Subject=f"Job Monitor: {len(jobs)} new match(es)",
            Message=format_job_message(jobs),
        )


class ConsoleNotifier:
    def send(self, jobs: list[JobPosting]) -> None:
        if not jobs:
            print("No new matches.")
            return
        print(format_job_message(jobs))
