from fastapi import APIRouter, HTTPException, status
from typing import List
from datetime import datetime
from app.schemas.metric import MetricReceive, MetricResponse
from app.db import get_all_servers, get_all_metrics, save_metric

router = APIRouter()

@router.post("/{server_id}/report", response_model=MetricResponse, status_code=status.HTTP_201_CREATED)
def ingest_metric(server_id: int, metric: MetricReceive):
    # 1. Validar que el servidor existe (Leyendo el archivo de servidores)
    servers = get_all_servers()
    server_exists = any(s["id"] == server_id for s in servers)
    
    if not server_exists:
        raise HTTPException(status_code=404, detail="Server not registered")

    # 2. Lógica de Alerta "DevOps"
    is_critical = False
    if metric.cpu_usage > 85.0 or metric.ram_usage > 90.0:
        is_critical = True

    # 3. Guardar Métrica
    new_metric = metric.model_dump()
    new_metric["server_id"] = server_id
    new_metric["timestamp"] = datetime.now()
    new_metric["alert_triggered"] = is_critical

    save_metric(new_metric)
    
    return new_metric

@router.get("/alerts", response_model=List[MetricResponse])
def get_critical_alerts():
    """Retorna solo las métricas que dispararon alerta."""
    metrics = get_all_metrics()
    alerts = [m for m in metrics if m["alert_triggered"] is True]
    return alerts