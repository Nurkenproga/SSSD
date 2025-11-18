# app/main.py (fixed for Python 3.9)
import json
import logging
import os
from pathlib import Path
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

log = logging.getLogger("lab4")
logging.basicConfig(level=logging.INFO)

app = FastAPI(title="doing FastAPI safe demo")

_allowed = os.environ.get("ALLOWED_ORIGINS", "").strip()
if _allowed:
    origins = [o.strip() for o in _allowed.split(",") if o.strip()]
else:
    origins = []

if origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["Authorization", "Content-Type"],
    )
    log.info("CORS enabled for origins: %s", origins)
else:ь
    log.info("CORS disabled (no ALLOWED_ORIGINS configured)")

SECRET_KEY = os.environ.get("API_SECRET")  # set via .env or secrets manager

config_path = Path("config/config.json")
if config_path.exists():
    try:
        with config_path.open("r", encoding="utf-8") as f:
            config = json.load(f)
    except Exception as e:
        log.warning("Failed to parse config/config.json: %s", e)
        config = {}
else:
    log.info("config/config.json not found — using empty config")
    config = {}

@app.get("/")
def root():
    return {"message": "HEY Hey world"}

@app.get("/secret")
def get_secret(token: Optional[str] = None):
    """
    Protected access to secret:
    - If SECRET_KEY is not configured on the server, return 404 (not available).
    - If configured, require a token query param matching ADMIN_TOKEN env var (simple demo auth).
    """
    if not SECRET_KEY:
        raise HTTPException(status_code=404, detail="Secret not available")
    admin_token = os.environ.get("ADMIN_TOKEN")
    if not admin_token or token != admin_token:
        raise HTTPException(status_code=403, detail="forbidden")
    return {"secret": SECRET_KEY}

@app.get("/divide")
def divide(a: int, b: int):
    if b == 0:
        raise HTTPException(status_code=400, detail="Invalid input: divisor must not be zero")
    try:
        result = a / b
        return {"result": result}
    except Exception:
        log.exception("Unhandled error in /divide with a=%s b=%s", a, b)
        raise HTTPException(status_code=500, detail="Internal server error")
