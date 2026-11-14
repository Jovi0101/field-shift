"""Contrato: análise de rotação (Integrante 02 produz, Integrante 04 consome)."""
from pydantic import BaseModel, Field, model_validator


class Priorities(BaseModel):
    soil_health: int = Field(ge=0, le=100, default=25)
    water_efficiency: int = Field(ge=0, le=100, default=25)
    climate_resilience: int = Field(ge=0, le=100, default=25)
    diversification: int = Field(ge=0, le=100, default=25)

    @model_validator(mode="after")
    def must_sum_100(self) -> "Priorities":
        total = self.soil_health + self.water_efficiency + self.climate_resilience + self.diversification
        if total != 100:
            raise ValueError(f"priorities must sum to 100 (got {total})")
        return self


class RotationAnalyzeRequest(BaseModel):
    farm_id: str = Field(examples=["farm-001"])
    priorities: Priorities = Field(default_factory=Priorities)


class Recommendation(BaseModel):
    strategy: str = Field(examples=["Alternative A"])
    score: int = Field(ge=0, le=100)
    crops: list[str]
    benefits: list[str] = Field(default_factory=list)
    risks: list[str] = Field(default_factory=list)


class RotationAnalyzeResponse(BaseModel):
    farm_id: str
    recommendations: list[Recommendation]
    is_mock: bool = False
