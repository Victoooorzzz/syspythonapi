from fastapi import FastAPI
from app.api.endpoints import servers, metrics

app = FastAPI(
    title="SysMonitor API v2 (Persistent)",
    description="API de monitoreo con persistencia JSON.",
    version="2.0.0"
)

app.include_router(servers.router, prefix="/api/v1/servers", tags=["Servers"])
app.include_router(metrics.router, prefix="/api/v1/metrics", tags=["Metrics"])

@app.get("/")
def health_check():
    return {"status": "ok", "system": "SysMonitor v2 Running"}