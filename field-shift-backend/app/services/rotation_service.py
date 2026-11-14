"""Motor agronômico — dono: Integrante 02.

Hoje devolve recomendações fixas no formato do contrato (is_mock=True).
TODO (Integrante 02): gerar estratégias a partir de CROPS + clima + solo,
pontuar cada critério (0-100) e combinar com os pesos de `priorities`.
"""
from app.schemas.farm import FarmRead
from app.schemas.rotation import Priorities, Recommendation, RotationAnalyzeResponse


def analyze(farm: FarmRead, priorities: Priorities) -> RotationAnalyzeResponse:
    recommendations = [
        Recommendation(
            strategy="Alternative A",
            score=87,
            crops=["soybean", "oats", "corn"],
            benefits=["Crop diversification", "Soil coverage"],
            risks=["Water availability must be verified"],
        ),
        Recommendation(
            strategy="Alternative B",
            score=74,
            crops=["soybean", "wheat", "soybean"],
            benefits=["Winter income"],
            risks=["Low family diversity"],
        ),
    ]
    return RotationAnalyzeResponse(farm_id=farm.id, recommendations=recommendations, is_mock=True)
