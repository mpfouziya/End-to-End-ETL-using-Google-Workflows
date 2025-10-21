import jwt
import time
import requests
import gzip
import pandas as pd
from pathlib import Path
from google.cloud import secretmanager
import os
import tempfile

from src.config import PROJECT_ID, JWT_TOKEN, APP_ID, ISSUER_ID, KEY_ID, VENDOR_NUMBER
from src.constants.columns import sales_columns, finance_columns


# Base URL for API
BASE_URL = "https://api.appstoreconnect.apple.com/v1"

class AppleStore:

    def __init__(self):
        # --- Get secrets from GCP Secret Manager ---
        self.project_id = PROJECT_ID
        self.private_key = self.load_secret(JWT_TOKEN)  # contents of .p8 file
        self.issuer_id = self.load_secret(ISSUER_ID)  # Issuer ID
        self.key_id = self.load_secret(KEY_ID)  # Key ID
        self.vendor_number = VENDOR_NUMBER

        # --- Build JWT token ---
        payload = {
            "iss": self.issuer_id,
            "exp": int(time.time()) + 600,  # Token valid for 10 minutes
            "aud": "appstoreconnect-v1"
        }

        headers = {
            "alg": "ES256",
            "kid": self.key_id
        }

        self.token = jwt.encode(payload, self.private_key, algorithm="ES256", headers=headers)

    def load_secret(self,secret_name):
        """Load a secret from Secret Manager."""
        client = secretmanager.SecretManagerServiceClient()
        name = f"projects/{self.project_id}/secrets/{secret_name}/versions/latest"
        response = client.access_secret_version(name=name)
        return response.payload.data.decode("UTF-8")

    def process_df(self, df):
        df['begin_date'] = pd.to_datetime(df['begin_date']).dt.date
        df['product_type_identifier'] = df['product_type_identifier'].astype('str')
        df['version'] = df['version'].astype(str)
        df['sku'] = df['sku'].astype(str)
        return df

# Fetch sales reports (Corrected)
    def fetch_sales_report(self, report_type="SALES", frequency="DAILY", report_subtype="SUMMARY", date="2025-01-28"):
        try:
            headers = {"Authorization": f"Bearer {self.token}"}

            endpoint = f"{BASE_URL}/salesReports"
            params = {
                "filter[reportType]": report_type,  # SALES or SUBSCRIPTION
                "filter[reportSubType]": report_subtype,  # SUMMARY, DETAILED, OPT-IN, etc.
                "filter[frequency]": frequency,  # DAILY, WEEKLY, MONTHLY, YEARLY
                "filter[reportDate]": date,  # Format: YYYY-MM-DD
                "filter[vendorNumber]": VENDOR_NUMBER  # Your vendor number
            }

            response = requests.get(endpoint, headers=headers, params=params)
            if response.status_code == 200:
                with open("sales_report.gz", "wb") as file:
                    file.write(response.content)
                print("Sales report downloaded successfully: sales_report.gz")
            else:
                print(f"Failed to download sales report: {response.text}")

            with gzip.open(Path.cwd() / 'sales_report.gz', "rt", encoding="utf-8") as f:
                df = pd.read_csv(f, delimiter="\t")  # TSV format
                os.remove(Path.cwd() /'sales_report.gz')

                # Display the first few rows
            df = df[sales_columns]
            df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
            df = self.process_df(df)

            return df

        except Exception as e:
            print(e)



    # Fetch financial reports (Corrected)
    def fetch_financial_report(self, year="2024", month="02", region_code="WW"):  # "WW" for worldwide

        headers = {"Authorization": f"Bearer {self.token}"}

        endpoint = f"{BASE_URL}/financeReports"
        params = {
            "filter[reportDate]": f"{year}-{month}",  # Format: YYYY-MM
            "filter[regionCode]": region_code,  # Region code (WW for worldwide)
            "filter[vendorNumber]": VENDOR_NUMBER  # Your vendor number
        }

        response = requests.get(endpoint, headers=headers, params=params)

        if response.status_code == 200:
            with open("financial_report.gz", "wb") as file:
                file.write(response.content)
            print("Financial report downloaded successfully: financial_report.gz")
        else:
            print(f"Failed to download financial report: {response.text}")


# Example Usage
# fetch_sales_report()
# fetch_financial_report()
