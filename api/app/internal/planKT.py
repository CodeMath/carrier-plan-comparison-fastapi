from pydantic import BaseModel, HttpUrl, Field
from typing import Union


class PlanKT(BaseModel):
    price: int = Field(default=0, ge=0)
    title: Union[str, None] = None
    url: Union[HttpUrl, None] = None
    carrier: str

    class Config:
        schema_extra = {
            "example": {
                "price": 100000,
                "title": "스페셜",
                "url": "kt.com",
                "carrier": "5G",
            }
        }


fake_plan = {
    "choice_premiem": {"price": 130000, "title": "초이스 프리미엄", "carrier": "5G"},
    "choice_special": {"price": 110000, "title": "초이스 스페셜", "carrier": "5G"},
    "choice_basic": {"price": 90000, "title": "초이스 베이직", "carrier": "5G"},
    "special": {"price": 100000, "title": "스페셜", "carrier": "5G"},
    "special_Y": {"price": 100000, "title": "스페셜Y", "carrier": "5G"},
    "basic": {"price": 80000, "title": "베이직", "carrier": "5G"},
    "basic_Y": {"price": 80000, "title": "베이직Y", "carrier": "5G"},
    "data_on_premiem": {
        "price": 89000,
        "title": "데이터 온 프리미엄",
        "carrier": "LTE",
    },
    "data_on_premiem_Y": {
        "price": 89000,
        "title": "데이터 온 프리미엄",
        "carrier": "LTE",
    },
}


class CombinedDiscount(BaseModel):
    name: str = Field(default="choice_premiem", title="eng) choice_premiem")
    title: str
    base_line: PlanKT
    is_flat_discount: bool = Field(default=False)
    base_discount: Union[float, int] = Field(default=0, ge=0)
    other_discount: Union[float, None] = Field(default=0, ge=0)
    internet_discount: Union[int, None] = Field(default=0, ge=0)


fake_combination = [
    {
        "name": "single",
        "title": "프리미엄 싱글 결합",
        "is_flat_discount": False,
        "base_discount": 0.25,
        "other_discount": 0,
        "internet_discount": 0,
    },
    {
        "name": "family",
        "title": "프리미엄 가족 결합",
        "is_flat_discount": True,
        "base_discount": 11000,
        "other_discount": 0.25,
        "internet_discount": 0,
    },
]


class InternatCombination(BaseModel):
    internet: str
    price: int = Field(default=0, ge=0)
    speed: int = Field(default=0, ge=0)


fake_internet = {
    "slim": {"internet": "슬림", "price": 20900, "speed": 100},
    "slim_plus": {"internet": "슬림 플러스", "price": 30250, "speed": 200},
    "basic": {"internet": "베이직", "price": 31350, "speed": 500},
    "essense": {"internet": "에센스", "price": 36300, "speed": 1000},
    "premien": {"internet": "프리미엄", "price": 41250, "speed": 2500},
    "premien_plus": {"internet": "프리미엄플러스", "price": 56650, "speed": 5000},
    "super_premien": {"internet": "슈퍼프리미엄", "price": 82500, "speed": 10000},
}


class SumDiscountCombination(BaseModel):
    mobile_sum_price: list[int]
    mobile_discount: int = Field(default=0, ge=0)
    internet: str = Field(default="슬림")
    internet_discount: int = Field(default=0, ge=0)


fake_sum_combination = [
    {
        "mobile_sum_price": [0, 22000],
        "mobile_discount": 0,
        "internet": "슬림",
        "internet_discount": 1650,
    },
    {
        "mobile_sum_price": [0, 22000],
        "mobile_discount": 0,
        "internet": "no슬림",
        "internet_discount": 2200,
    },
    {
        "mobile_sum_price": [22000, 64899],
        "mobile_discount": 5500,
        "internet": "슬림",
        "internet_discount": 5500,
    },
    {
        "mobile_sum_price": [22000, 64899],
        "mobile_discount": 0,
        "internet": "no슬림",
        "internet_discount": 3300,
    },
    {
        "mobile_sum_price": [64900, 108899],
        "mobile_discount": 3300,
        "internet": "슬림",
        "internet_discount": 5500,
    },
    {
        "mobile_sum_price": [64900, 108899],
        "mobile_discount": 5500,
        "internet": "no슬림",
        "internet_discount": 5500,
    },
    {
        "mobile_sum_price": [108900, 141899],
        "mobile_discount": 14300,
        "internet": "슬림",
        "internet_discount": 5500,
    },
    {
        "mobile_sum_price": [108900, 141899],
        "mobile_discount": 16610,
        "internet": "no슬림",
        "internet_discount": 5500,
    },
    {
        "mobile_sum_price": [141900, 174899],
        "mobile_discount": 18700,
        "internet": "슬림",
        "internet_discount": 5500,
    },
    {
        "mobile_sum_price": [141900, 174899],
        "mobile_discount": 22110,
        "internet": "no슬림",
        "internet_discount": 5500,
    },
    {
        "mobile_sum_price": [174900, 999999],
        "mobile_discount": 23100,
        "internet": "슬림",
        "internet_discount": 5500,
    },
    {
        "mobile_sum_price": [174900, 999999],
        "mobile_discount": 27610,
        "internet": "no슬림",
        "internet_discount": 5500,
    },
]
