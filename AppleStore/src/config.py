import os
from dotenv import load_dotenv

load_dotenv('.env')

PROJECT_ID = os.environ.get("PROJECT_ID")
SECRET_ID = os.environ.get("SECRET_ID")

JWT_TOKEN = os.environ.get("JWT_TOKEN")
APP_ID = os.environ.get("APP_ID")
KEY_ID = os.environ.get("KEY_ID")
ISSUER_ID = os.environ.get("ISSUER_ID")
VENDOR_NUMBER = os.environ.get("VENDOR_NUMBER")
