from pydantic import BaseModel, HttpUrl, Field
from typing import Union


class InternatCombination(BaseModel):
    internet: str
    price: int = Field(default=0, ge=0)
    speed: int = Field(default=0, ge=0)
    wifi: int = Field(default=0, ge=0)

    class Config:
        schema_extra = {
            "example": {"internet": "slim", "price": 0, "speed": 0, "wifi": 0}
        }


class PlanKT(BaseModel):
    price: int = Field(default=0, ge=0)
    title: str
    eng_title: str
    url: HttpUrl
    carrier: str

    class Config:
        schema_extra = {
            "example": {
                "price": 100000,
                "title": "스페셜",
                "eng_title": "special",
                "url": "https://kt.com",
                "carrier": "5G",
            }
        }


class PlanKTinDB(PlanKT):
    class Config:
        orm_mode = True


class CombinationRule(BaseModel):
    name: str
    carrier_line: int = Field(default=1)
    is_flat_discount: bool = Field(default=False)
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


class LineDiscount(PlanKT):
    contract_discount: float = Field(default=0.25, ge=0)
    combination_rule: Union[CombinationRule, None] = None
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


class CombinedDiscount(BaseModel):
    base_line: LineDiscount
    other_line: Union[list[LineDiscount], None] = None
    internet: InternatCombination
    sum_payment: int = Field(default=0, ge=0)


class SumDiscountCombination(BaseModel):
    mobile_plan_list: list[LineDiscount]
    mobile_discount: int = Field(default=0, ge=0)
    internet: Union[InternatCombination, None] = None
    internet_discount: int = Field(default=0, ge=0)


class ComparisonPlan(BaseModel):
    family_pay: int = Field(default=0, ge=0)
    sum_pay: int = Field(default=0, ge=0)
    family_plan: Union[CombinedDiscount, None] = None
    sum_plan: Union[SumDiscountCombination, None] = None


class Carriers(BaseModel):
    mobile_line: list[str]
    internet_line: str


class Internets(BaseModel):
    internet: str
    eng_internet: str
    price: int
    speed: int
    wifi: int
