"""
Main file for my_api.
"""
from fastapi import FastAPI


app = FastAPI()


@app.get("/")
async def hello_world():
    return {"Hello":"world"}
