from database.models import *
from parser import get_all_info, Book


def add_book_to_bd(book: Book) -> None:
    BookTable.create(name=book.name,
                     date_release=book.date_release,
                     book_rating=book.book_rating,
                     book_genres=book.book_genres,
                     description=book.description,
                     author=book.author,
                     photo=book.photo,
                     ebup=book.ebup)

def get_all_genres() -> list:
    book_genres = BookTable.select(BookTable.book_genres)

    genres_unique = set()
    for genres_book in book_genres:
        genres_book = str(genres_book.book_genres).strip()

        all_genre = genres_book.split(',')
        for genre in all_genre:
            genres_unique.add(genre.lower().strip())

    return sorted(list(genres_unique))


def get_book_from_id(book_id: int) -> Book:
    for book in BookTable.select().where(BookTable.id == book_id):
        return Book(book.name, book.date_release, book.book_rating, book.book_genres,
                    book.description, book.author, book.photo, book.ebup)


def add_genre_to_bd(genre: str) -> None:
    Genre.create(name=genre)


def add_favorites(book_id: int, user_id: int) -> None:
    Favorites.create(book_id=book_id, user_id=user_id)


def delete_from_favorites(book_id: int, user_id: int) -> None:
    Favorites.get(Favorites.book_id == book_id and Favorites.user_id == user_id).delete_instance()


def get_book_id_from_user_favorites(user_id) -> list:
    book_ids = []
    for book in Favorites.select().where(Favorites.user_id == user_id):
        book_ids.append(book.book_id)

    return book_ids


def add_all_genre() -> None:
    all_genre = get_all_genres()
    for genre in all_genre:
        add_genre_to_bd(genre)


def get_id_from_genre_name(name: str) -> int:
    name = name.strip()
    for genre in Genre.select(Genre.id, Genre.name):
        if str(genre.name).strip() == name:
            return genre.id


def get_all_book_ids() -> list:
    ids = []
    for book in BookTable.select(BookTable.id, BookTable.name):
        ids.append(book.id)

    return ids


def get_book_ids_from_genre_name(genre_name: str):
    genre_id = get_id_from_genre_name(genre_name)

    return [book.book_id for book in
            GenreSearcher.select(GenreSearcher.book_id).where(GenreSearcher.genre_id == genre_id)]


def is_favorites_in(book_id: int, user_id: int) -> bool:
    is_in = False
    for _ in Favorites.select().where((Favorites.book_id == book_id) & (Favorites.user_id == user_id)):
        is_in = True

    return is_in


def is_user_reg(user_id: int) -> bool:
    is_reg = False
    for _ in User.select().where(User.user_id_tg == user_id):
        is_reg = True

    return is_reg


def get_user_role(user_id: int) -> str:
    for user in User.select(User.role).where(User.user_id_tg == user_id):
        return user.role


def add_user(name: str, user_id_tg: int, role: str) -> None:
    User.create(name=name, user_id_tg=user_id_tg, role=role)


def has_favorites(user_id: int) -> bool:
    has = False
    for _ in Favorites.select().where(Favorites.user_id == user_id):
        has = True

    return has


def create_search_table() -> None:
    a = BookTable.select(BookTable.id, BookTable.book_genres)

    for book in a:
        book_id = book.id

        genres_name = [genre.lower().strip() for genre in str(book.book_genres).split(',')]


        for genre_name in genres_name:
            genre_id = get_id_from_genre_name(genre_name)
            GenreSearcher.create(genre_id=genre_id, book_id=book_id)

#
# def reload_base() -> None:
#     delete_all_tables()
#     create_all_tables()
#     books = get_all_info(20)
#     for bookk in books:
#         add_book_to_bd(bookk)
#
# reload_base()
# genres = get_all_genres()
# for genre in genres:
#     add_genre_to_bd(genre)
#
# for i in BookTable.select():
#     if i.book_genres == ' ':
#         new = str(i.book_genres)
#         new = new.replace(' ', 'No')
#         i.book_genres = new
#         i.save()
#
# for i in BookTable.select():
#     new = str(i.author)
#     if '[' in new:
#         new = new[2:len(new) - 2:]
#         new = new.replace("'", '')
#
#         i.author = new
#         i.save()
#
# GenreSearcher.drop_table()
# GenreSearcher.create_table()
# create_search_table()

