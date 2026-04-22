"""MCP для ChatGPT по гайду OpenAI: ``mcp`` + ``FastMCP`` (streamable HTTP), опционально Google OAuth.

См. https://developers.openai.com/apps-sdk/build/mcp-server/ (Python: пакет ``mcp``, эргономика FastMCP).
"""

from __future__ import annotations

import logging
import os

from dotenv import load_dotenv
from fastmcp import FastMCP
from fastmcp.server.auth.providers.google import GoogleProvider
from mcp.types import ToolAnnotations
from starlette.requests import Request
from starlette.responses import JSONResponse

load_dotenv()


def _strip(v: str | None) -> str | None:
    if v is None:
        return None
    s = v.strip()
    return s or None


PUBLIC_BASE_URL = (_strip(os.environ.get("PUBLIC_BASE_URL")) or "http://127.0.0.1:8000").rstrip("/")
_GOOGLE_ID = _strip(os.environ.get("GOOGLE_CLIENT_ID"))
_GOOGLE_SECRET = _strip(os.environ.get("GOOGLE_CLIENT_SECRET"))
_JWT_KEY = _strip(os.environ.get("JWT_SIGNING_KEY"))

# Что должно быть в токене Google (tokeninfo): обычно openid + два URI userinfo.
_GOOGLE_USER_SCOPES = [
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
]
# Что разрешено при DCR / authorize у MCP-клиента (ChatGPT). Он часто шлёт OIDC
# шорткаты email и profile; если их нет в valid_scopes, mcp.shared.auth выдаёт
# invalid_scope: «Client was not registered with scope profile».
_GOOGLE_VALID_SCOPES = [
    "openid",
    "email",
    "profile",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
]


def _google_auth() -> GoogleProvider | None:
    if not _GOOGLE_ID or not _GOOGLE_SECRET:
        return None
    return GoogleProvider(
        client_id=_GOOGLE_ID,
        client_secret=_GOOGLE_SECRET,
        base_url=PUBLIC_BASE_URL,
        resource_base_url=PUBLIC_BASE_URL,
        required_scopes=_GOOGLE_USER_SCOPES,
        valid_scopes=_GOOGLE_VALID_SCOPES,
        jwt_signing_key=_JWT_KEY,
    )


_auth = _google_auth()


def _maybe_log_auth_scope_policy() -> None:
    """При AUTH_LOG_SCOPES=1 печатает, какие наборы scope где используются."""
    if not _strip(os.environ.get("AUTH_LOG_SCOPES")):
        return
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s %(name)s: %(message)s",
        force=True,
    )
    log = logging.getLogger(__name__)
    if _auth:
        log.info(
            "OAuth policy: required_in_google_token=%s | valid_for_mcp_client(DCR/authorize)=%s | "
            "tool_meta_securitySchemes_scopes=%s",
            _GOOGLE_USER_SCOPES,
            _GOOGLE_VALID_SCOPES,
            list(_GOOGLE_USER_SCOPES),
        )
    else:
        log.info("OAuth disabled (no GOOGLE_CLIENT_ID / GOOGLE_CLIENT_SECRET).")


_maybe_log_auth_scope_policy()

mcp = FastMCP(
    "hello-chatgpt-mcp",
    instructions="Тест: один инструмент echo. При включённом OAuth — как в коннекторе ChatGPT.",
    auth=_auth,
)

_tool_kw: dict = {
    "name": "echo",
    "description": "Возвращает тот же текст.",
    "annotations": ToolAnnotations(readOnlyHint=True),
}
if _auth:
    _tool_kw["meta"] = {
        "securitySchemes": [{"type": "oauth2", "scopes": list(_GOOGLE_USER_SCOPES)}],
    }


@mcp.tool(**_tool_kw)
def echo(text: str) -> str:
    return text


@mcp.custom_route("/", methods=["GET"])
async def _root(_request: Request) -> JSONResponse:
    return JSONResponse(
        {
            "mcp_url": f"{PUBLIC_BASE_URL}/mcp",
            "oauth": _auth is not None,
        }
    )


@mcp.custom_route("/health", methods=["GET"])
async def _health(_request: Request) -> JSONResponse:
    return JSONResponse({"status": "ok"})


app = mcp.http_app(path="/mcp", transport="streamable-http")
