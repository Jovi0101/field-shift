"""O clima do local (NASA POWER) precisa mudar as notas do motor de rotação.

Nenhum teste chama a internet: climate_service.get_climate é substituído via monkeypatch.
"""
import pytest
from fastapi.testclient import TestClient

from app.integrations.nasa.power_client import NasaPowerError
from app.schemas.climate import ClimateResponse, Location, MonthlyClimate
from app.services import climate_service
from main import app

client = TestClient(app)


def _seasonal(summer: tuple[float, float], winter: tuple[float, float]) -> dict:
    """Monta 12 meses (hemisfério sul): out-mar = verão, abr-set = inverno. Tuplas = (°C, mm/dia)."""
    monthly = [
        MonthlyClimate(month=f"2024-{m:02d}", temperature_c=t, precipitation_mm_day=p)
        for m in range(1, 13)
        for t, p in [summer if m in (10, 11, 12, 1, 2, 3) else winter]
    ]
    return {
        "temperature_avg_c": round(sum(m.temperature_c for m in monthly) / 12, 2),
        "precipitation_avg_mm_day": round(sum(m.precipitation_mm_day for m in monthly) / 12, 2),
        "monthly": monthly,
    }


# Valores aproximados: Santa Maria/RS (úmido, ameno) e sertão nordestino (seco, quente).
SUBTROPICAL = _seasonal(summer=(23.6, 4.8), winter=(15.0, 4.4))  # média 19.3 °C, 4.6 mm/dia
SEMIARID = _seasonal(summer=(27.0, 1.6), winter=(25.5, 0.8))

PRIORITIES = {"soil_health": 25, "water_efficiency": 25, "climate_resilience": 25, "diversification": 25}


def _farm(latitude: float, longitude: float) -> dict:
    return {
        "name": "Farm Clima",
        "latitude": latitude,
        "longitude": longitude,
        "area_hectares": 50,
        "soil_type": "clay",
        "irrigation": False,
        "previous_crops": ["soybean"],
    }


def _fake_climate(by_latitude: dict[float, dict], is_mock: bool = False):
    def get_climate(latitude: float, longitude: float) -> ClimateResponse:
        return ClimateResponse(
            location=Location(latitude=latitude, longitude=longitude),
            period="2020-2024",
            is_mock=is_mock,
            **by_latitude[latitude],
        )

    return get_climate


def _analyze(latitude: float, longitude: float) -> dict:
    farm_id = client.post("/api/v1/farms", json=_farm(latitude, longitude)).json()["id"]
    res = client.post("/api/v1/rotation/analyze", json={"farm_id": farm_id, "priorities": PRIORITIES})
    assert res.status_code == 200
    return res.json()


def _criteria_by_strategy(body: dict) -> dict[str, dict[str, int]]:
    return {rec["strategy"]: rec["criteria"] for rec in body["recommendations"]}


def test_different_climates_change_water_and_climate_scores(monkeypatch):
    monkeypatch.setattr(climate_service, "get_climate", _fake_climate({-29.7: SUBTROPICAL, -9.4: SEMIARID}))

    wet = _analyze(-29.7, -52.4)
    dry = _analyze(-9.4, -40.5)
    wet_criteria, dry_criteria = _criteria_by_strategy(wet), _criteria_by_strategy(dry)

    for strategy, wet_scores in wet_criteria.items():
        dry_scores = dry_criteria[strategy]
        # Menos chuva e mais calor => notas menores; os demais critérios não dependem do clima.
        assert dry_scores["water_efficiency"] < wet_scores["water_efficiency"], strategy
        assert dry_scores["climate_resilience"] < wet_scores["climate_resilience"], strategy
        assert dry_scores["soil_health"] == wet_scores["soil_health"]
        assert dry_scores["diversification"] == wet_scores["diversification"]

    assert wet["is_mock"] is False and dry["is_mock"] is False
    rationale = " ".join(wet["recommendations"][0]["rationale"])
    assert "1679 mm/year" in rationale  # 4.6 mm/day x 365
    assert "19.3 °C" in rationale
    assert "summer 23.6 °C" in rationale and "winter 15.0 °C" in rationale


def test_without_monthly_data_uses_annual_average(monkeypatch):
    annual_only = {"temperature_avg_c": 26.0, "precipitation_avg_mm_day": 1.0}
    monkeypatch.setattr(climate_service, "get_climate", _fake_climate({-9.4: annual_only}))
    rationale = " ".join(_analyze(-9.4, -40.5)["recommendations"][0]["rationale"])
    assert "summer 26.0 °C and 1.00 mm/day" in rationale


def test_semiarid_reports_water_deficit_risk(monkeypatch):
    monkeypatch.setattr(climate_service, "get_climate", _fake_climate({-9.4: SEMIARID}))
    body = _analyze(-9.4, -40.5)
    risks = " ".join(r for rec in body["recommendations"] for r in rec["risks"])
    assert "below the minimum water demand" in risks


def test_nasa_failure_falls_back_to_base_scores(monkeypatch):
    def broken(latitude: float, longitude: float) -> ClimateResponse:
        raise NasaPowerError("NASA POWER request failed: timeout")

    monkeypatch.setattr(climate_service, "get_climate", broken)
    body = _analyze(-29.7, -52.4)

    criteria = _criteria_by_strategy(body)
    # Notas base da estratégia + ajustes de solo argiloso sem irrigação (milho: -5 de água).
    assert criteria["Winter cover"]["water_efficiency"] == 65
    assert criteria["Winter cover"]["climate_resilience"] == 84
    assert criteria["Wheat income"]["water_efficiency"] == 78
    assert criteria["Wheat income"]["climate_resilience"] == 73
    for rec in body["recommendations"]:
        assert any("currently unavailable" in line for line in rec["rationale"])


@pytest.mark.parametrize("is_mock", [True, False])
def test_rotation_is_mock_follows_climate(monkeypatch, is_mock):
    monkeypatch.setattr(climate_service, "get_climate", _fake_climate({-29.7: SUBTROPICAL}, is_mock=is_mock))
    assert _analyze(-29.7, -52.4)["is_mock"] is is_mock
