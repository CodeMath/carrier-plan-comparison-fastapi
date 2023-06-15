from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.sql.schema import Column
from pydantic import BaseModel
from db.base_class import Base
from typing import Union


class PlanKT_model(Base):
    __tablename__ = "PlanKT"

    id = Column(Integer, primary_key=True)
    price = Column(Integer, nullable=False)
    title = Column(String(100), nullable=False)
    eng_title = Column(String(100), nullable=False)
    url = Column(String(255), nullable=True, default="")
    carrier = Column(String(100), nullable=False)
