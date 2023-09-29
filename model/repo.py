"""
Create local database.
"""
import databases
from sqlalchemy import create_engine
from sqlalchemy import MetaData, Table, Column
from sqlalchemy import Integer, String, Date, ForeignKey
from .models import Book, OwnedBook, Person

DATABASE_URL = "sqlite:///test.db"

database = databases.Database(DATABASE_URL)

meta = MetaData()
BOOKS = Table(
    "books",
    meta,
    Column("id", Integer, primary_key=True),
    Column("title", String, nullable=False),
    Column("isbn", String),
    Column("cover", String),
    Column("published_at", Date),
)
PEOPLE = Table(
    "people",
    meta,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("age", Integer, primary_key=True),
)
BOOK_OWNERS = Table(
    "book_owners",
    meta,
    Column("id", Integer, primary_key=True),
    Column("book_id", ForeignKey("books.id", ondelete="cascade")),
    Column("person_id", ForeignKey("people.id", ondelete="cascade")),
)
BORROWED_BOOKS = Table(
    "borrowed_books",
    meta,
    Column("owner_id", ForeignKey("book_owners.id", ondelete="cascade")),
    Column("borrower_id", ForeignKey("people.id", ondelete="cascade")),
)

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
meta.create_all(engine)

async def app_startup():
    await database.connect()

async def app_close():
    await database.disconnect()

class BookRepo:
    def __init__(self):
        super().__init__()

    async def get_all_books(self) -> list:
        """fetch from database all books"""
        query = BOOKS.select()
        return await database.fetch_all(query)

    async def get_one_book(self, book_id: int):
        """
        get one book
        :param book_id: db book key
        """
        query = BOOKS.select().where(BOOKS.c.id == book_id)
        return await database.fetch_one(query)

    async def create_book(self, book: Book) -> dict:
        """Insert one book in db
        :param book: new Book from catalog.
        """
        query = BOOKS.insert().values(
            title=book.title,
            isbn=book.isbn,
            cover=book.cover,
            published_at=book.published_at,
        )
        last_row_id = await database.execute(query)

        return {
            **book.model_dump(),
            'id': last_row_id
        }

    async def update_book(self, book: Book) -> dict:
        """Update one book.
        :params kargs: dict where keys are name from fields to update.
        """
        assert book.id and book.id > 0, "No book available!"
        query = BOOKS.update().where(BOOKS.c.id == book.id).values(
            title = book.title, isbn = book.isbn,
            cover = book.cover, published_at = book.published_at 
            )
        await database.execute(query)
        return book.model_dump()

    async def delete_book(self, book_id: int) -> bool:
        """Delete book from library"""
        assert book_id and book_id > 0, "No book available!"
        query = BOOKS.delete().where(BOOKS.c.id == book_id)
        result = await database.execute(query)
        assert result, "Could not delete book"
