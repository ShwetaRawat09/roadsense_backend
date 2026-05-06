from fastapi import APIRouter
from models import EventPayload
from services import road_service

router = APIRouter()

@router.post("/report-event")
def report_event(event: EventPayload):
    response = road_service.process_new_event(event)
    return response

@router.get("/road-health")
def get_road_health(lat: float, lon: float):
    response = road_service.calculate_road_health_score(lat, lon)
    return response

@router.get("/top-10-roads")
def get_top_roads(ward_id: int):
    response = road_service.get_top_priority_roads(ward_id)
    return response
