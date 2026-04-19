
import os
from fastmcp import FastMCP
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, JSONResponse
import requests

# --- CONFIG ---
CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")

AUTH_URI = "https://accounts.google.com/o/oauth2/auth"
TOKEN_URI = "https://oauth2.googleapis.com/token"

# --- MCP ---
mcp = FastMCP("ai-tools-echo")

@mcp.tool()
def echo(text: str):
    return {"echo": text}

@mcp.tool()
def echo_upper(text: str):
    return {"echo_upper": text.upper()}

# --- FASTAPI WRAPPER ---
app = FastAPI()

@app.get("/")
def root():
    return {"status": "running"}

@app.get("/auth/login")
def login():
    url = (
        f"{AUTH_URI}?response_type=code"
        f"&client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&scope=openid email profile"
    )
    return RedirectResponse(url)

@app.get("/auth/callback")
async def callback(request: Request):
    code = request.query_params.get("code")
    data = {
        "code": code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    token = requests.post(TOKEN_URI, data=data).json()
    return JSONResponse(token)

# Mount MCP
app.mount("/mcp", mcp.app)
