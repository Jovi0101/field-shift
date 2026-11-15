"""Serviço climático — dono: Integrante 01.

Busca dados mensais reais na NASA POWER (últimos 5 anos completos) e converte para o contrato.
Com USE_MOCK_CLIMATE=true devolve dados fixos (útil sem internet).
"""
from datetime import date
from functools import lru_cache

from app.core.config import settings
from app.integrations.nasa.power_client import NasaPowerError, fetch_monthly_point
from app.schemas.climate import ClimateResponse, Location, MonthlyClimate

PERIOD_YEARS = 5
# END_YEAR só vale se tiver os 12 meses: ano incompleto distorce a média (ex.: falta o verão).
REQUIRED_END_YEAR_MONTHS = 12
MISSING = -999.0  # fill_value da NASA POWER


def _climate_period(today: date | None = None) -> tuple[int, int]:
    """(START_YEAR, END_YEAR): END_YEAR = ano atual - 1 (último ano completo), 5 anos no total.

    Os testes substituem esta função para controlar a data.
    """
    end_year = (today or date.today()).year - 1
    return end_year - (PERIOD_YEARS - 1), end_year


def get_climate(latitude: float, longitude: float) -> ClimateResponse:
    start_year, end_year = _climate_period()
    if settings.use_mock_climate:
        return _mock_climate(latitude, longitude, start_year, end_year)
    # A grade da NASA POWER tem ~0.5°; arredondar evita chamadas repetidas para o mesmo ponto.
    lat, lon = round(latitude, 3), round(longitude, 3)
    try:
        return _get_real_climate(lat, lon, start_year, end_year)
    except NasaPowerError:
        # END_YEAR pode ainda não estar completo (a NASA devolve -999): recua o período 1 ano, uma única vez.
        return _get_real_climate(lat, lon, start_year - 1, end_year - 1)


@lru_cache(maxsize=256)
def _get_real_climate(latitude: float, longitude: float, start_year: int, end_year: int) -> ClimateResponse:
    raw = fetch_monthly_point(latitude, longitude, start_year, end_year)
    climate = _normalize(raw, latitude, longitude, start_year, end_year)
    end_year_months = sum(1 for m in climate.monthly if m.month.startswith(f"{end_year}-"))
    if end_year_months < REQUIRED_END_YEAR_MONTHS:
        raise NasaPowerError(
            f"NASA POWER has only {end_year_months}/12 valid months for {end_year}; the year is not complete yet"
        )
    return climate


def _normalize(raw: dict, latitude: float, longitude: float, start_year: int, end_year: int) -> ClimateResponse:
    """Converte o JSON da NASA para o contrato.

    O endpoint mensal devolve chaves YYYYMM e também YYYY13 (média anual) — essas são ignoradas.
    """
    try:
        params = raw["properties"]["parameter"]
        temps: dict[str, float] = params["T2M"]
        precs: dict[str, float] = params["PRECTOTCORR"]
    except (KeyError, TypeError) as exc:
        messages = raw.get("messages") if isinstance(raw, dict) else None
        raise NasaPowerError(f"Unexpected NASA POWER response (missing {exc}); messages={messages}") from exc

    monthly: list[MonthlyClimate] = []
    for key in sorted(temps):
        if len(key) != 6 or key.endswith("13"):
            continue
        t, p = temps[key], precs.get(key, MISSING)
        if t is None or p is None or t == MISSING or p == MISSING:
            continue
        monthly.append(MonthlyClimate(month=f"{key[:4]}-{key[4:]}", temperature_c=t, precipitation_mm_day=p))

    if not monthly:
        raise NasaPowerError("NASA POWER returned no valid monthly data for this location")

    n = len(monthly)
    return ClimateResponse(
        location=Location(latitude=latitude, longitude=longitude),
        period=f"{start_year}-{end_year}",
        temperature_avg_c=round(sum(m.temperature_c for m in monthly) / n, 2),
        precipitation_avg_mm_day=round(sum(m.precipitation_mm_day for m in monthly) / n, 2),
        monthly=monthly,
    )


def _mock_climate(latitude: float, longitude: float, start_year: int, end_year: int) -> ClimateResponse:
    temps = [25.1, 24.8, 23.2, 20.0, 16.9, 14.3, 13.8, 15.4, 16.9, 19.6, 21.9, 24.1]
    precs = [4.6, 4.9, 4.1, 4.8, 4.4, 4.7, 5.0, 4.2, 5.1, 6.0, 4.3, 4.5]
    monthly = [
        MonthlyClimate(month=f"{end_year}-{i + 1:02d}", temperature_c=t, precipitation_mm_day=p)
        for i, (t, p) in enumerate(zip(temps, precs))
    ]
    return ClimateResponse(
        location=Location(latitude=latitude, longitude=longitude),
        period=f"{start_year}-{end_year}",
        temperature_avg_c=round(sum(temps) / 12, 2),
        precipitation_avg_mm_day=round(sum(precs) / 12, 2),
        monthly=monthly,
        is_mock=True,
    )
