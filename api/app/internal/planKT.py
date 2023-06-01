from pydantic import BaseModel, HttpUrl
from typing import Union


class PlanKT(BaseModel):
    name: str
    price: int
    title: Union[str, None] = None
    url: Union[HttpUrl, None] = None
    carrier: str

    class Config:
        schema_extra = {
            "example": {
                "name": "Special",
                "price": 100000,
                "title": "스페셜",
                "url": "kt.com",
                "carrier": "5G",
            }
        }


fake_plan = [
    {"name": "choice_premiem", "price": 130000, "title": "초이스 프리미엄", "carrier": "5G"},
    {"name": "choice_special", "price": 110000, "title": "초이스 스페셜", "carrier": "5G"},
    {"name": "choice_basic", "price": 90000, "title": "초이스 베이직", "carrier": "5G"},
    {"name": "special", "price": 100000, "title": "스페셜", "carrier": "5G"},
    {"name": "special_Y", "price": 100000, "title": "스페셜Y", "carrier": "5G"},
    {"name": "basic", "price": 80000, "title": "베이직", "carrier": "5G"},
    {"name": "basic_Y", "price": 80000, "title": "베이직Y", "carrier": "5G"},
    {
        "name": "data_on_premiem",
        "price": 89000,
        "title": "데이터 온 프리미엄",
        "carrier": "LTE",
    },
    {
        "name": "data_on_premiem_Y",
        "price": 89000,
        "title": "데이터 온 프리미엄",
        "carrier": "LTE",
    },
]


class CombinedDiscount(BaseModel):
    name: str
    base_line: PlanKT
    other_lines: Union[list[PlanKT], None] = None
    base_discount: float
    other_discount: Union[float, None] = None
    internet_discount: Union[float, None] = None


fake_combination = [
    {
        "name": "single",
        "title": "프리미엄 싱글 결합",
        "base_line": {
            "name": "data_on_premiem",
            "price": 89000,
            "title": "데이터 온 프리미엄",
            "carrier": "LTE",
        },
        "base_discount": 0.25,
    }
]
