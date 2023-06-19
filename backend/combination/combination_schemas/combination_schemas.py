from pydantic import BaseModel, Field
from typing import Union
from internet.internet_schemas import Internet
from .base_combination_schemas import LineDiscount

"""
##### Combination BaseModel #####
"""


class Combination(BaseModel):
    """싱글 결합 & 가족 결합"""

    base_line: LineDiscount
    other_line: Union[list[LineDiscount], None] = None  # None is "싱글 결합"
    internet: Internet
    sum_payment: int = Field(default=0, ge=0)

    class Config:
        schema_extra = {
            "example": {
                "base_line": {
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
                },
                "other_line": [
                    {
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
                ],
                "internet": {
                    "internet": "슬림",
                    "eng_internet": "slim",
                    "price": 20900,
                    "speed": "100",
                    "wifi": 0,
                },
                "sum_payment": 0,
            }
        }


class SumCombination(BaseModel):
    """총액 결합"""

    mobile_plan_list: list[LineDiscount]
    mobile_discount: int = Field(default=0, ge=0)
    internet: Union[Internet, None] = None
    internet_discount: int = Field(default=0, ge=0)

    class Config:
        schema_extra = {
            "example": {
                "mobile_plan_list": [
                    {
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
                    },
                    {
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
                    },
                ],
                "mobile_discount": 0,
                "internet": {
                    "internet": "슬림",
                    "eng_internet": "slim",
                    "price": 20900,
                    "speed": "100",
                    "wifi": 0,
                },
                "internet_discount": 0,
            }
        }


class ComparisonCombination(BaseModel):
    """가족결합 vs 총액결합"""

    family_pay: int = Field(default=0, ge=0)
    sum_pay: int = Field(default=0, ge=0)
    family_plan: Union[Combination, None] = None
    sum_plan: Union[SumCombination, None] = None


"""
##### Combination Schemas #####
"""


class CreateCombination_Schema(Combination):
    class Config:
        orm_mode = True


class CreateSumCombination_Schema(SumCombination):
    class Config:
        orm_mode = True


class CreateComparisonCombination_Schema(ComparisonCombination):
    class Config:
        orm_mode = True


class Carriers(BaseModel):
    """1) 가족결합 -> 2) 총액결합 API 콜 각각 하면 굳이 아래는 필요할까?"""

    mobile_line: list[str]
    internet_line: str
