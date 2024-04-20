from aiogram.types import (KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton)


main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Получить карточку'),
    KeyboardButton(text='Кончить на коленку')]
], resize_keyboard=True, input_field_placeholder='Писять сюда...')

card = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Отправить друзьям', callback_data='newcard')],
    [InlineKeyboardButton(text='Посмотреть коллекцию', callback_data='collection')]
])