"""Cliente da NASA POWER API — dono: Integrante 01.

Docs: https://power.larc.nasa.gov/docs/services/api/temporal/monthly/
Não precisa de chave de API.
"""
import httpx

from app.core.config import settings

PARAMETERS = "T2M,PRECTOTCORR"  # temperatura 2 m (°C), precipitação corrigida (mm/dia)


class NasaPowerError(Exception):
    pass


def fetch_monthly_point(latitude: float, longitude: float, start_year: int, end_year: int) -> dict:
    """Retorna o JSON bruto da NASA POWER (endpoint mensal, comunidade AG).

    O cache por coordenada fica em climate_service. TODO (Integrante 01): retry em falhas temporárias.
    """
    url = f"{settings.nasa_power_base_url}/temporal/monthly/point"
    params = {
        "parameters": PARAMETERS,
        "community": "AG",
        "latitude": latitude,
        "longitude": longitude,
        "start": start_year,
        "end": end_year,
        "format": "JSON",
    }
    try:
        response = httpx.get(url, params=params, timeout=30)
        response.raise_for_status()
    except httpx.HTTPError as exc:
        raise NasaPowerError(f"NASA POWER request failed: {exc}") from exc
    return response.json()
