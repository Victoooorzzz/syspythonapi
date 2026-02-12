import json
import os
from typing import List, Any

# Nombres de nuestros archivos "Base de Datos"
SERVERS_FILE = "servers_db.json"
METRICS_FILE = "metrics_db.json"

def _load_json(filename: str) -> List[Any]:
    """Función privada para leer un archivo JSON de forma segura."""
    if not os.path.exists(filename):
        return []
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []

def _save_json(filename: str, data: List[Any]):
    """Función privada para guardar datos en un archivo JSON."""
    with open(filename, "w") as f:
        # default=str convierte objetos complejos (como fechas) a texto
        json.dump(data, f, indent=4, default=str)

# --- Funciones Públicas para Servidores ---
def get_all_servers():
    return _load_json(SERVERS_FILE)

def save_server(server_data: dict):
    servers = get_all_servers()
    servers.append(server_data)
    _save_json(SERVERS_FILE, servers)

# --- Funciones Públicas para Métricas ---
def get_all_metrics():
    return _load_json(METRICS_FILE)

def save_metric(metric_data: dict):
    metrics = get_all_metrics()
    metrics.append(metric_data)
    _save_json(METRICS_FILE, metrics)