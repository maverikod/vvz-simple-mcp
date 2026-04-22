#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
source .venv/bin/activate

PORT="${PORT:-8000}"
HOST="${HOST:-0.0.0.0}"
PIDFILE="${PIDFILE:-${PWD}/.uvicorn.pid}"

rm -f "$PIDFILE"
cleanup() {
	rm -f "$PIDFILE"
}
trap cleanup EXIT INT TERM

uvicorn server:app --host "$HOST" --port "$PORT" &
echo $! >"$PIDFILE"
wait
