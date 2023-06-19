from pydantic import BaseModel, HttpUrl, Field

"""
##### Mobile #####
"""


class Mobile(BaseModel):
    price: int = Field(default=0, ge=0)
    plan: str
    url: HttpUrl
    carrier: str

    class Config:
        schema_extra = {
            "example": {
                "price": 100000,
                "plan": "스페셜",
                "url": "https://kt.com",
                "carrier": "5G",
            }
        }


class MobileList(BaseModel):
    total: int = 0
    mobiel_list: list[Mobile] = []


class CreateMobile_Schema(Mobile):
    """Create Plan Schemas"""

    class Config:
        orm_mode = True


class UpdateMobile_Schema(CreateMobile_Schema):
    mobile_id: int


class DeleteMobile_Schema(Mobile):
    mobile_id: int
