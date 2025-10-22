# 🧠 ETL Automation Project

This project automates the extraction, transformation, and loading (ETL) of data from multiple sources into Google Cloud Platform (GCP), using **Cloud Run**, **Workload Identity Federation**, and **GitHub Actions**.

---

## 🚀 Overview

The ETL pipeline:
1. Extracts data from internal & external APIs.
2. Transforms and cleans it using Python (Pandas / BigQuery / Dataflow-ready scripts).
3. Loads the processed data into **BigQuery** and triggers further reporting processes.

Deployment and authentication are handled through **GitHub Actions** and **Workload Identity Federation (WIF)** — eliminating the need for static service account keys.

---

## 🧩 Architecture


| Component | Description |
|------------|-------------|
| **GitHub Actions** | CI/CD pipeline that triggers the ETL job deployment or run |
| **Workload Identity Federation (WIF)** | Secure authentication from GitHub to GCP without service account keys |
| **Cloud Run Job** | Executes the ETL code in a serverless container environment |
| **BigQuery** | Stores and aggregates the transformed data |
| **Cloud Storage** | Optional: stores raw data dumps or intermediate results |

---

## ⚙️ Prerequisites

Before proceeding, ensure you have:

- A **Google Cloud Project** 
- **Owner** or **Editor** IAM access to create pools, providers, and service accounts
- A **GitHub repository** (e.g., `mpfouziya/End-to-End-ETL-using-Google-Workflows`)
- Installed the **gcloud CLI** locally (if configuring via terminal)

---

## 🧰 1. Create a Service Account


This service account will execute the ETL process inside Cloud Run.

```bash
gcloud iam service-accounts create <GITHUB_DEPLOYER_SERVICE_ACCOUNT> \
  --project="<PROJECT_ID>" \
  --display-name="GitHub Deployer" 
```
Grant necessary roles

```bash
gcloud projects add-iam-policy-binding <PROJECT_ID> \
  --member="serviceAccount:<GITHUB_DEPLOYER_SERVICE_ACCOUNT>@<PROJECT_ID>.iam.gserviceaccount.com" \
  --role="roles/run.admin"

gcloud projects add-iam-policy-binding <PROJECT_ID> \
  --member="serviceAccount:<GITHUB_DEPLOYER_SERVICE_ACCOUNT>@<PROJECT_ID>.iam.gserviceaccount.com" \
  --role="roles/iam.serviceAccountUser"
```
## 🔐 Step 2 — Configure Workload Identity Federation (WIF)

2.1 Create a Workload Identity Pool

```bash
gcloud iam workload-identity-pools create <POOL_NAME> \
  --project="<PROJECT_ID>" \
  --location="global" \
  --display-name="GitHub Actions Pool"
```

2.2 Create an OIDC Provider for GitHub

```bash
gcloud iam workload-identity-pools providers create-oidc <PROVIDER_NAME> \
  --project="<PROJECT_ID>" \
  --location="global" \
  --workload-identity-pool=<POOL_NAME>  \
  --display-name="GitHub Provider" \
  --issuer-uri="https://token.actions.githubusercontent.com" \
  --attribute-mapping="google.subject=assertion.sub,attribute.repository=assertion.repository" \
  --attribute-condition="assertion.repository == '<GITHUB_USERNAME>/<REPO_NAME>'"
```

2.3 Bind GitHub Repository to Service Account

```bash
gcloud iam service-accounts add-iam-policy-binding \
  <GITHUB_DEPLOYER_SERVICE_ACCOUNT>@<PROJECT_ID>.iam.gserviceaccount.com \
  --role="roles/iam.workloadIdentityUser" \
  --member="principalSet://iam.googleapis.com/projects/<PROJECT_NUMBER>/locations/global/workloadIdentityPools/<POOL_NAME>/attribute.repository/<GITHUB_USERNAME>/<REPO_NAME>"
```

## ⚡ Step 3 — Setup GitHub Actions

Create the file:
.github/workflows/deploy.yml

