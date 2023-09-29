'''
Create local database.
'''
from sqlalchemy import create_engine
from sqlalchemy import MetaData, Table, Column
from sqlalchemy import Integer, String, Date, ForeignKey
from entities import Book, OwnedBook, Person

meta = MetaData()
BOOKS = Table('books', meta,
              Column('id', Integer, primary_key=True),
              Column('title', String, nullable=False),
              Column('isbn', String),
              Column('cover', String),
              Column('published_at', Date))
PEOPLE = Table('people', meta,
               Column('id', Integer, primary_key=True),
               Column('name', String, nullable=False),
               Column('age', Integer, primary_key=True))
BOOK_OWNERS = Table('book_owners', meta,
                    Column('id', Integer, primary_key=True),
                    Column('book_id', ForeignKey(
                        'books.id', ondelete='cascade')),
                    Column('person_id', ForeignKey('people.id', ondelete='cascade')))
BORROWED_BOOKS = Table('borrowed_books', meta,
                       Column('owner_id', ForeignKey(
                           'book_owners.id', ondelete='cascade')),
                       Column('borrower_id', ForeignKey('people.id', ondelete='cascade')))


class Repo:
    _engine = None
    _conn = None

    def __init__(self):
        self.__conn = Repo._get_connection()

    @classmethod
    def _get_connection(cls):
        if cls._engine is None and cls._conn is None:
            cls._engine = create_engine('sqlite://test.db')
            cls._conn = cls._engine.connect()
        return cls._conn

    def get_all_books(self) -> list:
        """fetch from database all books"""
        stmt = BOOKS.select()
        results = self.__conn.execute(stmt)
        return [Book.create_from_result(r) for r in results]

    def get_book(self, book_id: int) -> Book:
        """
        get one book
        :param book_id: db book key
        """
        res = self.__conn.execute(BOOKS.select().where(BOOKS.c.id == book_id))
        return Book.create_from_result(res.fetchone())

    def create_book(self, book: Book) -> Book:
        """Insert one book in db
        :param book: Book
        """
        stmt = BOOKS.insert().values(title=book.title, isbn=book.isbn,
                                     cover=book.cover, published_at=book.published_at)
        res = self.__conn.execute(stmt)
        return self.get_book(res.inserted_primary_key)

    def update_book(self, **kargs) -> Book:
        """Update one book.
        :params kargs: dict where keys are name from fields to update.
        """
        assert kargs and (b_id := kargs.get('id')) and len(
            kargs) > 0, "No book to update!"
        book = {(k, v) for k, v in kargs.items() if v and k in [
            'title', 'isbn', 'cover', 'published_at']}
        stmt = BOOKS.update().where(BOOKS.c.id == b_id).values(book)
        res = self.__conn.execute(stmt)
        assert res.lastrowid, 'Sorry! could not update that book'
        return self.get_book(b_id)


def _start():
    '''Create database tables'''
    engine = create_engine('sqlite://test.db')
    meta.create_all(engine)


if __name__ == '__main__':
    _start()
