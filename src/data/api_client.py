"""Cliente HTTP do backend Field Shift (FastAPI).

URL base configurável por FIELD_SHIFT_API_URL (padrão: http://localhost:8000/api/v1).
"""
import os

import requests

API_URL = os.getenv("FIELD_SHIFT_API_URL", "http://localhost:8000/api/v1").rstrip("/")
TIMEOUT = (3, 90)  # (conexão, leitura) — a primeira chamada à NASA POWER pode levar alguns segundos


class BackendUnavailable(Exception):
    """Backend fora do ar ou inacessível."""


class BackendError(Exception):
    """Backend respondeu com erro (4xx/5xx)."""

    def __init__(self, status_code: int, detail: str) -> None:
        super().__init__(f"{status_code}: {detail}")
        self.status_code = status_code
        self.detail = detail


def _request(method: str, path: str, **kwargs) -> dict | list:
    try:
        response = requests.request(method, f"{API_URL}{path}", timeout=TIMEOUT, **kwargs)
    except (requests.ConnectionError, requests.Timeout) as exc:
        raise BackendUnavailable(f"Could not connect to {API_URL}: {exc.__class__.__name__}") from exc
    if not response.ok:
        try:
            detail = response.json().get("detail", response.text)
        except ValueError:
            detail = response.text
        raise BackendError(response.status_code, str(detail))
    return response.json()


def health() -> bool:
    """True se o backend responde em /health (fica fora do prefixo /api/v1)."""
    base = API_URL.removesuffix("/api/v1")
    try:
        return requests.get(f"{base}/health", timeout=2).ok
    except requests.RequestException:
        return False


def list_farms() -> list[dict]:
    return _request("GET", "/farms")


def create_farm(farm: dict) -> dict:
    return _request("POST", "/farms", json=farm)


def get_climate(latitude: float, longitude: float) -> dict:
    return _request("GET", "/environment/climate", params={"latitude": latitude, "longitude": longitude})


def list_crops() -> list[dict]:
    return _request("GET", "/crops")


def analyze_rotation(farm_id: str, priorities: dict[str, int]) -> dict:
    return _request("POST", "/rotation/analyze", json={"farm_id": farm_id, "priorities": priorities})
