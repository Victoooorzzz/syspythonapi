from pydantic import BaseModel, IPvAnyAddress, Field
from typing import List
from enum import Enum

class OSFamily(str, Enum):
    LINUX = "linux"
    WINDOWS = "windows"
    MACOS = "macos"

class ServerBase(BaseModel):
    hostname: str = Field(..., min_length=3, example="web-prod-01")
    ip_address: IPvAnyAddress
    os_family: OSFamily
    tags: List[str] = []

class ServerCreate(ServerBase):
    pass

class ServerResponse(ServerBase):
    id: int
    status: str = "active"