from sqlalchemy import Column, Integer, ForeignKey, BIGINT, DateTime, String
from sqlalchemy.sql.schema import Column
from db.base_class import Base
from sqlalchemy.orm import relationship, Mapped
from typing import List
from models.model_mobile import Mobile
from models.model_combination import CombinationRule


class ResultBoard(Base):
    __tablename__ = "result_board"

    id = Column(BIGINT, primary_key=True, autoincrement=True)
    create_time = Column(DateTime, nullable=False)
    title = Column(String(100), nullalbe=False)

    combination_rule_id = Column(
        CombinationRule, ForeignKey("CombinationRule.id", ondelete="CASCADE")
    )
    combination_rule = relationship("CombinationRule")

    initial_price = Column(Integer, default=0, nullable=False)
    discount_price = Column(Integer, default=0, nullable=False)
    result_price = Column(Integer, default=0, nullable=False)

    mobile_id = Column(Integer, ForeignKey("Mobile.id", ondelete="CASCADE"))
    mobile = relationship("Mobile")

    internet_id = Column(Integer, ForeignKey("Internet.id", ondelete="CASCADE"))
    internet = relationship("Internet")

    other_mobile = relationship("Mobile")
