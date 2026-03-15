#!/bin/bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PID_FILE="$SCRIPT_DIR/.backend.pid"
LOG_FILE="$SCRIPT_DIR/backend.log"
VENV_PYTHON="$SCRIPT_DIR/.venv/bin/python"

cd "$SCRIPT_DIR"

if [[ -f "$PID_FILE" ]]; then
    EXISTING_PID="$(cat "$PID_FILE")"
    if kill -0 "$EXISTING_PID" >/dev/null 2>&1; then
        echo "Backend is already running with PID $EXISTING_PID"
        exit 0
    fi
    rm -f "$PID_FILE"
fi

if [[ ! -x "$VENV_PYTHON" ]]; then
    echo "Virtual environment is missing at $VENV_PYTHON"
    echo "Create it first with: python3 -m venv .venv && ./.venv/bin/pip install -r requirements.txt"
    exit 1
fi

if [[ -f ".env" ]]; then
    set -a
    source ".env"
    set +a
fi

LLM_PROVIDER="${LLM_PROVIDER:-gemini}"

if [[ "$LLM_PROVIDER" == "groq" ]]; then
    if [[ -z "${GROQ_API_KEY:-}" ]]; then
        echo "LLM_PROVIDER=groq but GROQ_API_KEY is not set."
        echo "Add GROQ_API_KEY to backend/.env before starting the server."
        exit 1
    fi
elif [[ "$LLM_PROVIDER" == "gemini" ]]; then
    if [[ -z "${GOOGLE_API_KEY:-}" && -z "${GEMINI_API_KEY:-}" ]]; then
        echo "LLM_PROVIDER=gemini but GOOGLE_API_KEY or GEMINI_API_KEY is not set."
        echo "Add one of them to backend/.env before starting the server."
        exit 1
    fi
else
    echo "Unsupported LLM_PROVIDER: $LLM_PROVIDER"
    echo "Use LLM_PROVIDER=gemini or LLM_PROVIDER=groq"
    exit 1
fi

nohup "$VENV_PYTHON" -m uvicorn app.main:app --host 127.0.0.1 --port 8000 >"$LOG_FILE" 2>&1 &
BACKEND_PID=$!
echo "$BACKEND_PID" >"$PID_FILE"

sleep 2

if kill -0 "$BACKEND_PID" >/dev/null 2>&1; then
    echo "Backend started successfully."
    echo "PID: $BACKEND_PID"
    echo "Log: $LOG_FILE"
    echo "Health: http://127.0.0.1:8000/health"
else
    echo "Backend failed to start. Check $LOG_FILE"
    rm -f "$PID_FILE"
    exit 1
fi
