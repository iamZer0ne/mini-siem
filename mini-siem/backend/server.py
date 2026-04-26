from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB = []
VALID_KEYS = ["device-1-key", "device-2-key"]

@app.get("/")
def home():
    return {"status": "SIEM backend running"}

@app.post("/logs")
async def receive_logs(data: Dict, authorization: str = Header(None)):
    if authorization not in VALID_KEYS:
        raise HTTPException(status_code=401, detail="Unauthorized")

    log = {
        "timestamp": datetime.utcnow().isoformat(),
        "hostname": data.get("hostname"),
        "cpu": data.get("cpu"),
        "memory": data.get("memory"),
        "processes": data.get("processes")
    }

    DB.append(log)
    return {"status": "received"}

@app.get("/logs")
def get_logs():
    return DB[-50:]
