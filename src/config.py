import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"

load_dotenv(dotenv_path=ENV_PATH)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
LLM_NAME = os.getenv("OLLAMA_NAME")
LLM_HOST = os.getenv("OLLAMA_HOST")
