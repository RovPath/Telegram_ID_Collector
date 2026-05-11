import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TG_TOKEN")
DB_PATH = "database/users.db"

USE_PROXY = os.getenv("USE_PROXY", "False").lower() == "true"
PROXY_URL = os.getenv("PROXY_URL")

if not BOT_TOKEN:
    raise ValueError("TG_TOKEN is missing in environment. Please check your .env file.")

os.makedirs("database", exist_ok=True)
