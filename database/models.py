from peewee import *

from book import Book

from parser import get_all_info

db = SqliteDatabase(r'C:\PycharmProjects\с\database\people1.db')

class BookTable(Model):
    name = TextField()
    date_release = TextField()
    book_rating = FloatField()
    book_genres = TextField()
    description = TextField()
    author = TextField()
    photo = TextField()
    ebup = TextField()

    class Meta:
        database = db


class Favorites(Model):
    user_id = IntegerField()
    book_id = IntegerField()

    class Meta:
        database = db


class User(Model):
    user_id = AutoField()
    name = TextField()
    user_id_tg = TextField()
    role = TextField()

    class Meta:
        database = db


class GenreSearcher(Model):
    genre_id = IntegerField()
    book_id = IntegerField()

    class Meta:
        database = db


class Genre(Model):
    name = TextField()

    class Meta:
        database = db


def create_all_tables():
    BookTable.create_table()
    Favorites.create_table()
    User.create_table()
    Genre.create_table()
    GenreSearcher.create_table()


def delete_all_tables():
    BookTable.drop_table()
    Favorites.drop_table()
    User.drop_table()
    Genre.drop_table()
    GenreSearcher.drop_table()


def add_book_to_bd(book: Book) -> None:
    BookTable.create(name=book.name,
                     date_release=book.date_release,
                     book_rating=book.book_rating,
                     book_genres=book.book_genres,
                     description=book.description,
                     author=book.author,
                     photo=book.photo,
                     ebup=book.ebup)


if __name__ == '__main__':
    books = get_all_info(20)
    for book in books:
        add_book_to_bd(book)
