
# FastMCP Echo (OpenAI / ChatGPT–compatible MCP)

## Features
- **MCP** (streamable HTTP) with tools `echo` and `echo_upper`
- **Google OAuth** via FastMCP `GoogleProvider` (MCP authorization spec: PRM + OAuth AS metadata on the same host)
- **FastAPI** only for `/` and `/health`; MCP + OAuth + `/.well-known/*` are served from the mounted FastMCP ASGI app at `/`

## Public URLs (production)
- **MCP (Streamable HTTP):** `https://mcp.techsup.od.ua/mcp`  
  Use this exact URL in ChatGPT / OpenAI connector settings (avoid a trailing slash — some clients get an extra redirect).
- **Health:** `GET https://mcp.techsup.od.ua/health`
- **OAuth / discovery:** served at the **root** of the host, e.g.  
  `GET https://mcp.techsup.od.ua/.well-known/oauth-protected-resource/mcp`  
  `GET https://mcp.techsup.od.ua/.well-known/oauth-authorization-server`

## Environment variables
| Variable | Required | Description |
|----------|----------|-------------|
| `PUBLIC_BASE_URL` | recommended | Public origin, no trailing slash. Default: `https://mcp.techsup.od.ua` |
| `GOOGLE_CLIENT_ID` | for OAuth | Google OAuth client ID |
| `GOOGLE_CLIENT_SECRET` | for OAuth | Google OAuth client secret |

If `GOOGLE_CLIENT_ID` / `GOOGLE_CLIENT_SECRET` are **not** set, the server runs **without** OAuth (tools work, but there is no `/.well-known/oauth-*` metadata — not suitable for ChatGPT connector OAuth).

### Google Cloud Console
- Add authorized redirect URIs required by your OAuth client. FastMCP’s Google provider uses paths under `PUBLIC_BASE_URL` (see FastMCP docs for `redirect_path`, default `/auth/callback`).
- For **ChatGPT**, allow redirect URIs documented by OpenAI (e.g. `https://chatgpt.com/connector/oauth/...`) — see [OpenAI Apps SDK auth](https://developers.openai.com/apps-sdk/build/auth/).

## Run locally
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
cp -n .env.example .env   # optional: create from template
# edit .env — set GOOGLE_* and optionally PUBLIC_BASE_URL=http://127.0.0.1:8000 for local tests
./run.sh
```

Local MCP URL: `http://127.0.0.1:8000/mcp`

## ChatGPT / OpenAI
- **Connector MCP URL:** `https://mcp.techsup.od.ua/mcp`
- Complete the OAuth link flow in ChatGPT when prompted; the server expects `Authorization: Bearer` on MCP requests after linking.

## Scripts
- `./run.sh` — start uvicorn
- `./stop.sh`, `./status.sh` — if present, helper scripts for the process
