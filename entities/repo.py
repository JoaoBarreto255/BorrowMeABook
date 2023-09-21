'''
Create local database.
'''
from sqlalchemy import create_engine, text

BOOK_TABLE = '''CREATE TABLE books
( id INTEGER PRIMARY KEY AUTOINCREMENT,
  title VARCHAR NOT NULL,
  isbn VARCHAR NOT NULL,
  author VARCHAR NOT NULL,
  capa VARCHAR,
  published_at DATE
);
'''
PEOPLE_TABLE = '''CREATE TABLE people
( id INTEGER PRIMARY KEY AUTOINCREMENT,
  name VARCHAR NOT NULL,
  age INT NOT NULL DEFAULT 5
);
'''
BOOK_OWNERS = '''CREATE TABLE book_owners
( id INTEGER PRIMARY KEY AUTOINCREMENT,
  book_id INTEGER,
  person_id INTEGER,
  CONSTRAINT fk_books
    FOREIGN KEY (book_id)
    REFERENCES books(id)
    ON DELETE CASCADE,
  CONSTRAINT fk_people
    FOREIGN KEY (person_id)
    REFERENCES people(id)
    ON DELETE CASCADE
);
'''
BORROWED_BOOKS = '''CREATE TABLE borrowed_books
( owner_id INTEGER,
  borrower_id INTEGER,
  CONSTRAINT fk_owners
    FOREIGN KEY (owner_id)
    REFERENCES book_owners(id)
    ON DELETE CASCADE,
  CONSTRAINT fk_people
    FOREIGN KEY (borrower_id)
    REFERENCES people(id)
    ON DELETE CASCADE
);
'''


def start():
    '''Create database tables'''
    engine = create_engine('sqlite://test.db')
    with engine.begin() as conn:
        conn.execute(text(BOOK_TABLE))
        conn.execute(text(PEOPLE_TABLE))
        conn.execute(text(BOOK_OWNERS))
        conn.execute(text(BORROWED_BOOKS))


if __name__ == '__main__':
    start()
