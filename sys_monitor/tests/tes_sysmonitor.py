import os
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Configuración: Borrar DBs antes de cada test para empezar limpio
@pytest.fixture(autouse=True)
def clean_db():
    if os.path.exists("servers_db.json"):
        os.remove("servers_db.json")
    if os.path.exists("metrics_db.json"):
        os.remove("metrics_db.json")
    yield

def test_monitoring_flow():
    # 1. Registrar servidor
    server_payload = {
        "hostname": "test-server",
        "ip_address": "10.0.0.1",
        "os_family": "linux",
        "tags": ["test"]
    }
    response = client.post("/api/v1/servers/", json=server_payload)
    assert response.status_code == 201
    server_id = response.json()["id"]

    # 2. Verificar que se guardó (Persistencia)
    get_res = client.get(f"/api/v1/servers/{server_id}")
    assert get_res.status_code == 200
    assert get_res.json()["hostname"] == "test-server"

    # 3. Enviar Alerta Crítica
    metric_critical = {"cpu_usage": 95.0, "ram_usage": 50.0, "disk_usage": 20.0}
    res_crit = client.post(f"/api/v1/metrics/{server_id}/report", json=metric_critical)
    assert res_crit.status_code == 201
    assert res_crit.json()["alert_triggered"] is True

    # 4. Verificar endpoint de alertas
    alerts = client.get("/api/v1/metrics/alerts").json()
    assert len(alerts) == 1