from sqlalchemy import Column, Integer, ForeignKey, BIGINT, DateTime, String
from sqlalchemy.sql.schema import Column
from db.base_class import Base
from sqlalchemy.orm import relationship, Mapped
from typing import List
from db.models.model_mobile import Mobile
from db.models.model_combination import CombinationRule


class ResultBoard(Base):
    __tablename__ = "result_board"

    id = Column(Integer, primary_key=True, autoincrement=True)
    create_time = Column(DateTime, nullable=False)
    title = Column(String(100), nullable=False)

    combination_rule_id = Column(Integer, ForeignKey("combination_rule.id"))
    combination_rule = relationship("CombinationRule")

    initial_price = Column(Integer, nullable=False)
    discount_price = Column(Integer, nullable=False)
    result_price = Column(Integer, nullable=False)

    mobile_id = Column(Integer, ForeignKey("mobile.id"))
    mobile = relationship("Mobile")

    internet_id = Column(Integer, ForeignKey("internet.id"))
    internet = relationship("Internet")

    other_mobile = relationship("Mobile")
