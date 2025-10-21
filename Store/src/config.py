import os
from dotenv import load_dotenv

load_dotenv('.env')


PROJECT_ID = os.environ.get("PROJECT_ID")
SECRET_ID = os.environ.get("SECRET_ID")
API_KEY = os.environ.get("EXCHANGE_API_KEY")