"""
Module entities, has all model schema from api.
"""

from datetime import datetime
from pydantic import BaseModel


class Book(BaseModel):
    id: int | None = None
    title: str
    isbn: str | None = None
    cover: str | None = None
    published_at: datetime | None = None


class Person(BaseModel):
    """
    type Person: People registred in api.
    :field id: api acess key
    :field name: person names
    :field age: person age
    :field own_books: books which belongs to person
    :field borrowed_books: books borrowed from other people
    """

    id: int
    name: str
    age: int
    own_books: list
    borrowed_books: list


class OwnedBook(BaseModel):
    """
    type OwnedBook: Registries books which belongs to someone.
    :field owner: person who owners the book.
    :field book: Book belonged to someone.
    """

    owner: Person
    book: Book
