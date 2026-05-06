from pydantic import BaseModel

class EventPayload(BaseModel):
    lat: float
    lon: float
    duration: float
    rise_time: float
    fall_time: float
    rise_fall_ratio: float
    max_jerk: float
    negative_spike: float
    peak_amplitude: float
    max_yaw_rate: float
    max_pitch_rate: float
    gyro_accel_correlation: float
    pitch_symmetry: float
