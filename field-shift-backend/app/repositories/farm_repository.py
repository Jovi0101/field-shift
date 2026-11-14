"""Armazenamento de propriedades.

MVP: em memória (perde os dados ao reiniciar). Troque por SQLAlchemy + Postgres
depois do marco de 60% sem mudar a interface pública (create/get/list_all).
"""
from app.schemas.farm import FarmCreate, FarmRead


class InMemoryFarmRepository:
    def __init__(self) -> None:
        self._farms: dict[str, FarmRead] = {}
        self._seq = 0

    def create(self, data: FarmCreate) -> FarmRead:
        self._seq += 1
        farm = FarmRead(id=f"farm-{self._seq:03d}", **data.model_dump())
        self._farms[farm.id] = farm
        return farm

    def get(self, farm_id: str) -> FarmRead | None:
        return self._farms.get(farm_id)

    def list_all(self) -> list[FarmRead]:
        return list(self._farms.values())


farm_repository = InMemoryFarmRepository()
