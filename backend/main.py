from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from backend.gcs_service import GCSService
import os

app = FastAPI()

# CORS - Allow all for simplicity in this setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

gcs = GCSService()

class ScanModel(BaseModel):
    qr1: str
    qr2: str
    status: str
    timestamp: str

@app.get("/api/health")
def health_check():
    return {"status": "ok"}

@app.post("/api/scan")
def save_scan(scan: ScanModel):
    try:
        success = gcs.save_scan(scan.dict())
        return {"success": success}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/history")
def get_history():
    return gcs.get_history()

# Serve Frontend Static Files
# This expects the frontend to be built into ../frontend/dist
frontend_dist = os.path.abspath(os.path.join(os.path.dirname(__file__), "../frontend/dist"))

if os.path.exists(frontend_dist):
    app.mount("/", StaticFiles(directory=frontend_dist, html=True), name="static")
else:
    print(f"Frontend build not found at {frontend_dist}. API only mode.")
