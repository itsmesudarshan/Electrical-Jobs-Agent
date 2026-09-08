import json, os
from pathlib import Path
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")

def load_json(relative):
    with open(ROOT / relative, encoding="utf-8") as f:
        return json.load(f)

SETTINGS = load_json("config/settings.json")
PROFILE = load_json("config/profile.json")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "").strip()
HF_TOKEN = os.getenv("HF_TOKEN", "").strip()
ENABLE_HF_AI = os.getenv("ENABLE_HF_AI", "false").lower() == "true"
STATE_PATH = ROOT / "data" / "state.json"
