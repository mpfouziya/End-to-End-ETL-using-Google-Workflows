import os
from dotenv import load_dotenv

load_dotenv('.env')

PROJECT_ID = os.environ.get("PROJECT_ID")
SECRET_ID = os.environ.get("SECRET_ID")
PUBLISHER_ID = os.environ.get("PUBLISHER_ID")
AD_MOB_SECRET = os.environ.get("AD_MOB_SECRET")
AD_MOB_CREDENTIALS = os.environ.get("AD_MOB_CREDENTIALS")