"""Período climático dinâmico: últimos 5 anos completos, com recuo de 1 ano se o END_YEAR não estiver publicado.

Nenhum teste chama a internet: fetch_monthly_point é substituído via monkeypatch.
"""
from datetime import date

import pytest
from fastapi.testclient import TestClient

from app.integrations.nasa.power_client import NasaPowerError
from app.services import climate_service
from main import app

client = TestClient(app)
REAL_CLIMATE_PERIOD = climate_service._climate_period  # antes do monkeypatch do fixture
CLIMATE_URL = "/api/v1/environment/climate"
PARAMS = {"latitude": -29.717, "longitude": -52.425}


def _nasa_payload(
    start_year: int, end_year: int, missing_years: set[int] = frozenset(), missing_months: set[str] = frozenset()
) -> dict:
    """Resposta no formato da NASA POWER; anos/meses ausentes vêm com -999 (ainda não publicados).

    missing_months usa o formato da NASA, ex.: {"202510", "202511"}.
    """
    t2m, prec = {}, {}
    for year in range(start_year, end_year + 1):
        for month in range(1, 13):
            key = f"{year}{month:02d}"
            missing = year in missing_years or key in missing_months
            t2m[key] = -999.0 if missing else 20.0
            prec[key] = -999.0 if missing else 3.0
        t2m[f"{year}13"], prec[f"{year}13"] = 20.0, 3.0  # média anual, ignorada
    return {"properties": {"parameter": {"T2M": t2m, "PRECTOTCORR": prec}}, "messages": []}


@pytest.fixture(autouse=True)
def real_mode(monkeypatch):
    monkeypatch.setattr(climate_service.settings, "use_mock_climate", False)
    monkeypatch.setattr(climate_service, "_climate_period", lambda: (2021, 2025))
    climate_service._get_real_climate.cache_clear()
    yield
    climate_service._get_real_climate.cache_clear()


@pytest.fixture
def calls(monkeypatch):
    """Registra os períodos pedidos à NASA; cada teste define a resposta em calls.respond."""
    recorded: list[tuple[int, int]] = []

    def fake_fetch(latitude, longitude, start_year, end_year):
        recorded.append((start_year, end_year))
        return fake_fetch.respond(start_year, end_year)

    monkeypatch.setattr(climate_service, "fetch_monthly_point", fake_fetch)
    fake_fetch.recorded = recorded
    return fake_fetch


@pytest.mark.parametrize(
    ("today", "expected"),
    [(date(2026, 11, 15), (2021, 2025)), (date(2027, 1, 1), (2022, 2026)), (date(2026, 12, 31), (2021, 2025))],
)
def test_period_is_last_five_complete_years(today, expected):
    assert REAL_CLIMATE_PERIOD(today) == expected


def test_uses_current_period_when_end_year_is_published(calls):
    calls.respond = lambda start, end: _nasa_payload(start, end)
    res = client.get(CLIMATE_URL, params=PARAMS)
    assert res.status_code == 200
    assert res.json()["period"] == "2021-2025"
    assert calls.recorded == [(2021, 2025)]


def test_falls_back_one_year_when_end_year_has_no_data(calls):
    # NASA responde 200, mas 2025 todo com -999 (ano ainda não publicado).
    calls.respond = lambda start, end: _nasa_payload(start, end, missing_years={2025})
    res = client.get(CLIMATE_URL, params=PARAMS)
    assert res.status_code == 200
    body = res.json()
    assert body["period"] == "2020-2024"
    assert body["monthly"][-1]["month"] == "2024-12"
    assert calls.recorded == [(2021, 2025), (2020, 2024)]


def test_falls_back_one_year_when_end_year_is_incomplete(calls):
    # Como o 2026 real hoje: jan-set publicados, out-dez ainda -999. Ano incompleto distorce a média.
    calls.respond = lambda start, end: _nasa_payload(start, end, missing_months={"202510", "202511", "202512"})
    res = client.get(CLIMATE_URL, params=PARAMS)
    assert res.status_code == 200
    body = res.json()
    assert body["period"] == "2020-2024"
    assert len(body["monthly"]) == 60
    assert calls.recorded == [(2021, 2025), (2020, 2024)]


def test_falls_back_one_year_when_nasa_returns_error(calls):
    def respond(start, end):
        if end == 2025:
            raise NasaPowerError("NASA POWER request failed: 422")
        return _nasa_payload(start, end)

    calls.respond = respond
    res = client.get(CLIMATE_URL, params=PARAMS)
    assert res.status_code == 200
    assert res.json()["period"] == "2020-2024"
    assert calls.recorded == [(2021, 2025), (2020, 2024)]


def test_retries_only_once(calls):
    def always_fail(start, end):
        raise NasaPowerError("NASA POWER request failed: 500")

    calls.respond = always_fail
    res = client.get(CLIMATE_URL, params=PARAMS)
    assert res.status_code == 502
    assert calls.recorded == [(2021, 2025), (2020, 2024)]


def test_mock_mode_uses_dynamic_period(monkeypatch):
    monkeypatch.setattr(climate_service.settings, "use_mock_climate", True)
    body = client.get(CLIMATE_URL, params=PARAMS).json()
    assert body["is_mock"] is True
    assert body["period"] == "2021-2025"
    assert body["monthly"][0]["month"] == "2025-01"
