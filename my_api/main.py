"""
Main file for my_api.
"""
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends
import my_api.crud as cr
from my_api.database import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

SessionDep = Annotated[Session, Depends(get_db)]



app = FastAPI()


@app.get("/")
async def hello_world():
    return {"Hello": "world"}


@app.get("/db_alive/")
async def check_db_alive(db: SessionDep):
    return cr.check_alive(db)
