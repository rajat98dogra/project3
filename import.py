import os, csv

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import psycopg2
# database engine object from SQLAlchemy that manages connections to the database
DB_URL = 'postgresql://{user}:{pw}@{url}/{db}'.format(user='postgres',pw='root',url='localhost',db='user')
engine = create_engine(DB_URL)

# create a 'scoped session' that ensures different users' interactions with the
# database are kept separate
db = scoped_session(sessionmaker(bind=engine))

file = open("books.csv")

reader = csv.reader(file)
next(reader,None)
for isbn, title, author, year in reader:

    db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
                {"isbn": isbn,
                 "title": title,
                 "author": author,
                 "year": year})

    print(f"Added book {title} to database.")

    db.commit()