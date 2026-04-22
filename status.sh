#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
PIDFILE="${PIDFILE:-${PWD}/.uvicorn.pid}"

if [[ ! -f "$PIDFILE" ]]; then
	echo "Не запущен (нет $PIDFILE)."
	exit 0
fi

pid="$(<"$PIDFILE")"
alive=false
if [[ -d "/proc/$pid" ]]; then
	alive=true
elif kill -0 "$pid" 2>/dev/null; then
	alive=true
fi

if $alive; then
	echo "Запущен pid=$pid"
	ps -p "$pid" -o pid=,args= 2>/dev/null || true
else
	echo "Устаревший pidfile (pid $pid). Удалите $PIDFILE или ./stop.sh"
	exit 1
fi
