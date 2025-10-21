import pandas as pd
import pymysql
from google.cloud import secretmanager
from src.config import (PROJECT_ID, DB_HOST, DB_DATABASE, DB_USER, DB_PASSWORD)


class GameData:
    def __init__(self):
        self.project_id = PROJECT_ID
        self.connection = pymysql.connect(
            host=self.load_secret(DB_HOST).strip(),
            user=self.load_secret(DB_USER).strip(),
            password=self.load_secret(DB_PASSWORD).strip(),
            port=3306,
            database=self.load_secret(DB_DATABASE).strip()
        )
    def load_secret(self,secret_name):
        """Load a secret from Secret Manager."""
        client = secretmanager.SecretManagerServiceClient()
        name = f"projects/{self.project_id}/secrets/{secret_name}/versions/latest"
        response = client.access_secret_version(name=name)
        return response.payload.data.decode("UTF-8")

    def run_query(self, query):
        try:        
            data = pd.read_sql_query(query, self.connection)
            return data
        
        except Exception as e:
            return f'events :{str(e)}'

    def close_tunnel(self):
        self.connection.close()


   

    

