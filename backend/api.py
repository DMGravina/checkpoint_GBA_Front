from fastapi import FastAPI, Request
from pydantic import BaseModel
import time
from typing import Dict, Any

app = FastAPI(title="Forzy Sensor API", version="1.0.0")

# Simulando um banco de dados de sensores com a telemetria atual
sensores_db = {
    "MTR-001": {
        "tensao_v": 220,
        "corrente_a": 15.5,
        "temp_c": 45.2,
        "vibracao_mms": 1.2,
        "rotacao_rpm": 1750,
        "severidade_temp": "Normal",
        "severidade_vibracao": "Normal"
    }
}

# Simulando histórico de leituras
historico_db = {
    "MTR-001": [
        {"timestamp": "2026-10-14T08:00:00Z", "temp_c": 45.0, "vibracao_mms": 1.1},
        {"timestamp": "2026-10-14T08:01:00Z", "temp_c": 45.1, "vibracao_mms": 1.2},
        {"timestamp": "2026-10-14T08:02:00Z", "temp_c": 45.2, "vibracao_mms": 1.2}
    ]
}

# Lista em memória para armazenar os logs de observabilidade (rastreabilidade)
observabilidade_logs = []

# Middleware para interceptar as requisições e calcular métricas de Governança
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    # Extraindo os headers de contexto injetados pelo front-end
    session_id = request.headers.get("X-Session-Id", "N/A")
    feature = request.headers.get("X-Feature", "N/A")
    client_platform = request.headers.get("X-Client-Platform", "N/A")
    app_version = request.headers.get("X-App-Version", "N/A")
    
    # Registrando o log apenas nas rotas focadas no checkpoint
    if request.url.path.startswith("/v1/sensores") or request.url.path == "/v1/observabilidade":
        log_entry = {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "path": request.url.path,
            "method": request.method,
            "status_code": response.status_code,
            "latency_ms": round(process_time * 1000, 2), # Latência em milissegundos
            "session_id": session_id,
            "feature": feature,
            "client_platform": client_platform,
            "app_version": app_version
        }
        observabilidade_logs.append(log_entry)
        
    return response

@app.get("/v1/sensores/{tag}/leitura-atual")
def obter_leitura_atual(tag: str) -> Dict[str, Any]:
    if tag in sensores_db:
        return sensores_db[tag]
    return {"erro": "Sensor não encontrado"}

@app.get("/v1/sensores/{tag}/historico")
def obter_historico(tag: str, n: int = 48) -> list:
    if tag in historico_db:
        return historico_db[tag][-n:]
    return []

@app.get("/v1/observabilidade")
def obter_observabilidade() -> list:
    return observabilidade_logs

if __name__ == "__main__":
    import uvicorn
    # Executar a aplicação (ex: uvicorn api:app --reload)
    uvicorn.run(app, host="0.0.0.0", port=8000)