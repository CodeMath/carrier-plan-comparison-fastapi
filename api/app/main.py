from fastapi import FastAPI, HTTPException, APIRouter
from enum import Enum
from .router import combination, plan_list

app = FastAPI()
app.include_router(plan_list.router)
app.include_router(combination.router)
