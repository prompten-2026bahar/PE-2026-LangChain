from __future__ import annotations

import os

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI


DEFAULT_PROVIDER = "gemini"
DEFAULT_GEMINI_MODEL = "gemini-2.5-flash"
DEFAULT_GROQ_MODEL = "openai/gpt-oss-20b"
DEFAULT_TIMEOUT_SECONDS = 240.0
DEFAULT_MAX_RETRIES = 3


def read_provider() -> str:
    return os.environ.get("LLM_PROVIDER", DEFAULT_PROVIDER).strip().lower()


def read_temperature() -> float:
    return float(os.environ.get("LLM_TEMPERATURE", "0.1"))


def read_timeout() -> float:
    return float(os.environ.get("LLM_TIMEOUT_SECONDS", str(DEFAULT_TIMEOUT_SECONDS)))


def read_max_retries() -> int:
    return int(os.environ.get("LLM_MAX_RETRIES", str(DEFAULT_MAX_RETRIES)))


def build_gemini_model(model_name: str | None = None) -> ChatGoogleGenerativeAI:
    api_key = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GOOGLE_API_KEY or GEMINI_API_KEY is not set.")

    return ChatGoogleGenerativeAI(
        model=model_name or os.environ.get("LLM_MODEL", DEFAULT_GEMINI_MODEL),
        google_api_key=api_key,
        temperature=read_temperature(),
        timeout=read_timeout(),
        max_retries=read_max_retries(),
    )


def build_groq_model(model_name: str | None = None) -> ChatOpenAI:
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY is not set.")

    return ChatOpenAI(
        model=model_name or os.environ.get("LLM_MODEL", DEFAULT_GROQ_MODEL),
        openai_api_key=api_key,
        openai_api_base=os.environ.get("GROQ_BASE_URL", "https://api.groq.com/openai/v1"),
        temperature=read_temperature(),
        request_timeout=read_timeout(),
        max_retries=read_max_retries(),
    )


def build_chat_model(model_name: str | None = None):
    provider = read_provider()
    if provider == "gemini":
        return build_gemini_model(model_name=model_name)
    if provider == "groq":
        return build_groq_model(model_name=model_name)
    raise RuntimeError(
        "Unsupported LLM_PROVIDER. Use 'gemini' or 'groq'."
    )
