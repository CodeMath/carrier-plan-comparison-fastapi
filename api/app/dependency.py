from fastapi import Depends, Header, HTTPException
from typing import Union
from typing_extensions import Annotated

# KT Dependency
carrier_type = {"all": {"tp": "all"}, "5g": {"tp": "5g"}, "lte": {"tp": "lte"}}


async def router_get_token_headeer(x_token: Annotated[str, Header()]):
    if x_token != "fake-secret-token-value":
        raise HTTPException(status_code=400, detail="X-Token header invalid")
