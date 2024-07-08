from aiogram.types import (KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Получить карточку'),
    KeyboardButton(text='Посмотреть коллекцию'),],
    [KeyboardButton(text='Цель нашего проекта'),
    KeyboardButton(text='Команда проекта'),]
], resize_keyboard=True, input_field_placeholder='Писять сюда...')

card = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Отправить друзьям', callback_data='newcard')],
    [InlineKeyboardButton(text='Посмотреть коллекцию', callback_data='collection')]
])

collectioncard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='⏪', callback_data='back_collection'),
    InlineKeyboardButton(text='счетч', callback_data='сч'),
    InlineKeyboardButton(text='⏩', callback_data='forw_collection')]
])


async def get_callback_btns(*, btns: dict[str, str], sizes: tuple[int] = (3,)):
    keyboard = InlineKeyboardBuilder()

    for text, data in btns.items():
        keyboard.add(InlineKeyboardButton(text=text, callback_data=data))

    return keyboard.adjust(*sizes).as_markup()



























import math


# Простой пагинатор
class Paginator:
    def __init__(self, array: list | tuple, page: int=1, per_page: int=1):
        self.array = array
        self.per_page = per_page
        self.page = page
        self.len = len(self.array)
        # math.ceil - округление в большую сторону до целого числа
        self.pages = math.ceil(self.len / self.per_page)

    def __get_slice(self):
        start = (self.page - 1) * self.per_page
        stop = start + self.per_page
        return self.array[start:stop]

    def get_page(self):
        page_items = self.__get_slice()
        return page_items

    def has_next(self):
        if self.page < self.pages:
            return self.page + 1
        return False

    def has_previous(self):
        if self.page > 1:
            return self.page - 1
        return False

    def get_next(self):
        if self.page < self.pages:
            self.page += 1
            return self.get_page()
        raise IndexError(f'Next page does not exist. Use has_next() to check before.')

    def get_previous(self):
        if self.page > 1:
            self.page -= 1
            return self.__get_slice()
        raise IndexError(f'Previous page does not exist. Use has_previous() to check before.')