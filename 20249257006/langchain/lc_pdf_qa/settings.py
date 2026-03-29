from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parent.parent

CHROMA_DIR = os.getenv("CHROMA_DIR", ".chroma")
DATA_DIR = os.getenv("DATA_DIR", "data")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_LLM = os.getenv("OLLAMA_LLM", "llama3.1")
HF_EMBED_MODEL = os.getenv(
    "HF_EMBED_MODEL",
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
)


def chroma_path() -> Path:
    p = Path(CHROMA_DIR)
    return p if p.is_absolute() else (PROJECT_ROOT / p)


def data_path() -> Path:
    p = Path(DATA_DIR)
    return p if p.is_absolute() else (PROJECT_ROOT / p)
