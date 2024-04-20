from aiogram import F, Router
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command, CommandStart

import app.keybords as kb
# import app.cardgame as cg
import database.requests as rq

import random


router = Router()

@router.message(CommandStart())
async def firstmessage(message: Message):
    await rq.setuser(message.from_user.id)
    await message.answer(f'Привет, {message.from_user.first_name}, ты попал в МИРЭА карточки мирэа карты мира', reply_markup=kb.main)


@router.message(F.text == 'Получить карточку')
async def newcardmessage(message: Message):
    x = await rq.gamerandom(message.from_user.id)
    if x[0]:
        await message.answer(x[1])
        await message.answer('Вам выпал дубликат!', reply_markup=kb.card)
    else:
        await message.answer(x[1])
        await message.answer('Вам выпала новая карточка!', reply_markup=kb.card)


@router.message(F.text == 'Коленки')
async def kleimessage(message: Message):
    await message.reply('Придурки')