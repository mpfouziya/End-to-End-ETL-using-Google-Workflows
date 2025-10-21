import os
from dotenv import load_dotenv

load_dotenv('.env')

PROJECT_ID = os.environ.get("PROJECT_ID")
SECRET_ID = os.environ.get("SECRET_ID")
ADJUST_API_TOKEN = os.environ.get("ADJUST_API_TOKEN")
APP_TOKEN = os.environ.get("APP_TOKEN")
