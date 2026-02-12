SysMonitor API
Una API REST construida con FastAPI para simular el monitoreo de servidores y el manejo de alertas.

El objetivo de este proyecto es tener un sistema centralizado donde se puedan registrar servidores y recibir sus métricas (CPU, RAM, Disco). Si un servidor supera ciertos umbrales (por ejemplo, 85% de CPU), la API detecta la anomalía y genera una alerta.

Cómo funciona
El sistema tiene dos partes principales:

Inventario: Un CRUD para registrar servidores. Valida que las IPs sean correctas y que el SO sea válido (Linux, Windows, MacOS).

Métricas: Un endpoint que recibe el estado de salud de los servidores. Si recibe un uso de recursos crítico, marca el reporte con alert_triggered: True.

Tecnologías
Python 3.10+

FastAPI: Para la creación de la API y documentación automática.

Pydantic: Para la validación estricta de datos (Schemas).

Pytest: Para los tests de integración y unitarios.

Instalación y Uso
Prepara el entorno: Crea un entorno virtual e instala las dependencias.

Bash
pip install -r requirements.txt
Levanta el servidor:

Bash
uvicorn app.main:app --reload
La API correrá en http://127.0.0.1:8000.

Documentación: Puedes probar todos los endpoints directamente desde Swagger UI en: http://127.0.0.1:8000/docs

Tests
El proyecto cuenta con tests de integración para asegurar que el flujo de registro y alertas funciona bien.

Bash
pytest --cov=app tests/
Nota sobre la Base de Datos
Actualmente, el proyecto utiliza persistencia en archivos JSON (servers_db.json y metrics_db.json). Tomé esta decisión para que el proyecto sea portable y fácil de ejecutar sin necesidad de configurar una base de datos local como PostgreSQL. En un entorno de producción real, esto se sustituiría por una base de datos relacional para el inventario y una TimeSeries DB (como InfluxDB) para las métricas.