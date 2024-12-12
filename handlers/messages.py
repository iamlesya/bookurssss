from aiogram import Router, F
from aiogram.enums import InputMediaType
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, FSInputFile
from aiogram.utils.media_group import MediaGroupBuilder

from backup import create_backup
from callbacks.calldata import MyCallback
from constants.const import *
from converters.csv_converter import *
from database.models import *
from database.request import get_book_from_id, get_all_book_ids, get_book_id_from_user_favorites, has_favorites
from keyboards.builders import genres_kb
from keyboards.reply import convert_menu, main_kb, search_settings
from str_equal import is_names_equal

router = Router()


@router.message(F.text == GENRES)
async def genres(message: Message):
    await message.answer("Доступные жанры:", reply_markup=genres_kb())


@router.message(F.text == "Параметры")
async def top(message: Message):
    await message.answer("Настройки поиска", reply_markup=search_settings)


@router.message(F.text == "Выгрузить данные")
async def top(message: Message):
    await message.answer("Выберите формат", reply_markup=convert_menu)


@router.message(F.text == "Назад")
async def top(message: Message):
    await message.answer("Главное меню", reply_markup=main_kb)


@router.message(F.text == "Создать backup")
async def top(message: Message):
    await message.answer("Backup создан")
    await create_backup()


@router.message(F.text == "CSV")
async def get_data_on_csv(message: Message):
    tables = [User, BookTable, Favorites, Genre, GenreSearcher]
    tables_name = ["user", "book", "favorites", "genres", "genre_searcher"]

    for i in range(len(tables)):
        write_to_csv(tables[i], f"convert/{tables_name[i]}")

    media = MediaGroupBuilder()

    for table_name in tables_name:
        media.add(type=InputMediaType.DOCUMENT, media=FSInputFile(f"convert/{table_name}.csv"))

    await message.answer_media_group(media=media.build())


@router.message(F.text == "Json")
async def get_data_on_json(message: Message):
    tables = [User, BookTable, Favorites, Genre, GenreSearcher]
    tables_name = ["user", "book", "favorites", "genres", "genre_searcher"]

    for i in range(len(tables)):
        write_to_json(tables[i], f"convert/{tables_name[i]}")

    media = MediaGroupBuilder()

    for table_name in tables_name:
        media.add(type=InputMediaType.DOCUMENT, media=FSInputFile(f"convert/{table_name}.json"))

    await message.answer_media_group(media=media.build())


@router.message(F.text == "Excel")
async def get_data_on_excel(message: Message):
    tables = [User, BookTable, Favorites, Genre, GenreSearcher]
    tables_name = ["user", "book", "favorites", "genres", "genre_searcher"]

    for i in range(len(tables)):
        write_to_excel(tables[i], f"convert/{tables_name[i]}")

    media = MediaGroupBuilder()

    for table_name in tables_name:
        media.add(type=InputMediaType.DOCUMENT, media=FSInputFile(f"convert/{table_name}.xlsx"))

    await message.answer_media_group(media=media.build())


@router.message(F.text == FAVORITES)
async def favorites(message: Message):
    if has_favorites(message.from_user.id):
        book_ids = get_book_id_from_user_favorites(message.from_user.id)
        buttons = []
        for book_id in book_ids:
            book = get_book_from_id(book_id)

            button = InlineKeyboardButton(text=book.name,
                                          callback_data=MyCallback(foo="send", bar=str(book_id)).pack())
            buttons.append([button])

        kb = InlineKeyboardMarkup(inline_keyboard=buttons)

        await message.answer(f"Избранное:, {message.from_user.first_name}", reply_markup=kb)
    else:
        await message.answer("Избранное пусто")


@router.message(F.text == SEARCH)
async def search(message: Message):
    await message.answer("Просто отправьте боту название книги")


@router.message()
async def find_book(message: Message):
    msg_text = message.text

    all_book_ids = get_all_book_ids()

    buttons = []
    for book_id in all_book_ids:
        book = get_book_from_id(book_id)

        if is_names_equal(book.name, msg_text):
            button = InlineKeyboardButton(text=book.name,
                                          callback_data=MyCallback(foo="send", bar=str(book_id)).pack())
            buttons.append([button])

    kb = InlineKeyboardMarkup(inline_keyboard=buttons)

    if len(buttons) > 0:
        text = f'Вот, что удалось найти по запросу "{msg_text}"'
    else:
        text = f'К сожалению, по вашему запросу ничего не найдено. 😔\n \n' \
               f'Попробуйте проверить правильность написания названия книги'

    await message.answer(text=text, reply_markup=kb)
