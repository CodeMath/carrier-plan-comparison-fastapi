from pydantic import BaseModel, HttpUrl, Field

"""
##### Mobile #####
"""


class Internet(BaseModel):
    title: str
    price: int
    speed: int
    wifi: int

    class Config:
        schema_extra = {
            "example": {
                "title": "슬림",
                "price": 20900,
                "speed": "100",
                "wifi": 0,
            }
        }


class InternetList(BaseModel):
    """List Internet"""

    total: int = 0
    mobiel_list: list[Internet] = []


class CreateInternet_Schema(Internet):
    """Create Internet Schema"""

    class Config:
        orm_mode = True


class UpdateInternet_Schema(Internet):
    internet_id: int


class DeleteInternet_Schema(Internet):
    internet_id: int
