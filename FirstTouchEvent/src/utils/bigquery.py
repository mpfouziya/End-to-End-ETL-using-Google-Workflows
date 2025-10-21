from pathlib import Path
import json
from google.cloud import bigquery, secretmanager
from google.oauth2 import service_account

from src.config import PROJECT_ID, SECRET_ID


class BigQuery:
    def __init__(self):
        self.project_id = PROJECT_ID
        self.secret_id = SECRET_ID
        self.version_id = 1

        # Build the name of the secret version
        name = f"projects/{self.project_id}/secrets/{self.secret_id}/versions/{self.version_id}"

        # Create the Secret Manager client
        client = secretmanager.SecretManagerServiceClient()

        # Access the secret version
        response = client.access_secret_version(name=name)

        # Get the secret payload
        secret_payload = response.payload.data.decode('UTF-8')

        # Parse the JSON key content
        service_account_info = json.loads(secret_payload)

        # Create credentials using the service account info
        credentials = service_account.Credentials.from_service_account_info(service_account_info)
        self.client = bigquery.Client(credentials=credentials, project=self.project_id)

    def run_query(self, query):
        job = self.client.query(query)
        job.result()