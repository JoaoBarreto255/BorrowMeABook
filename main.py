#!/usr/bin/env python

"""
Simple api is a api for serve list of books shared with colleague
"""
from fastapi import FastAPI
from controller import BOOK_ROUTER
from model import app_startup, app_close

app = FastAPI()

@app.on_event("startup")
async def startup():
    """Api prelude routine"""
    await app_startup()


@app.on_event("shutdown")
async def shutdown():
    """Api defer routine"""
    await app_close()


@app.get("/")
async def read_hello():
    """Send Hello Message"""
    return {"message": "Hello World!"}

app.include_router(BOOK_ROUTER)
