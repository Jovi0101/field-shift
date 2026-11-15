import pandas as pd

from src.models.dashboard import Indicator, Strategy


def get_indicators() -> list[Indicator]:
    """Retorna indicadores fictícios para a primeira versão da interface."""
    return [
        Indicator("Average temperature", "24.8", "°C", "Average for the selected period."),
        Indicator("Accumulated rainfall", "142", "mm", "Accumulated rainfall for the selected period."),
        Indicator("Soil moisture", "68", "%", "Fictional soil moisture estimate."),
        Indicator("Climate risk", "Moderate", "", "Demo classification; validate with real data."),
    ]


def get_historical_data() -> pd.DataFrame:
    """Série mensal fictícia de temperatura e precipitação."""
    return pd.DataFrame(
        {
            "Month": ["Dec", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov"],
            "Temperature (°C)": [25.1, 25.8, 25.4, 24.7, 23.8, 22.1, 20.5, 20.2, 21.6, 23.0, 24.2, 24.9],
            "Precipitation (mm)": [180, 210, 165, 142, 110, 72, 48, 42, 55, 88, 125, 160],
        }
    )


def get_strategies() -> list[Strategy]:
    """Estratégias fictícias para demonstrar comparação e ranking."""
    return [
        Strategy(
            name="Corn → Soybean → Cover crop",
            score=87,
            rotation="Corn → Soybean → Brachiaria",
            estimated_yield=8.4,
            water_use=640,
            soil_health="High",
            justification="Combines cash crops with soil cover and balances yield and water use well.",
            risks=[
                "The result depends on the planting window.",
                "The yield estimate needs to be validated for the region.",
            ],
        ),
        Strategy(
            name="Soybean → Corn",
            score=79,
            rotation="Soybean → Corn",
            estimated_yield=7.8,
            water_use=710,
            soil_health="Medium",
            justification="A simple option to implement, with two cash crops in the rotation.",
            risks=[
                "Greater exposure to dry spells during the cycle.",
                "Lower crop diversity than the recommended strategy.",
            ],
        ),
        Strategy(
            name="Corn → Cover crop",
            score=72,
            rotation="Corn → Brachiaria",
            estimated_yield=6.9,
            water_use=590,
            soil_health="High",
            justification="Prioritizes soil cover and has a lower estimated water use.",
            risks=[
                "May generate less commercial revenue in the short term.",
                "The choice of cover crop depends on the farm's goals.",
            ],
        ),
    ]
