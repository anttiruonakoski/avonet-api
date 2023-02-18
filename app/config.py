from pathlib import Path
from decouple import config

DB_FILE = config("DB_FILE", default="app.db")
DATA_DIR = Path(__file__).parent / "data"
DATA_FILE = config("DATA_FILE", default="AVONET1_BirdLife.csv")

API_LAJI_FI_TOKEN = config("API_LAJI_FI_TOKEN")
