Here's the full README for roadsense_backend directly:

🛣️ RoadSense — AI-Powered Road Intelligence Backend

WitchHunt 2026 · Team LogicWeave
Transforming every smartphone into a passive road sensor to enable proactive, data-driven municipal maintenance.

Show Image Show Image Show Image Show Image

📌 What is RoadSense?
RoadSense is an AI-powered telemetry analytics platform that automatically detects potholes and road damage using smartphone sensor data — no manual reporting required. As vehicles travel, accelerometer and GPS data is passively collected, classified by a trained ML model, and surfaced to municipal officers through a real-time decision dashboard.
The problem it solves: India has 63+ lakh km of roads but maintenance is entirely reactive. Municipal corporations lack real-time visibility, complaint-based systems see <5% participation, and reactive repairs cost 3–4× more than preventive maintenance.

🏗️ Architecture Overview
Flutter App (50Hz sensor harvest)
        │
        ▼
POST /record-bump ──► RandomForest Classifier ──► Classification + Severity Score
                              │
                    pothole_model.pkl
                              │
GET /top-10-roads ◄───────────┘
        │
        ▼
React + Leaflet.js Dashboard (municipal officers)
4-Layer Backend Model
LayerDescriptionAPI LayerFastAPI handles all HTTP requests with CORS securityService LayerOrchestrates business logic and decision-makingProcessing LayerMathematical clustering on jerk and amplitude sensor dataData LayerPandas ingests and queries 10,000+ records from CSV

📁 Project Structure
roadsense_backend/
├── main.py                    # FastAPI application & API endpoints
├── models.py                  # Pydantic data models (13-feature EventPayload)
├── train_model.py             # RandomForest training script
├── pothole_model.pkl          # Trained ML model (serialised via joblib)
├── roadsense_10k_dataset.csv  # 10,000 synthetic sensor records
├── requirements.txt           # Python dependencies
├── runtime.txt                # Python version declaration
├── App.js                     # React + Vite frontend (Leaflet + Recharts)
├── db/                        # Database layer
├── processors/                # Jerk & amplitude clustering logic
├── routers/                   # API route handlers
└── services/                  # Business logic services

🤖 ML Model & Features
Current POC Model
pothole_model.pkl is a RandomForestClassifier trained on max_jerk from the 10K synthetic dataset.
pythonclass TelemetryData(BaseModel):
    max_jerk: float   # Rate of change of acceleration (m/s³)
    lat: float        # GPS latitude
    lon: float        # GPS longitude
Full Sensor Schema — Phase 2 (models.py)
FeatureTypeDescriptionlatfloatGPS latitude coordinatelonfloatGPS longitude coordinatedurationfloatDuration of bump event (ms)rise_timefloatTime from onset to peak amplitude (ms)fall_timefloatTime from peak back to baseline (ms)rise_fall_ratiofloatRatio of rise_time to fall_timemax_jerkfloatMaximum rate of change of acceleration (m/s³)negative_spikefloatMaximum downward acceleration spikepeak_amplitudefloatPeak vertical acceleration magnitudemax_yaw_ratefloatMaximum yaw angular velocity (°/s)max_pitch_ratefloatMaximum pitch angular velocity (°/s)gyro_accel_correlationfloatCorrelation between gyroscope and accelerometerpitch_symmetryfloatSymmetry of pitch motion during bump eventlabel (target)int0 = Normal Road · 1 = Speed Breaker · 2 = Pothole

🚀 API Endpoints
GET /
json{ "message": "RoadSense AI Backend is Online" }
POST /record-bump
Request:
json{ "max_jerk": 12.5, "lat": 28.6139, "lon": 77.2090 }
Response:
json{ "status": "success", "analysis": "Pothole", "severity": 12.5 }
analysisMeaningNormal_RoadSmooth surface — no anomalySpeed_BreakerSpeed breaker classifiedPotholePothole — repair priority triggered
GET /top-10-roads
json{
  "priority_segments": [
    { "segment_id": "ST-101", "health_score": 45 },
    { "segment_id": "ST-202", "health_score": 88 }
  ]
}
Lower health_score (0–100) = worse condition = higher repair priority.

⚙️ Quick Start
bashgit clone https://github.com/ShwetaRawat09/roadsense_backend.git
cd roadsense_backend

python -m venv venv
.\venv\Scripts\activate        # Windows
source venv/bin/activate       # macOS / Linux

pip install -r requirements.txt
python train_model.py          # optional: retrain model
uvicorn main:app --reload
API → http://localhost:8000 | Swagger docs → http://localhost:8000/docs
Frontend
bashnpm install && npm run dev

📦 Dependencies
joblib==1.5.3        numpy==2.4.4
pandas==3.0.3        scikit-learn==1.8.0
scipy==1.17.1        tzdata==2026.2

🧪 Test the API
bashcurl http://localhost:8000/

curl -X POST http://localhost:8000/record-bump \
  -H "Content-Type: application/json" \
  -d '{"max_jerk": 14.2, "lat": 28.6139, "lon": 77.2090}'

curl http://localhost:8000/top-10-roads

📊 Dataset
roadsense_10k_dataset.csv — 10,000 synthetic sensor records across 3 classes:
ClassDescriptionNormal RoadBaseline vibration — no anomalySpeed BreakerControlled bump, symmetric rise/fallPotholeSharp asymmetric jerk spike, high negative amplitude

🗺️ Roadmap
PhaseStatusKey AdditionsPhase 1 — POC✅ CompleteFastAPI + RandomForest on max_jerk + 10K CSV + React/LeafletPhase 2 — Beta🔄 Planned13-feature model · passive mobile app · PostgreSQL + PostGISPhase 3 — Scale📋 FutureXGBoost 90-day forecast · Open-Meteo rainfall · multi-city

👥 Team — LogicWeave
