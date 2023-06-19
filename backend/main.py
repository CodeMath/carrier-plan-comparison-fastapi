from fastapi import FastAPI, HTTPException, APIRouter
from enum import Enum
from router import combination, plan_list
from fastapi.middleware.cors import CORSMiddleware
from entry_point import create_table


def get_application():
    app = FastAPI()
    create_table()
    return app


app = get_application()

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
