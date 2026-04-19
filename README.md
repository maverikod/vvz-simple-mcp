
# FastMCP Echo OAuth Server

## Features
- MCP server (echo)
- Google OAuth ready
- FastAPI wrapper
- Start/stop/status scripts

## Run
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

./run.sh

## MCP endpoint
http://localhost:8000/mcp

## OAuth
/auth/login
/auth/callback

## ChatGPT
Use MCP URL:
https://YOUR_DOMAIN/mcp
