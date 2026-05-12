from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import joblib
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load AI Brain
base_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(base_dir, "pothole_model.pkl")
ai_model = joblib.load(model_path) if os.path.exists(model_path) else None

class TelemetryData(BaseModel):
    max_jerk: float
    lat: float
    lon: float

@app.post("/record-bump")
async def record_bump(data: TelemetryData):
    res = "Normal_Road"
    if ai_model:
        res = ai_model.predict([[data.max_jerk]])
    return {"status": "success", "analysis": res, "severity": data.max_jerk}

@app.get("/top-10-roads")
async def get_roads():
    # Returning sample data from your 10k dataset logic
    return {"priority_segments": [{"segment_id": "ST-101", "health_score": 45}, {"segment_id": "ST-202", "health_score": 88}]}

@app.get("/")
def home():
    return {"message": "RoadSense AI Backend is Online"}
