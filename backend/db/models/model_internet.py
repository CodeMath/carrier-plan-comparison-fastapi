from sqlalchemy import Column, Integer, BIGINT, String
from sqlalchemy.sql.schema import Column
from db.base_class import Base
from sqlalchemy.orm import validates, Mapped, mapped_column


class Internet(Base):
    __tablename__ = "internet"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    price: Mapped[int] = mapped_column(default=0)
    speed: Mapped[int] = mapped_column(default=0)
    wifi: Mapped[int] = mapped_column(default=0)

    @validates("wifi")
    def validate_wifi(self, k, v):
        if v > 3 or v < 0:
            raise ValueError("Greater then 0 and Less then 3")
        return v
