from fastapi import Depends, Header, HTTPException
from typing import Union
from typing_extensions import Annotated

# KT Dependency
exclude_res_model = response_model_exclude_unset = True


class CarrierPlanQueryParams:
    def __init__(
        self,
        price: Union[int, None] = None,
        tp: str = "all",
    ):
        self.price = price
        self.tp = tp


async def router_get_token_headeer(x_token: Annotated[str, Header()]):
    if x_token != "fake-secret-token-value":
        raise HTTPException(status_code=400, detail="X-Token header invalid")
