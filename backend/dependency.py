from fastapi import Header, HTTPException
from typing_extensions import Annotated
from db.session import SessionLocal


# Database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# get Token
async def router_get_token_headeer(x_token: Annotated[str, Header()]):
    if x_token != "fake-secret-token-value":
        raise HTTPException(status_code=400, detail="X-Token header invalid")
