# ??? RoadSense: Telemetry Analytics System

A full-stack application designed to analyze road quality using high-frequency sensor telemetry.

## ??? The Architecture (4-Layer Model)
1. **API Layer (FastAPI):** Handles requests and CORS security.
2. **Service Layer:** Orchestrates business logic and decision-making.
3. **Processing Layer:** Performs mathematical clustering on jerk and amplitude data.
4. **Data Layer (Pandas):** Ingests and queries 10,000+ records from CSV.

## ?? Quick Start
### Backend
1. `python -m venv venv`
2. `.\venv\Scripts\activate`
3. `pip install -r requirements.txt`
4. `uvicorn main:app --reload`

### Frontend (React + Vite)
1. `npm install`
2. `npm run dev`

## ?? Features
- **Spatial Mapping:** Interactive OpenStreetMap using Leaflet.
- **Data Visualization:** Real-time health distribution charts via Recharts.
- **Dynamic Analysis:** Automated road health scoring based on sensor jerk rates.
