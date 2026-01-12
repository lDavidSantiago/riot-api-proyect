from dotenv import load_dotenv
import os

load_dotenv()

RIOT_API_KEY = os.getenv("RIOT_API_KEY")
REDIS_URL = os.getenv("REDIS_URL")

if not RIOT_API_KEY:
    raise RuntimeError("RIOT_API_KEY missing")
