# Field Shift API contracts (draft)

These are integration contracts for the MVP, derived from the team brief. The example scores and values are illustrative, not agronomic advice. Keep the frontend and backend aligned to these shapes; refine fields together before implementation.

Base path: `/api/v1`. JSON request and response bodies. Errors use FastAPI's standard `detail` response unless the team adopts a shared error schema.

## Create a farm

`POST /api/v1/farms`

```json
{
  "name": "Farm Demo",
  "latitude": -29.717,
  "longitude": -52.425,
  "area_hectares": 120,
  "soil_type": "clay",
  "irrigation": false,
  "previous_crops": ["soybean", "corn"]
}
```

`201 Created`

```json
{
  "id": "farm-001",
  "name": "Farm Demo",
  "latitude": -29.717,
  "longitude": -52.425,
  "area_hectares": 120,
  "soil_type": "clay",
  "irrigation": false,
  "previous_crops": ["soybean", "corn"]
}
```

## Climate summary

`GET /api/v1/environment/climate?latitude=-29.717&longitude=-52.425`

```json
{
  "location": { "latitude": -29.717, "longitude": -52.425 },
  "period": "2020-2025",
  "temperature_avg_c": 22.5,
  "precipitation_avg_mm": 145.2,
  "source": "NASA POWER"
}
```

The units and aggregation window must be confirmed by the NASA integration owner. Keep source and units explicit in the implemented schema.

## Analyze crop rotation

`POST /api/v1/rotation/analyze`

```json
{
  "farm_id": "farm-001",
  "priorities": {
    "soil_health": 30,
    "water_efficiency": 25,
    "climate_resilience": 25,
    "diversification": 20
  }
}
```

`200 OK`

```json
{
  "recommendations": [
    {
      "strategy": "Alternative A",
      "score": 87,
      "crops": ["soybean", "oats", "corn"],
      "benefits": ["Crop diversification", "Soil coverage"],
      "risks": ["Water availability must be verified"]
    }
  ]
}
```

The priority weights in a request should total 100; the backend validates this. Recommendation content and scores are owned by the agronomic engine and must not be presented as scientific findings without validation.

## Integration checklist

- Agree crop IDs, soil values, required fields, date range, and units with module owners.
- The farm creation response's `id` is the `farm_id` consumed by rotation analysis.
- Backend exposes OpenAPI at `/docs` and `/openapi.json` during development.
- Keep demo fixtures deterministic so the full demo does not depend on a live NASA request.
