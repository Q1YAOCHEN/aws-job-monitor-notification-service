# AWS Setup Guide

This guide deploys the job monitor as a small AWS serverless application.

## 1. Create DynamoDB Table

Create a table:

```text
Table name: JobMonitorSeenJobs
Partition key: job_id
Type: String
```

Recommended settings:

```text
Capacity mode: On-demand
```

## 2. Create SNS Topic

Create an SNS topic:

```text
Name: job-monitor-alerts
Type: Standard
```

Create an email subscription and confirm it from your inbox.

## 3. Create Lambda Function

Create a Lambda function:

```text
Runtime: Python 3.11
Handler: lambda_function.lambda_handler
Memory: 256 MB
Timeout: 30 seconds
```

Set environment variables:

```text
DRY_RUN=false
DYNAMODB_TABLE=JobMonitorSeenJobs
SNS_TOPIC_ARN=<your SNS topic ARN>
KEYWORDS=software intern,ai intern,data analyst
LOCATIONS=boston,cambridge,remote
```

## 4. Add IAM Permissions

Attach permissions for:

- DynamoDB table read/write
- SNS publish
- CloudWatch Logs

Use `docs/iam_policy.json` as a starting point and replace:

```text
REGION
ACCOUNT_ID
```

## 5. Package and Upload

From the project root:

```bash
mkdir package
pip install -r requirements.txt -t package
copy src\*.py package\
Compress-Archive -Path package\* -DestinationPath deployment-package.zip -Force
```

Upload `deployment-package.zip` to Lambda.

## 6. Create EventBridge Schedule

Create an EventBridge rule or schedule:

```text
Schedule expression: rate(6 hours)
Target: your Lambda function
```

## 7. Test

Run a Lambda test event using `events/sample_event.json`.

Expected behavior:

- Lambda fetches job postings.
- Filters postings by configured keywords and locations.
- Stores unseen jobs in DynamoDB.
- Sends SNS email for new matches.
- Writes logs to CloudWatch.

## Notes

The included code uses a sample job source by default. Replace or extend `src/job_sources.py` with a real source that you are allowed to access, such as an approved API, internal feed, or public RSS source.
