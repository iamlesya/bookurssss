import requests
from bs4 import BeautifulSoup, PageElement
from book import Book
from tqdm import tqdm


def get_info_book(url: str):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")

    allInformation = soup.findAll('div', class_='book_name')
    index = str(allInformation).find('<h1>')
    allInformation = str(allInformation)[index + 4::]
    index = str(allInformation).find('<')
    allInformation = str(allInformation)[:index:]
    name = str(allInformation)


    allInformation = soup.findAll('div', class_='b_biblio_book_annotation')
    index = str(allInformation).find('<p>')
    allInformation = str(allInformation)[index + 3::]
    index = str(allInformation).find('</p>')
    allInformation = str(allInformation)[:index:]
    description = str(allInformation)

    allInformation = soup.findAll('div', class_='row year_public')
    index = str(allInformation).find('"row_content">')
    allInformation = str(allInformation)[index + 14::]
    index = str(allInformation).find('<')
    allInformation = str(allInformation)[:index:]
    date_release = str(allInformation)

    allInformation = soup.findAll('div', class_='row author')
    index = str(allInformation).find('"author">')
    allInformation = str(allInformation)[index + 9::]
    index = str(allInformation).find('<')
    allInformation = str(allInformation)[:index:]
    author = str(allInformation)

    allInformation = soup.findAll('div', class_='book_rating')
    index = str(allInformation).find('"ratingCount"')
    allInformation = str(allInformation)[index+31::]
    index = str(allInformation).find('"')
    allInformation = str(allInformation)[:index:]
    book_rating = str(allInformation)


    allInformation = soup.findAll('div', class_='row genre')
    index = str(allInformation).find('"genre">')
    allInformation= str(allInformation)[index+8::]\
        .replace('</a>', '') \
        .replace('Эротические рассказы и истории', 'Эротические рассказы') \
        .replace('Документальная литература', 'Документальное') \
        .replace('Здоровое и правильное питание', 'Здоровое питание') \
        .replace('Классика приключенческой литературы', 'Приключения') \
        .replace('Исторические приключения', 'Приключения') \
        .replace('Книги о путешествиях', 'Приключения') \
        .replace('Остросюжетные любовные романы', 'Остросюжетные романы') \
        .replace('Зарубежные любовные романы', 'Зарубежные романы') \
        .replace('Короткие любовные романы', 'Короткие романы') \
        .replace('Исторические любовные романы', 'Исторические романы') \
        .replace('Классические любовные романы', 'Классические романы') \
        .replace('Любовно-фантастические романы', 'Фантастические романы') \
        .replace('Современные любовные романы', 'Совр. романы') \
        .replace('Современная русская литература', 'Русское совр.') \
        .replace('Зарубежная старинная литература', 'Зарубежное стар.') \
        .replace('Современная зарубежная литература', 'Зарубежное сов.') \
        .replace('Стартапы и создание бизнеса', 'Про бизнес') \
        .replace('Личная эффективность', 'Личностный рост') \
        .replace('Психологическая консультация', 'Психология') \
        .replace('Психологические тренинги', 'Психология') \
        .replace('Состояния и явления психики', 'Психология')\
        .replace('Юмористическая фантастика', 'Юмористич. фантастика') \

    book_genres = ''
    index = str(allInformation).find('<')
    book_genres = book_genres + str(allInformation)[:index:]

    allInformation = str(allInformation)[index::].replace(']', '')
    while len(allInformation) != 0:
        index = str(allInformation).find('>')
        allInformation = str(allInformation)[index+1::]
        index = str(allInformation).find('<')
        book_genres = book_genres + str(allInformation)[:index:]
        allInformation = str(allInformation)[index::]

    allInformation = soup.findAll('div', class_='book_img')
    index = str(allInformation).find('/')
    allInformation = str(allInformation)[index::]
    index = str(allInformation).find('"')
    allInformation = str(allInformation)[:index:]
    photo = 'https://flibusta.su' + allInformation

    allInformation = soup.findAll('span', class_='link')[1]
    index = str(allInformation).find("/")
    allInformation = str(allInformation)[index::]
    index = str(allInformation).find("'")
    allInformation = str(allInformation)[:index:]
    ebup = 'https://flibusta.su' + allInformation

    return Book(name, date_release, book_rating, book_genres, description, author, photo, ebup)


def get_all_books_from_page(page: int):
    url = f'https://flibusta.su/hot/?page={page}/'
    get_g = requests.get(url)
    soup = BeautifulSoup(get_g.text, "html.parser")
    allInformation = soup.findAll('div', class_='book_name')
    index = str(allInformation).find('/')
    allInformation = str(allInformation)[index::]
    index = str(allInformation).find('"')
    book = 'https://flibusta.su' + str(allInformation)[:index:]
    allInformation = allInformation[index::]

    books = []
    books.append(book)

    allInformation = str(allInformation).replace('href="', 'https://flibusta.su')
    for i in range(1, 99):
        index = allInformation.find('https://flibusta.su')
        allInformation = allInformation[index::]
        index = allInformation.find('"')
        book = allInformation[:index:]
        books.append(book)
        allInformation = allInformation[index::]



    all_books_on_page = []
    for i in tqdm(range(len(books))):
        all_books_on_page.append(get_info_book(books[i]))

    return all_books_on_page


def get_all_info(count: int):
    all_books = []
    seen_titles = set()  # Множество для хранения уникальных названий книг
    for i in tqdm(range(1, count + 1)):
        books_on_page = get_all_books_from_page(i)  # Получаем все книги на текущей странице
        for book in books_on_page:
            if book.name not in seen_titles:  # Проверяем, не добавлена ли уже эта книга
                seen_titles.add(book.name)  # Добавляем название в множество
                all_books.append(book)  # Добавляем книгу в общий список

    return all_books
