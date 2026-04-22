#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
PIDFILE="${PIDFILE:-${PWD}/.uvicorn.pid}"

if [[ ! -f "$PIDFILE" ]]; then
	echo "Не запущен (нет $PIDFILE)."
	exit 0
fi

pid="$(<"$PIDFILE")"
if [[ -d "/proc/$pid" ]] || kill -0 "$pid" 2>/dev/null; then
	kill "$pid" 2>/dev/null || true
	# даём uvicorn завершиться
	for _ in 1 2 3 4 5 6 7 8 9 10; do
		if [[ ! -d "/proc/$pid" ]] && ! kill -0 "$pid" 2>/dev/null; then
			break
		fi
		sleep 0.2
	done
	if [[ -d "/proc/$pid" ]] || kill -0 "$pid" 2>/dev/null; then
		kill -9 "$pid" 2>/dev/null || true
	fi
	echo "Остановлен pid=$pid"
else
	echo "PID $pid уже не существует, удаляю pidfile."
fi
rm -f "$PIDFILE"
