from fastapi import APIRouter, HTTPException, status
from typing import List
from app.schemas.server import ServerCreate, ServerResponse
from app.db import get_all_servers, save_server

router = APIRouter()

@router.post("/", response_model=ServerResponse, status_code=status.HTTP_201_CREATED)
def register_server(server: ServerCreate):
    current_servers = get_all_servers()
    
    # Validar duplicados por Hostname
    for s in current_servers:
        if s["hostname"] == server.hostname:
            raise HTTPException(status_code=400, detail="Hostname already exists")

    # Generar ID incremental
    new_id = 1
    if current_servers:
        new_id = current_servers[-1]["id"] + 1

    # Preparar objeto para guardar
    new_server = server.model_dump()
    new_server["id"] = new_id
    new_server["status"] = "active"
    new_server["ip_address"] = str(new_server["ip_address"]) # IP a string para JSON
    
    # Guardar en disco
    save_server(new_server)
    
    return new_server

@router.get("/", response_model=List[ServerResponse])
def list_servers():
    return get_all_servers()

@router.get("/{server_id}", response_model=ServerResponse)
def get_server(server_id: int):
    servers = get_all_servers()
    for server in servers:
        if server["id"] == server_id:
            return server
    raise HTTPException(status_code=404, detail="Server not found")