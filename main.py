from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class TelemetryData(BaseModel):
    max_jerk: float
    lat: float
    lon: float

@app.post("/record-bump")
async def record_bump(data: TelemetryData):
    # Log the bump to your local CSV
    new_row = {
        "timestamp": time.time(),
        "max_jerk": data.max_jerk,
        "lat": data.lat,
        "lon": data.lon
    }
    # Append to the existing dataset
    df = pd.DataFrame([new_row])
    df.to_csv("roadsense_10k_dataset.csv", mode='a', header=False, index=False)
    return {"status": "success", "message": "Bump recorded at Chennai coordinates"}

@app.get("/top-10-roads")
async def get_roads(ward_id: int):
    # Your existing logic here...
    from db.queries import fetch_top_roads_by_ward
    return {"priority_segments": fetch_top_roads_by_ward(ward_id)}
