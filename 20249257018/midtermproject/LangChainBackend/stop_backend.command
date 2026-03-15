#!/bin/bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PID_FILE="$SCRIPT_DIR/.backend.pid"

cd "$SCRIPT_DIR"

if [[ ! -f "$PID_FILE" ]]; then
    echo "No PID file found. Backend may already be stopped."
    exit 0
fi

BACKEND_PID="$(cat "$PID_FILE")"

if ! kill -0 "$BACKEND_PID" >/dev/null 2>&1; then
    echo "Process $BACKEND_PID is not running. Cleaning up PID file."
    rm -f "$PID_FILE"
    exit 0
fi

kill "$BACKEND_PID"

for _ in {1..10}; do
    if ! kill -0 "$BACKEND_PID" >/dev/null 2>&1; then
        rm -f "$PID_FILE"
        echo "Backend stopped."
        exit 0
    fi
    sleep 1
done

kill -9 "$BACKEND_PID" >/dev/null 2>&1 || true
rm -f "$PID_FILE"
echo "Backend force-stopped."
