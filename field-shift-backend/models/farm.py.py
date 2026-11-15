from sqlalchemy import Column, Integer, String, Float
from database import Base

class FarmModel(Base):
    __tablename__ = "farms"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    area_hectares = Column(Float, nullable=False)
    soil_type = Column(String, nullable=False)