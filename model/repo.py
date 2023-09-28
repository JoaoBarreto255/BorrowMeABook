'''
Create local database.
'''
from sqlalchemy import create_engine
from sqlalchemy import MetaData, Table, Column
from sqlalchemy import Integer, String, Date, ForeignKey

meta = MetaData()
BOOKS = Table('books', meta, 
  Column('id', Integer, primary_key=True),
  Column('title', String, nullable=False),
  Column('isbn', String),
  Column('capa', String),
  Column('published_at', Date))
PEOPLE = Table('people', meta,
  Column('id', Integer, primary_key=True),
  Column('name', String, nullable=False),
  Column('age', Integer, primary_key=True))
BOOK_OWNERS = Table('book_owners', meta,
  Column('id', Integer, primary_key=True),
  Column('book_id', ForeignKey('books.id', ondelete='cascade')),
  Column('person_id', ForeignKey('people.id', ondelete='cascade')))
BORROWED_BOOKS = Table('borrowed_books', meta,
  Column('owner_id', ForeignKey('book_owners.id', ondelete='cascade')),
  Column('borrower_id', ForeignKey('people.id', ondelete='cascade')))



def start():
    '''Create database tables'''
    engine = create_engine('sqlite://test.db')
    meta.create_all(engine)


if __name__ == '__main__':
    start()
