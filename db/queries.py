import pandas as pd
import random

# 1. Load the dataset
try:
    import os; df = pd.read_csv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "roadsense_10k_dataset.csv"))
    telemetry_db = df.to_dict(orient="records")
    print(f"--- Successfully loaded {len(telemetry_db)} records ---")
except Exception as e:
    print("Warning: Could not load CSV.", e)
    telemetry_db = []
    df = pd.DataFrame()

def get_db_connection(): pass 

def insert_road_event(event_data: dict) -> int: return random.randint(1000, 9999)

def fetch_events_within_10m(lat: float, lon: float):
    if not telemetry_db: return []
    return random.sample(telemetry_db, random.randint(5, 20))

def fetch_top_roads_by_ward(ward_id: int):
    """
    Fetches road segments. 
    If 'lat' and 'lon' columns exist in your CSV, it uses them.
    Otherwise, it stays in Chennai for the simulation.
    """
    if df.empty: return []
    
    segments = []
    # Check if the CSV actually has GPS columns
    has_real_gps = 'lat' in df.columns and 'lon' in df.columns
    
    # Fallback coordinates (Chennai)
    base_lat, base_lon = 13.0827, 80.2707
    
    # Grab 10 samples from your data
    sample_size = min(len(df), 10)
    top_data = df.sample(sample_size)
    
    for i, (_, row) in enumerate(top_data.iterrows()):
        # Calculate health: higher jerk = lower health score
        jerk = row.get('max_jerk', 0)
        health = max(0.0, 100.0 - (jerk * 0.5)) # Adjusted formula for better spread
        
        segments.append({
            "segment_id": f"RD-{ward_id}-{100 + i}",
            "health_score": round(health, 2),
            "lat": row['lat'] if has_real_gps else base_lat + random.uniform(-0.08, 0.08),
            "lon": row['lon'] if has_real_gps else base_lon + random.uniform(-0.08, 0.08)
        })
        
    return sorted(segments, key=lambda x: x["health_score"])
