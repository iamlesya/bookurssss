
class Book:
    def __init__(self, name, date_release,  book_rating, book_genres,description, author, photo, ebup):
        self.name = name
        self.description = description
        self.date_release = date_release
        self.author = author
        self.book_rating = book_rating
        self.book_genres = book_genres
        self.photo = photo
        self.ebup = ebup

    def __str__(self):
        return (f'<b>Название книги:</b> {self.name}\n\n'
                f'<b>Описание:</b> {self.description}\n\n'
                f'<b>Дата выхода:</b> {self.date_release}\n\n'
                f'<b>Автор:</b> {self.author}\n\n'
                f'<b>Рейтинг:</b> {self.book_rating}/5\n\n'
                f'<b>Жанры:</b> {self.book_genres}'
                f'<b>Скачать в формате .ebup:</b> {self.ebup}\n\n')

