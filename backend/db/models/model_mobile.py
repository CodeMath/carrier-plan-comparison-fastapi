from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.sql.schema import Column
from db.base_class import Base


class Mobile(Base):
    __tablename__ = "mobile"

    id = Column(Integer, primary_key=True, autoincrement=True)
    price = Column(Integer, nullable=False)
    plan = Column(String(100), nullable=False)
    url = Column(String(255), nullable=True)
    carrier = Column(String(100), nullable=False)
