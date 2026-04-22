#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
source .venv/bin/activate

PORT="${PORT:-8000}"
HOST="${HOST:-0.0.0.0}"
PIDFILE="${PIDFILE:-${PWD}/.hypercorn.pid}"

rm -f "$PIDFILE"
cleanup() {
	rm -f "$PIDFILE"
}
trap cleanup EXIT INT TERM

hypercorn server:app --bind "${HOST}:${PORT}" &
echo $! >"$PIDFILE"
wait
