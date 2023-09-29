#!/usr/bin/env python

'''
Simple api is a api for serve list of books shared with colleague
'''

from fastapi import FastAPI
from model import app_startup, app_close
from model import Book, BookRepo

app = FastAPI()
book_repo = BookRepo()

@app.on_event("startup")
async def startup():
    await app_startup()

@app.on_event("shutdown")
async def shutdown():
    await app_close()

@app.get('/hello')
async def read_hello():
    """Send Hello Message"""
    return {"message": "Hello World!"}

@app.get('/books')
async def get_all_books():
    """fetch all books"""
    return await book_repo.get_all_books()

@app.get('/books/{book_id}')
async def get_one_book(book_id: int) -> Book:
    """fetch one book"""
    return await book_repo.get_one_book(book_id)

@app.post('/books')
async def create_book(book: Book) -> Book:
    book.id = None
    return await book_repo.create_book(book)
