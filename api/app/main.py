from fastapi import FastAPI, HTTPException, APIRouter
from enum import Enum
from .router import user_plan

app = FastAPI()
app.include_router(user_plan.router)


@app.get("/")
async def root():
    return {"messsage": "Hello"}
