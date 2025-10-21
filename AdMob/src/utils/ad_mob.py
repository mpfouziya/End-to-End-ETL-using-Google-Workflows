import json
import pandas as pd
import requests
from google.auth.transport.requests import Request
from google.cloud import secretmanager
from google.oauth2.credentials import Credentials
from datetime import datetime

from src.config import PROJECT_ID, PUBLISHER_ID, AD_MOB_SECRET, AD_MOB_CREDENTIALS

class AdMob:
    def __init__(self):
        self.project_id = PROJECT_ID
        self.publisher_id = PUBLISHER_ID
        self.ad_mob_secret = AD_MOB_SECRET # Saved in GCP Secret Manager to re use for browser login if the ad_mob_credentials is revoked
        self.ad_mob_credentials = AD_MOB_CREDENTIALS


    def load_secret(self,secret_name):
        """Load a secret from Secret Manager."""
        client = secretmanager.SecretManagerServiceClient()
        name = f"projects/{self.project_id}/secrets/{secret_name}/versions/latest"
        response = client.access_secret_version(name=name)
        return response.payload.data.decode("UTF-8")

    def get_ad_mob_credentials(self):
        creds = None
        # Load credentials.json (already contains refresh_token) from Secret Manager
        creds_json = self.load_secret(self.ad_mob_credentials)  # store credentials.json here
        creds = Credentials.from_authorized_user_info(json.loads(creds_json))

        # Refresh if expired
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

        pub_id = self.load_secret(self.publisher_id)

        return creds, pub_id

    def micros_to_currency(self,micros_value):
        return round(int(micros_value) / 1000000, 2)

    def fetch_admob_earnings(self, start_date, end_date):
        creds, pub_id = self.get_ad_mob_credentials()
        token = creds.token
        url = f"https://admob.googleapis.com/v1/accounts/{pub_id}/mediationReport:generate"
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        body = {
            "reportSpec": {
                "dateRange": {
                    "startDate": {"year": start_date.year, "month": start_date.month, "day": start_date.day},
                    "endDate": {"year": end_date.year, "month": end_date.month, "day": end_date.day},
                },
                "dimensions": ["DATE", "COUNTRY", "PLATFORM", "AD_SOURCE"],
                "metrics": ["ESTIMATED_EARNINGS"],
                "timeZone": ""
            }
        }

        response = requests.post(url, headers=headers, json=body)
        rows = []
        if response.status_code == 200:
            report = response.json()
            print(report)
            for item in report:
                print(item)
                if "row" in item:
                    row = item["row"]
                    date_str = row["dimensionValues"]["DATE"]["value"]
                    country_str = row["dimensionValues"]["COUNTRY"]["value"]
                    platform_str = row["dimensionValues"]["PLATFORM"]["value"]
                    micros_val = row["metricValues"]["ESTIMATED_EARNINGS"]["microsValue"]
                    try:
                        ad_source_str = row["dimensionValues"]["AD_SOURCE"]["displayLabel"]
                    except Exception as e:
                        ad_source_str = ""

                    rows.append({
                        "reporting_date": datetime.strptime(date_str, "%Y%m%d"),
                        "country_code": country_str,
                        "platform": platform_str,
                        "ad_source": ad_source_str,
                        "ad_revenue": self.micros_to_currency(micros_val)
                    })

            df = pd.DataFrame(rows)

            print(df)
            return df

        else:
            print(f"Error {response.status_code}: {response.text}")





   

    

