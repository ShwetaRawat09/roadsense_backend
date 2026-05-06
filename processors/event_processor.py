def cluster_gps_events(lat: float, lon: float, raw_events: list):
    if not raw_events:
        return None
    
    avg_jerk = sum(e["max_jerk"] for e in raw_events) / len(raw_events)
    
    return {
        "cluster_center": {"lat": lat, "lon": lon},
        "event_count": len(raw_events),
        "average_jerk": avg_jerk
    }

def compute_equity_score(ward_events: list) -> float:
    base_score = 100.0
    severity_penalty = sum(e.get("peak_amplitude", 0) * 0.5 for e in ward_events)
    return max(0.0, base_score - severity_penalty)
