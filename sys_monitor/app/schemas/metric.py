from pydantic import BaseModel, Field
from datetime import datetime

class MetricReceive(BaseModel):
    cpu_usage: float = Field(..., ge=0, le=100)
    ram_usage: float = Field(..., ge=0, le=100)
    disk_usage: float = Field(..., ge=0, le=100)

class MetricResponse(MetricReceive):
    server_id: int
    timestamp: datetime
    alert_triggered: bool = False