## 🧩 Step 4 — (Optional) Trigger ETL Job
```bash
    gcloud run jobs execute <CLOUD_RUN_JOB_NAME> \
      --region=${{ env.REGION }} \
      --project=${{ env.PROJECT_ID }}
```
✅ Verification

After pushing to main, go to GitHub → Actions → Deploy ETL to Cloud Run → Run workflow.

Expected outcomes:
- Successful authentication via OIDC
- Cloud Run job deployed
- Job visible under GCP Console → Cloud Run → Jobs

## 🕒 Step 5 - Scheduling the ETL Job (via Google Cloud Workflows)

Once your ETL Python job is deployed to Cloud Run, you can automate its execution using Google Workflows and Cloud Scheduler.
This approach keeps scheduling entirely on GCP — no need for GitHub cron triggers.
5.1 Create a Workflow

In your Google Cloud Console, go to
Navigation Menu → Workflows → Create Workflow
Name it something like <ETL_WORKFLOW_NAME> (e.g., etl-runner-workflow).
Set the schedule for the trigger.
Write the workflow to run the cloud run jobs one after the other if the result of one job influence the next ETL.
Example for Google Workflow YAML definition for Event & First Touch Event job:
```bash
main:
  steps:
    - run_event:
        try:
          call: http.post
          args:
            url: https://run.googleapis.com/v2/projects/<PROJECT_ID>/locations/<GCP_REGION>/jobs/event:run
            auth:
              type: OAuth2
            body: {}
          result: event_response
        retry:
          predicate: ${http.default_retry_predicate}
          max_retries: 3
          backoff:
            initial_delay: 5
            max_delay: 30
            multiplier: 2
        except:
          as: e
          steps:
            - log_event_error:
                call: sys.log
                args:
                  text: ${"Failed to start event job: " + e.message}
                  severity: "ERROR"
            - return_event_error:
                return: ${"Workflow failed at event job step: " + e.message}

    - wait_event:
        call: wait_for_job
        args:
          operation_name: ${event_response.body.name}

    - run_first_touch_event:
        try:
          call: http.post
          args:
            url: https://run.googleapis.com/v2/projects/<PROJECT_ID>/locations/<GCP_REGION>/jobs/first-touch-event:run
            auth:
              type: OAuth2
            body: {}
          result: fte_response
        retry:
          predicate: ${http.default_retry_predicate}
          max_retries: 3
          backoff:
            initial_delay: 5
            max_delay: 30
            multiplier: 2
        except:
          as: e
          steps:
            - log_fte_error:
                call: sys.log
                args:
                  text: ${"Failed to start first-touch-event job: " + e.message}
                  severity: "ERROR"
            - return_fte_error:
                return: ${"Workflow failed at first-touch-event job step: " + e.message}

    - wait_first_touch_event:
        call: wait_for_job
        args:
          operation_name: ${fte_response.body.name}

# Helper subworkflow to wait for job completion
wait_for_job:
  params: [operation_name]
  steps:
    - poll:
        try:
          call: http.get
          args:
            url: ${"https://run.googleapis.com/v2/" + operation_name}
            auth:
              type: OAuth2
          result: status
        except:
          as: e
          steps:
            - log_poll_error:
                call: sys.log
                args:
                  text: ${"Polling failed for " + operation_name + ": " + e.message}
                  severity: "ERROR"
            - return_poll_error:
                return: ${"Polling failed: " + e.message}

    - check:
        switch:
          - condition: ${"done" in status.body and status.body.done == true}
            return: ${status.body}

    - sleep:
        call: sys.sleep
        args:
          seconds: 10

    - repeat:
        next: poll


```
This ensures your workflow triggers the Cloud Run job and waits until it finishes before continuing to any downstream steps (like sending notifications, updating BigQuery, or calling another service).

## 📚 References

[Google Cloud Workload Identity Federation](https://cloud.google.com/iam/docs/workload-identity-federation)

[GitHub Actions OIDC for GCP](https://github.com/google-github-actions/auth)

[Cloud Run Jobs Documentation](https://cloud.google.com/run/docs/create-jobs)

[Google Workflows Documentation](https://cloud.google.com/workflows/docs)
