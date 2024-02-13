"""
Main file for my_api.
"""
from typing import Annotated
from contextlib import asynccontextmanager
import os
from sqlalchemy.orm import Session
from meilisearch import Client
from meilisearch.errors import MeilisearchApiError
from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import PositiveInt
import my_api.crud as cr
from my_api.database import SessionLocal, Base, engine
from my_api.schemas import CreatePost, RetrievePost


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

SessionDep = Annotated[Session, Depends(get_db)]


def get_search_client():
    client = Client(url=os.environ.get("SEARCH_INDEX_URL"), 
                    api_key=os.environ.get("SEARCH_INDEX_KEY")
                )
    try:
        client.health()
        yield client
    except MeilisearchApiError as e:
        print("Check something.")

SearchDep = Annotated[Client, Depends(get_search_client)]


# tables created with alembic at start
@asynccontextmanager
async def lifespan(frage: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def hello_world():
    return {"Hello": "world"}


@app.get("/db_alive/")
async def check_db_alive(db: SessionDep):
    return cr.check_alive(db)


@app.post("/post/", response_model = RetrievePost)
async def create_post(db: SessionDep, p_info:CreatePost):
    post = cr.create_post(db, p_info)
    return post

@app.get("/post/{p_id}", response_model = RetrievePost)
async def get_post(db: SessionDep, p_id: PositiveInt):
    post = cr.get_post_by_id(db, p_id)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {p_id} not found.")
    return post

@app.delete("/post/{p_id}", response_model = RetrievePost)
async def ghost_delete_post(db: SessionDep, p_id: PositiveInt):
    post = cr.get_post_by_id(db, p_id)
    if post is None or post.is_deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {p_id} not found.")
    post = cr.ghost_delete_post(db, p_id)
    return post

@app.delete("/secret/post/{p_id}", response_model = RetrievePost)
async def actually_delete_post(db: SessionDep, p_id: PositiveInt):
    post = cr.get_post_by_id(db, p_id)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {p_id} not found.")
    post = cr.delete_post(db, p_id)
    return post


@app.get("/search_health/")
async def check_search_connection(m_client: SearchDep):
    return m_client.health()
