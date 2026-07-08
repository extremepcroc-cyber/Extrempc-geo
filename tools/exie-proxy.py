#!/usr/bin/env python3
"""
exie-proxy.py — OpenAI-compatible proxy for Exie chat widget.
Accepts /v1/chat/completions and proxies to Hermes agent via subprocess.

Usage:
    python tools/exie-proxy.py
    (listens on 0.0.0.0:8645)
"""

import json, os, sys, subprocess, re
from pathlib import Path
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

# Load .env
_env_paths = [
    Path(os.environ.get("HERMES_PROFILE_DIR", "")) / "extremepc.env",
    Path.home() / "AppData/Local/hermes/profiles/exie/extremepc.env",
]
for _p in _env_paths:
    if _p.exists():
        with open(_p) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip())

API_KEY = os.environ.get("API_SERVER_KEY", "")
ALLOWED_ORIGINS = os.environ.get("API_SERVER_CORS_ORIGINS", "").split(",")

app = FastAPI(title="Exie Proxy")

# CORS — allow BC storefront origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in ALLOWED_ORIGINS if o.strip()] + ["*"],
    allow_credentials=True,
    allow_methods=["POST", "OPTIONS"],
    allow_headers=["*"],
)


def _check_auth(request: Request):
    auth = request.headers.get("authorization", "")
    if not auth.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")
    token = auth[7:]
    if token != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")


@app.post("/v1/chat/completions")
async def chat_completions(request: Request):
    _check_auth(request)
    body = await request.json()
    messages = body.get("messages", [])

    # Build query from messages
    query_parts = []
    for m in messages:
        role = m.get("role", "user")
        content = m.get("content", "")
        if role == "system":
            query_parts.append(f"[System: {content}]")
        elif role == "user":
            query_parts.append(content)

    query = "\n".join(query_parts)

    # Call Hermes CLI for the response
    hermes_bin = str(Path.home() / "AppData/Local/hermes/hermes-agent/venv/Scripts/hermes.exe")
    try:
        result = subprocess.run(
            [hermes_bin, "chat", "-q", query, "-Q"],
            capture_output=True, text=True, timeout=120,
            env={**os.environ, "HERMES_PROFILE": "exie"},
        )
        reply = (result.stdout or result.stderr).strip()
        # Strip "session_id:" line if present
        if reply.startswith("session_id:"):
            lines = reply.split("\n", 1)
            reply = lines[1].strip() if len(lines) > 1 else ""
        if not reply:
            reply = "Sorry, I couldn't process that."
    except subprocess.TimeoutExpired:
        reply = "Request timed out. Please try again."
    except FileNotFoundError:
        reply = "Exie is not available right now."

    return JSONResponse({
        "id": "chatcmpl-exie",
        "object": "chat.completion",
        "choices": [{
            "index": 0,
            "message": {"role": "assistant", "content": reply},
            "finish_reason": "stop",
        }],
    })


@app.options("/v1/chat/completions")
async def chat_completions_preflight():
    return JSONResponse(status_code=204)


if __name__ == "__main__":
    port = int(os.environ.get("API_SERVER_PORT", "8645")) + 3  # 8648 to avoid conflict
    uvicorn.run(app, host="127.0.0.1", port=port, log_level="info")
