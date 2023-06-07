from fastapi import FastAPI, HTTPException, APIRouter
from enum import Enum
from .router import combination, plan_list
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:8080",
    "http://localhost:8081",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(plan_list.router)
app.include_router(combination.router)
