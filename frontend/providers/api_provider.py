
# frontend/providers/api_provider.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL", "http://localhost:8000")
API_KEY = os.getenv("API_KEY", "chave-local-dev")
APP_VERSION = os.getenv("APP_VERSION", "1.3.0")

import uuid
_SESSION_ID = str(uuid.uuid4())  # um por processo — poderia ser por aba, se o Gradio suportar
_TIMEOUT = 10


def _headers(feature: str) -> dict:
    return {
        "X-API-Key": API_KEY,
        "X-Session-Id": _SESSION_ID,
        "X-App-Version": APP_VERSION,
        "X-Feature": feature,
        "X-Client-Platform": "gradio-desktop",
    }


def _get(path: str, feature: str, params: dict | None = None):
    try:
        r = requests.get(f"{API_URL}{path}", headers=_headers(feature), params=params, timeout=_TIMEOUT)
        r.raise_for_status()
        return r.json()
    except requests.ConnectionError:
        print(f"[api_provider] Não foi possível conectar ao back-end em {API_URL}.")
        return None
    except requests.HTTPError as e:
        if e.response.status_code == 404:
            return None
        print(f"[api_provider] Erro {e.response.status_code} em {path}: {e.response.text}")
        return None


# cada chamada agora identifica de qual feature ela vem
def listar_todos() -> list[dict]:
    return _get("/v1/equipamentos", feature="equipamentos") or []


def leitura_atual(tag: str) -> dict:
    return _get(f"/v1/sensores/{tag}/leitura-atual", feature="sensores") or {}


def listar_equipamentos(planta: str, area: str) -> list[str]:
    return _get(f"/v1/plantas/{planta}/areas/{area}/equipamentos", feature="dashboard") or []
    
def historico_simulado(tag: str, n_pontos: int = 48) -> list[dict]:
    return _get(f"/v1/sensores/{tag}/historico", feature="sensores", params={"n": n_pontos}) or []
    
def get_observabilidade():
    return _get(f"/v1/observabilidade", feature="observabilidade") or []
