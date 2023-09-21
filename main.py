#!/usr/bin/env python

'''
Simple api is a api for serve list of books shared with colleague
'''

# from typing import Union
import asyncio
from fastapi import FastAPI
from hypercorn.config import Config
from hypercorn.asyncio import serve

app = FastAPI()

@app.get('/hello')
async def read_hello():
    """Send Hello Message"""
    return {"message": "Hello World!"}

if __name__ == '__main__':
    asyncio.run(serve(app, Config()))
