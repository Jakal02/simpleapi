"""
Main file for my_api.
"""
from typing import Annotated
from contextlib import asynccontextmanager
import os
import asyncio
from meilisearch_python_sdk import AsyncClient
from meilisearch_python_sdk.errors import MeilisearchApiError
from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import PositiveInt
import my_api.crud as cr
from my_api.database import Base, engine, SEARCH_INDEX_NAME, SessionDep
from my_api.schemas import CreatePost, RetrievePost
from my_api.search_sync import BackgroundSearchSyncer


async def get_search_client():
    client = AsyncClient(
        url=os.environ.get("SEARCH_INDEX_URL"),
        api_key=os.environ.get("SEARCH_INDEX_KEY"),
    )
    try:
        await client.health()
        yield client
    except MeilisearchApiError:
        print("Check something.")


SearchDep = Annotated[AsyncClient, Depends(get_search_client)]


runner = BackgroundSearchSyncer()


# tables created with alembic at start
@asynccontextmanager
async def lifespan(frage: FastAPI):
    Base.metadata.create_all(bind=engine)
    syncer = asyncio.create_task(runner.run_main())
    yield
    print(syncer.cancel())


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def hello_world():
    return {"Hello": "world"}


@app.get("/db_alive/")
async def check_db_alive(db: SessionDep):
    return cr.check_alive(db)


@app.post("/post/", response_model=RetrievePost)
async def create_post(db: SessionDep, p_info: CreatePost):
    post = cr.create_post(db, p_info)
    return post


@app.get("/post/{p_id}", response_model=RetrievePost)
async def get_post(db: SessionDep, p_id: PositiveInt):
    post = cr.get_post_by_id(db, p_id)
    if post is None or post.is_deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {p_id} not found."
        )
    return post


@app.delete("/post/{p_id}", response_model=RetrievePost)
async def ghost_delete_post(db: SessionDep, p_id: PositiveInt):
    post = cr.get_post_by_id(db, p_id)
    if post is None or post.is_deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {p_id} not found."
        )
    post = cr.ghost_delete_post(db, p_id)
    return post


@app.delete("/secret/post/{p_id}", response_model=RetrievePost)
async def actually_delete_post(db: SessionDep, client: SearchDep, p_id: PositiveInt):
    post = cr.get_post_by_id(db, p_id)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {p_id} not found."
        )
    await client.index(SEARCH_INDEX_NAME).delete_document(str(p_id))
    post = cr.delete_post(db, p_id)
    return post


@app.get("/search_health/")
async def check_search_connection(client: SearchDep):
    return await client.health()


@app.post("/search_index/")
async def create_search_index(client: SearchDep):
    return await client.create_index(uid=SEARCH_INDEX_NAME)


@app.delete("/search_index/")
async def delete_search_index(client: SearchDep):
    return await client.index(uid=SEARCH_INDEX_NAME).delete()


@app.get("/search_index/")
async def get_search_index(client: SearchDep):
    try:
        return await client.get_index(uid=SEARCH_INDEX_NAME)
    except MeilisearchApiError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)


@app.delete("/search_index/documents/all/")
async def delete_all_documents_in_search_index(client: SearchDep):
    try:
        return await client.index(uid=SEARCH_INDEX_NAME).delete_all_documents()
    except MeilisearchApiError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)


@app.get("/value/")
async def read_value():
    return {"value": runner.value, "updated": runner.updated_at}


@app.get("/search_index/{doc_id}")
async def get_document(doc_id: PositiveInt, client: SearchDep):
    try:
        return await client.index(SEARCH_INDEX_NAME).get_document(str(doc_id))
    except MeilisearchApiError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
