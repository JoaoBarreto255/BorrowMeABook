#!/usr/bin/env python

'''
Simple api is a api for serve list of books shared with colleague
'''

# from typing import Union
import asyncio
from fastapi import FastAPI
from hypercorn.config import Config
from hypercorn.asyncio import serve
from model import Repo, Book

app = FastAPI()
repo = Repo()

@app.get('/hello')
async def read_hello():
    """Send Hello Message"""
    return {"message": "Hello World!"}

@app.get('/books')
async def get_all_books():
    """fetch all books"""

    return [
        b for b in repo.get_all_books()
    ]

@app.post('/books')
async def create_book(book: Book) -> Book:
    created = repo.create_book(book)
    return created

if __name__ == '__main__':
    asyncio.run(serve(app, Config()))
