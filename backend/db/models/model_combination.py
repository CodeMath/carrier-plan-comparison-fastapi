from sqlalchemy import (
    Column,
    Integer,
    String,
    BIGINT,
    Boolean,
    Float,
    ForeignKey,
    DateTime,
)
from sqlalchemy.sql.schema import Column
from db.base_class import Base
from sqlalchemy.orm import relationship, Mapped
from db.models.model_mobile import Mobile
from db.models.model_internet import Internet


class CombinationRule(Base):
    __tablename__ = "combination_rule"

    id = Column(BIGINT, primary_key=True, autoincrement=True)
    carrier_line = Column(Integer, nullable=False, default=1)
    name = Column(String(50), nullable=False)
    is_flat_discount = Column(Boolean(default=False))
    combination_discount = Column(Float, nullable=False, default=0)


class CombinationSingle(Base):
    __tablename__ = "combiantion_single"

    id = Column(BIGINT, primary_key=True, autoincrement=True)
    create_time = Column(DateTime, nullable=False)
    base_line_id = Column(Mobile, ForeignKey("Mobile.id", ondelete="CASCADE"))
    base_line = relationship("Mobile")

    internet_id = Column(Internet, ForeignKey("Internet.id", ondelete="CASCADE"))
    internet = relationship("Internet")
    sum_payment = Column(Integer, default=0, nullalbe=False)


class SumCombinationRule(Base):
    __tablename__ = "sum_combination_rule"

    id = Column(BIGINT, primary_key=True, autoincrement=True)
    st_range = Column(Integer, default=0, nullable=False)
    ed_range = Column(Integer, default=0, nullable=False)
    mobile_discount = Column(Integer, default=0, nullable=False)
    is_internet_slim = Column(Boolean(default=False))
    internet_discount = Column(Integer, default=0, nullable=False)
