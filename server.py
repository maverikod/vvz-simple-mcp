
import os

from fastapi import FastAPI
from mcp.types import ToolAnnotations

from fastmcp import FastMCP
from fastmcp.server.auth.providers.google import GoogleProvider

# --- Public URL (HTTPS, no trailing slash) — must match how clients reach this host
PUBLIC_BASE_URL = os.getenv("PUBLIC_BASE_URL", "https://mcp.techsup.od.ua").rstrip("/")

# Google OAuth (for FastMCP GoogleProvider → ChatGPT / OpenAI connector OAuth)
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")


def _build_auth() -> GoogleProvider | None:
    if not GOOGLE_CLIENT_ID or not GOOGLE_CLIENT_SECRET:
        return None
    return GoogleProvider(
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        base_url=PUBLIC_BASE_URL,
        resource_base_url=PUBLIC_BASE_URL,
        required_scopes=["openid", "email", "profile"],
        valid_scopes=["openid", "email", "profile"],
    )


auth = _build_auth()

# --- MCP ---
mcp = FastMCP(
    "ai-tools-echo",
    auth=auth,
    instructions=(
        "Echo demo tools for connectivity testing. Use echo to repeat text; "
        "use echo_upper to return uppercase text."
    ),
)


@mcp.tool(
    name="echo",
    title="Echo text",
    description=(
        "Use this when you need to repeat the user's input verbatim or verify that "
        "the MCP connector is working."
    ),
    annotations=ToolAnnotations(readOnlyHint=True),
)
def echo(text: str) -> dict[str, str]:
    return {"echo": text}


@mcp.tool(
    name="echo_upper",
    title="Echo text in uppercase",
    description=(
        "Use this when you need the same text as the user provided, but in UPPERCASE "
        "(for quick formatting checks)."
    ),
    annotations=ToolAnnotations(readOnlyHint=True),
)
def echo_upper(text: str) -> dict[str, str]:
    return {"echo_upper": text.upper()}


# Streamable HTTP + OAuth routes live on this Starlette app at the root of the host.
# MCP JSON-RPC endpoint: POST https://<host>/mcp
mcp_app = mcp.http_app(path="/mcp")


# FastAPI only adds a small health surface; everything else is delegated to mcp_app (mounted at /).
app = FastAPI(
    title="ai-tools-echo",
    lifespan=mcp_app.lifespan,
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)


@app.get("/")
def root():
    return {
        "status": "running",
        "mcp": f"{PUBLIC_BASE_URL}/mcp",
        "oauth": bool(auth),
    }


@app.get("/health")
def health():
    return {"status": "ok"}


# Mount MCP + OAuth + well-known at host root so RFC discovery paths match ChatGPT / OpenAI clients.
app.mount("/", mcp_app)
