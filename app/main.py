# app/main.py
import json
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

log = logging.getLogger("lab4")
log.setLevel(logging.INFO)

app = FastAPI(title="doing FastAPI vulnerable demo")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SECRET_KEY = "You found a secret!"

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
def get_secret():
    return {"secret": SECRET_KEY}

@app.get("/divide")
def divide(a: int, b: int):
    try:
        return {"result": a / b}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
