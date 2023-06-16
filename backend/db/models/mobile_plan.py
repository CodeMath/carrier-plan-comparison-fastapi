from sqlalchemy import Column, ForeignKey, Integer, String, BIGINT
from sqlalchemy.sql.schema import Column
from pydantic import BaseModel
from db.base_class import Base
from typing import Union


class PlanKT_model(Base):
    __tablename__ = "PlanKT"

    id = Column(BIGINT, primary_key=True, autoincrement=True)
    price = Column(Integer, nullable=False)
    title = Column(String(100), nullable=False)
    eng_title = Column(String(100), nullable=False)
    url = Column(String(255), nullable=True, default="")
    carrier = Column(String(100), nullable=False)
