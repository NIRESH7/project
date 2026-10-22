import os
from dotenv import load_dotenv

load_dotenv()

# --- Gemini API Keys (Primary - FREE) ---
GEMINI_API_KEY_1 = os.getenv("GEMINI_API_KEY_1", "")
GEMINI_API_KEY_2 = os.getenv("GEMINI_API_KEY_2", "")
GEMINI_API_KEY_3 = os.getenv("GEMINI_API_KEY_3", "")
GEMINI_API_KEY_4 = os.getenv("GEMINI_API_KEY_4", "")
GEMINI_API_KEY_5 = os.getenv("GEMINI_API_KEY_5", "")

# --- OpenAI API Keys (Fallback - if Gemini fails) ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_FALLBACK_API_KEY = os.getenv("OPENAI_FALLBACK_API_KEY", "")

# MySQL connection string, e.g., mysql+pymysql://user:password@aws-rds-host:3306/product_db
# Defaults to a local SQLite database if MySQL environment variables are not provided
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DB = os.getenv("MYSQL_DB", "products_db")

if MYSQL_HOST and MYSQL_USER:
    DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
else:
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./products.db")
