
"""
Owners all controllers from books
"""
from fastapi import status
from fastapi.routing import APIRouter
from model import Book, BookRepo

BOOK_ROUTER = APIRouter(prefix="/books")
BOOK_REPO = BookRepo()

@BOOK_ROUTER.get("/")
async def get_all_books():
    """fetch all books"""
    return await BOOK_REPO.get_all_books()


@BOOK_ROUTER.get("/{book_id}")
async def get_one_book(book_id: int) -> Book:
    """fetch one book"""
    return await BOOK_REPO.get_one_book(book_id)


@BOOK_ROUTER.post("/")
async def create_book(book: Book) -> Book:
    """Create one book"""
    book.id = None
    return await BOOK_REPO.create_book(book)


@BOOK_ROUTER.put("/{book_id}")
async def update_book(book_id: int, book: Book) -> Book:
    """Update one book"""
    book.id = book_id
    return await BOOK_REPO.update_book(book)


@BOOK_ROUTER.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int):
    """Remove the book from list of books to borrow"""
    await BOOK_REPO.delete_book(book_id)
