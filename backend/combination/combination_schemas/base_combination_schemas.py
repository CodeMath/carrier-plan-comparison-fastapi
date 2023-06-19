from pydantic import BaseModel, Field
from typing import Union
from schemas.plan_schemas import Mobile


"""
##### Base Combination #####
"""


class CombinationRule(BaseModel):
    name: str
    carrier_line: int = Field(default=1)
    is_flat_discount: bool = Field(
        default=False,
    )  # if flat, dicsount money(int), but %(float)
    combination_discount: Union[float, int] = Field(default=0, ge=0)

    class Config:
        schema_extra = {
            "example": {
                "name": "싱글 결합",
                "carrier_line": 1,
                "is_flat_discount": False,
                "combination_discount": 0.25,
            }
        }


class CreateCombinationRule_Schema(CombinationRule):
    class Config:
        orm_mode = True


class LineDiscount(Mobile):
    """
    각 회선 별 할인률 계산
    """

    contract_discount: float = Field(default=0.25, ge=0)
    combination_rule: Union[CombinationRule, None] = None  # 없을 경우 None
    mobile_pay: int

    class Config:
        schema_extra = {
            "example": {
                "price": 100000,
                "title": "스페셜",
                "url": "kt.com",
                "carrier": "5G",
                "contract_discount": 0.25,
                "combination_rule": {
                    "name": "싱글 결합",
                    "carrier_line": 1,
                    "is_flat_discount": False,
                    "combination_discount": 0.25,
                },
                "mobile_pay": 50000,
            }
        }


class CreateLineDiscount_Schema(LineDiscount):
    class Config:
        orm_mode = True
