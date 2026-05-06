from db import queries
from processors import event_processor

def _decide_if_pothole(telemetry_data) -> bool:
    if telemetry_data.max_jerk > 15.0 and telemetry_data.peak_amplitude > 5.0:
        return True
    return False

def process_new_event(event_payload):
    is_pothole = _decide_if_pothole(event_payload)
    event_dict = event_payload.model_dump()
    event_id = queries.insert_road_event(event_dict)
    return {"status": "success", "event_id": event_id, "classified_as_pothole": is_pothole}

def calculate_road_health_score(lat: float, lon: float):
    raw_events = queries.fetch_events_within_10m(lat, lon)
    cluster_data = event_processor.cluster_gps_events(lat, lon, raw_events)
    health_score = 100 - (cluster_data["average_jerk"] if cluster_data else 0)
    return {"health_score": round(health_score, 2)}

def get_top_priority_roads(ward_id: int):
    top_roads = queries.fetch_top_roads_by_ward(ward_id)
    return {"ward_id": ward_id, "priority_segments": top_roads}
