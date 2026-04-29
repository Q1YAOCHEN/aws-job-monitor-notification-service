from datetime import datetime, timezone

from filters import JobPosting


class SeenJobStore:
    def __init__(self, table_name: str):
        import boto3

        self.table = boto3.resource("dynamodb").Table(table_name)

    def has_seen(self, job_id: str) -> bool:
        response = self.table.get_item(Key={"job_id": job_id})
        return "Item" in response

    def mark_seen(self, job: JobPosting) -> bool:
        from botocore.exceptions import ClientError

        item = {
            "job_id": job.job_id,
            "title": job.title,
            "company": job.company,
            "location": job.location,
            "url": job.url,
            "source": job.source,
            "seen_at": datetime.now(timezone.utc).isoformat(),
        }
        try:
            self.table.put_item(
                Item=item,
                ConditionExpression="attribute_not_exists(job_id)",
            )
            return True
        except ClientError as exc:
            if exc.response.get("Error", {}).get("Code") == "ConditionalCheckFailedException":
                return False
            raise


class MemorySeenJobStore:
    def __init__(self):
        self.seen: set[str] = set()

    def has_seen(self, job_id: str) -> bool:
        return job_id in self.seen

    def mark_seen(self, job: JobPosting) -> bool:
        if job.job_id in self.seen:
            return False
        self.seen.add(job.job_id)
        return True
