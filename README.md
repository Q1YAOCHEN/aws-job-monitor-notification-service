# AWS Job Monitor Notification Service

Serverless job-monitoring service that checks job postings on a schedule, stores previously seen postings in DynamoDB, and sends email notifications for new matches through Amazon SNS.

This project is designed as a practical AWS backend portfolio project for job-search automation, serverless architecture, and cloud deployment practice.

## Architecture

```text
EventBridge Schedule
        |
        v
AWS Lambda job_monitor_handler
        |
        +-- Fetch job sources from config
        +-- Filter postings by keywords and location
        +-- Store/check seen jobs in DynamoDB
        +-- Publish new matches to SNS
        |
        v
CloudWatch Logs
```

## AWS Services

- AWS Lambda
- Amazon EventBridge Scheduler
- Amazon DynamoDB
- Amazon SNS
- Amazon CloudWatch Logs
- IAM roles and policies

## Features

- Scheduled serverless job monitoring
- Keyword and location filtering
- DynamoDB-based deduplication
- SNS email notification for new job matches
- Local dry-run mode for development
- Clear deployment and IAM setup documentation

## Repository Structure

```text
src/
  lambda_function.py       Lambda handler and local runner
  job_sources.py           Job source fetchers and sample data source
  storage.py               DynamoDB persistence wrapper
  notifier.py              SNS notification wrapper
  filters.py               Keyword/location filtering
events/
  sample_event.json        Example Lambda test event
docs/
  aws_setup.md             Step-by-step AWS setup guide
  iam_policy.json          Minimal IAM policy example
requirements.txt           Python dependencies
.env.example               Local environment variable template
```

## Local Dry Run

Create a virtual environment and install dependencies:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Run in dry-run mode:

```bash
set DRY_RUN=true
set KEYWORDS=software intern,ai intern,data analyst
set LOCATIONS=boston,cambridge,remote
python src/lambda_function.py
```

Dry-run mode uses sample job postings and prints matches without requiring AWS credentials.

## AWS Deployment Overview

1. Create a DynamoDB table named `JobMonitorSeenJobs`.
2. Create an SNS topic and subscribe your email.
3. Create a Lambda function using Python 3.11.
4. Upload the `src/` code and dependencies.
5. Configure environment variables.
6. Attach IAM permissions from `docs/iam_policy.json`.
7. Add an EventBridge schedule to run the Lambda periodically.

Detailed instructions are in [docs/aws_setup.md](docs/aws_setup.md).

## Example Environment Variables

```text
DRY_RUN=false
DYNAMODB_TABLE=JobMonitorSeenJobs
SNS_TOPIC_ARN=arn:aws:sns:us-east-1:123456789012:job-monitor-alerts
KEYWORDS=software intern,ai intern,data analyst
LOCATIONS=boston,cambridge,remote
```

## Resume Bullet

```text
AWS Job Monitor Notification Service
• Built a serverless job-monitoring service using AWS Lambda, EventBridge, DynamoDB, SNS, and CloudWatch.
• Implemented scheduled job checks, keyword/location filtering, DynamoDB deduplication, and email notifications for new matches.
```
