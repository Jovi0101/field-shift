import pandas as pd

from src.models.dashboard import Indicator, Strategy


def get_indicators() -> list[Indicator]:
    """Retorna indicadores fictícios para a primeira versão da interface."""
    return [
        Indicator("Temperatura média", "24,8", "°C", "Média do período selecionado."),
        Indicator("Precipitação acumulada", "142", "mm", "Chuva acumulada no período selecionado."),
        Indicator("Umidade do solo", "68", "%", "Estimativa fictícia da umidade do solo."),
        Indicator("Risco climático", "Moderado", "", "Classificação demonstrativa; validar com dados reais."),
    ]


def get_historical_data() -> pd.DataFrame:
    """Série mensal fictícia de temperatura e precipitação."""
    return pd.DataFrame(
        {
            "Mês": ["Dez", "Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov"],
            "Temperatura (°C)": [25.1, 25.8, 25.4, 24.7, 23.8, 22.1, 20.5, 20.2, 21.6, 23.0, 24.2, 24.9],
            "Precipitação (mm)": [180, 210, 165, 142, 110, 72, 48, 42, 55, 88, 125, 160],
        }
    )


def get_strategies() -> list[Strategy]:
    """Estratégias fictícias para demonstrar comparação e ranking."""
    return [
        Strategy(
            name="Milho → Soja → Cobertura",
            score=87,
            rotation="Milho → Soja → Braquiária",
            estimated_yield=8.4,
            water_use=640,
            soil_health="Alta",
            justification="Combina culturas comerciais com cobertura do solo e apresenta bom equilíbrio entre produtividade e uso de água.",
            risks=[
                "O resultado depende da janela de plantio.",
                "A estimativa de produtividade precisa ser validada para a região.",
            ],
        ),
        Strategy(
            name="Soja → Milho",
            score=79,
            rotation="Soja → Milho",
            estimated_yield=7.8,
            water_use=710,
            soil_health="Média",
            justification="Alternativa simples de implementar, com duas culturas comerciais na rotação.",
            risks=[
                "Maior exposição a períodos secos durante o ciclo.",
                "Menor diversidade de culturas que a estratégia recomendada.",
            ],
        ),
        Strategy(
            name="Milho → Cobertura",
            score=72,
            rotation="Milho → Braquiária",
            estimated_yield=6.9,
            water_use=590,
            soil_health="Alta",
            justification="Prioriza a cobertura do solo e apresenta menor uso estimado de água.",
            risks=[
                "Pode gerar menor receita comercial no curto prazo.",
                "A escolha da cobertura depende do objetivo da propriedade.",
            ],
        ),
    ]
