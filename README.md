# MCP для ChatGPT (как в гайде OpenAI)

Стек из [Build your MCP server (Apps SDK)](https://developers.openai.com/apps-sdk/build/mcp-server/):

- протокол и совместимость — пакет **`mcp`** (ставится как зависимость **`fastmcp`**);
- HTTP **Streamable** MCP, OAuth (Google), DCR, `/.well-known` — **`fastmcp`** (`FastMCP`, `GoogleProvider`).

Отдельно вручную Starlette для `/mcp` не собираем: `FastMCP.http_app(..., transport="streamable-http")`.

## Запуск

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
# или: pip install -e .
cp .env.example .env   # при необходимости заполните PUBLIC_BASE_URL и GOOGLE_*
./run.sh                 # пишет .uvicorn.pid; остановка: ./stop.sh; статус: ./status.sh
```

Переменные (опционально): `PORT` (по умолчанию 8000), `HOST` (по умолчанию 0.0.0.0), `PIDFILE` (по умолчанию `./.uvicorn.pid`).

- MCP: `{PUBLIC_BASE_URL}/mcp` (по умолчанию `http://127.0.0.1:8000/mcp`)
- `GET /health`, `GET /`

## ChatGPT

1. Публичный **HTTPS** и URL **ровно** до endpoint MCP (часто без слэша в конце).
2. В коннекторе: если в `.env` заданы `GOOGLE_*` — OAuth; иначе сервер без auth (подходит только для локальных экспериментов, если UI это допускает).

## Инструмент

| Имя  | Аргумент | Ответ   |
|------|----------|---------|
| echo | `text`   | тот же текст |
