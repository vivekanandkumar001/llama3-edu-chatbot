from pathlib import Path
import os

ROOT = Path(__file__).resolve().parent.parent

# Ollama / LLaMA config
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
LLAMA_MODEL = os.getenv("LLAMA_MODEL", "llama3")  # use "llama3" or "llama3:8b" etc.

# Embedding model for retrieval
EMBED_MODEL = os.getenv("EMBED_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

# Paths
DATA_DIR = ROOT / "data"
STORAGE_DIR = ROOT / "storage"
CHROMA_DIR = STORAGE_DIR / "chroma"
DB_PATH = STORAGE_DIR / "leads.db"

# UI / Server config
HOST = "127.0.0.1"
PORT = 8000

# Bot system prompt (tweak tone / persuasion here)
SYSTEM_PROMPT = """You are EduBot, a friendly and persuasive educational counselor.
- Answer accurately; prefer to use the provided context (do not invent course fees or durations).
- Use a warm tone and short replies. Use emojis sparingly.
- If the user is clearly interested, offer to send the syllabus/placement guide and ask politely for email & phone.
- If the information is not in context, ask to collect contact details so a counselor can confirm.
"""
