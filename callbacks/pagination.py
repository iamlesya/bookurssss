from contextlib import suppress

from aiogram import F
from aiogram import Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from callbacks.calldata import MyCallback, GenreCallback, FavoritesCallback
from constants.const import smiles, ADD_FAVORITES, DELETE_FAVORITES, DELETE_FAVORITES, ADD_FAVORITES
from database.request import get_book_from_id, get_book_ids_from_genre_name, is_favorites_in, add_favorites, \
    delete_from_favorites
from keyboards.builders import generate_favorites_keyboard
from keyboards.fabrics import Paginator, paginator

router = Router()


@router.callback_query(Paginator.filter(F.action.in_(['prev', 'next'])))
async def paginator_(call: CallbackQuery, callback_data: Paginator):
    page_num = int(callback_data.page)
    page = page_num - 1 if page_num > 0 else 0

    if callback_data.action == "next":
        page = page_num + 1 if page_num < (len(smiles) - 1) else page_num

    with suppress(TelegramBadRequest):
        await call.message.edit_text(
            f"{smiles[page][0]}, {smiles[page][1]}", reply_markup=paginator(page)
        )
    await call.answer()


@router.callback_query(GenreCallback.filter(F.type == "choose_genre"))
async def send_book_of_genre(call: CallbackQuery, callback_data: GenreCallback):
    genre_name = callback_data.genre_name

    book_ids = set(get_book_ids_from_genre_name(genre_name))

    buttons = []
    for book_id in book_ids:
        book = get_book_from_id(book_id)

        button = InlineKeyboardButton(text=book.name,
                                      callback_data=MyCallback(foo="send", bar=str(book_id)).pack())
        buttons.append([button])

    kb = InlineKeyboardMarkup(inline_keyboard=buttons)

    if len(buttons) > 0:
        text = f'Вот, что удалось найти по запросу "{genre_name}"'
    else:
        text = f'Ничего не найдено по запросу "{genre_name}"'

    await call.message.answer(text=text, reply_markup=kb)
    await call.answer()


@router.callback_query(MyCallback.filter(F.foo == "send"))
async def send_book(call: CallbackQuery, callback_data: MyCallback) -> None:
    book_id = int(callback_data.bar)
    book = get_book_from_id(book_id)

    if is_favorites_in(book_id, call.from_user.id):
        text, foo = DELETE_FAVORITES, 0
    else:
        text, foo = ADD_FAVORITES, 1

    kb_favorites = generate_favorites_keyboard(text, foo, book_id)

    book.description = book.description[:800:]

    await call.message.answer_photo(book.photo, str(book), reply_markup=kb_favorites)
    await call.answer()


@router.callback_query(FavoritesCallback.filter(F.type == "favorites"))
async def add_book_to_favorites(call: CallbackQuery, callback_data: FavoritesCallback) -> None:
    id = callback_data.id

    is_favorites_in(id, call.from_user.id)

    if callback_data.description:
        add_favorites(id, call.from_user.id)

        text = DELETE_FAVORITES
    else:
        delete_from_favorites(id, call.from_user.id)

        text = ADD_FAVORITES

    kb_favorites = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text=text,
                             callback_data=FavoritesCallback(
                                 type="favorites", description=bool(not callback_data.description), id=id).pack())
    ]])

    await call.message.edit_reply_markup(call.inline_message_id, kb_favorites)

    await call.answer()
