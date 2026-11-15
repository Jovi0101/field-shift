"""Testes de contrato: garantem que as rotas respeitam o formato combinado.

Rodar a partir de field-shift-backend/:  pytest
"""
import pytest
from fastapi.testclient import TestClient

from app.services import climate_service
from main import app

client = TestClient(app)

# Recorte real da NASA POWER (lat -29.717, lon -52.425), incluindo a chave anual "202013" e um -999.
NASA_SAMPLE = {
    "properties": {
        "parameter": {
            "T2M": {"202001": 24.08, "202002": 23.89, "202003": -999.0, "202013": 18.82},
            "PRECTOTCORR": {"202001": 4.31, "202002": 1.1, "202003": 0.71, "202013": 3.02},
        }
    },
    "messages": [],
}


@pytest.fixture(autouse=True)
def offline_nasa(monkeypatch):
    """Os testes nunca chamam a NASA de verdade: usam o recorte acima."""
    monkeypatch.setattr(climate_service.settings, "use_mock_climate", False)
    monkeypatch.setattr(climate_service, "fetch_monthly_point", lambda *args: NASA_SAMPLE)
    climate_service._get_real_climate.cache_clear()

FARM = {
    "name": "Farm Demo",
    "latitude": -29.717,
    "longitude": -52.425,
    "area_hectares": 120,
    "soil_type": "clay",
    "irrigation": False,
    "previous_crops": ["soybean", "corn"],
}


def test_health():
    assert client.get("/health").json() == {"status": "ok"}


def test_create_and_get_farm():
    created = client.post("/api/v1/farms", json=FARM)
    assert created.status_code == 201
    body = created.json()
    assert body["id"].startswith("farm-")
    assert client.get(f"/api/v1/farms/{body['id']}").json() == body


def test_climate_contract():
    res = client.get("/api/v1/environment/climate", params={"latitude": -29.717, "longitude": -52.425})
    assert res.status_code == 200
    body = res.json()
    for key in ("location", "period", "temperature_avg_c", "precipitation_avg_mm_day", "monthly", "source"):
        assert key in body
    assert body["is_mock"] is False


def test_nasa_normalization_skips_annual_and_missing():
    body = client.get("/api/v1/environment/climate", params={"latitude": -29.717, "longitude": -52.425}).json()
    assert [m["month"] for m in body["monthly"]] == ["2020-01", "2020-02"]
    assert body["temperature_avg_c"] == round((24.08 + 23.89) / 2, 2)
    assert body["precipitation_avg_mm_day"] == round((4.31 + 1.1) / 2, 2)


def test_bad_nasa_response_returns_502(monkeypatch):
    monkeypatch.setattr(climate_service, "fetch_monthly_point", lambda *args: {"messages": ["error"]})
    res = client.get("/api/v1/environment/climate", params={"latitude": 1, "longitude": 1})
    assert res.status_code == 502


def test_rotation_contract():
    farm_id = client.post("/api/v1/farms", json=FARM).json()["id"]
    res = client.post(
        "/api/v1/rotation/analyze",
        json={
            "farm_id": farm_id,
            "priorities": {"soil_health": 30, "water_efficiency": 25, "climate_resilience": 25, "diversification": 20},
        },
    )
    assert res.status_code == 200
    rec = res.json()["recommendations"][0]
    assert {"strategy", "score", "crops", "criteria", "benefits", "risks", "rationale"} <= rec.keys()
    assert res.json()["is_mock"] is False


def test_catalog_contract():
    res = client.get("/api/v1/crops")
    assert res.status_code == 200
    assert {"id", "name", "family", "season", "nitrogen_fixing", "water_demand"} <= res.json()[0].keys()


def test_priority_changes_ranking():
    farm_id = client.post("/api/v1/farms", json=FARM).json()["id"]
    soil_first = client.post(
        "/api/v1/rotation/analyze",
        json={"farm_id": farm_id, "priorities": {"soil_health": 70, "water_efficiency": 10, "climate_resilience": 10, "diversification": 10}},
    ).json()
    diversity_first = client.post(
        "/api/v1/rotation/analyze",
        json={"farm_id": farm_id, "priorities": {"soil_health": 10, "water_efficiency": 10, "climate_resilience": 10, "diversification": 70}},
    ).json()
    assert soil_first["recommendations"][0]["strategy"] == "Winter cover"
    assert diversity_first["recommendations"][0]["strategy"] == "Bean diversification"


def test_priorities_must_sum_100():
    farm_id = client.post("/api/v1/farms", json=FARM).json()["id"]
    res = client.post(
        "/api/v1/rotation/analyze",
        json={"farm_id": farm_id, "priorities": {"soil_health": 90, "water_efficiency": 90,
                                                  "climate_resilience": 0, "diversification": 0}},
    )
    assert res.status_code == 422


def test_unknown_farm_returns_404():
    res = client.post("/api/v1/rotation/analyze", json={"farm_id": "nope"})
    assert res.status_code == 404
