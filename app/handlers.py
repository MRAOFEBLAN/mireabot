from aiogram import F, Router, types
from aiogram.types import Message, FSInputFile, CallbackQuery, InputMediaPhoto
from aiogram.filters import Command, CommandStart
from aiogram.utils.media_group import MediaGroupBuilder

import datetime

import app.keybords as kb
# import app.cardgame as cg
import database.requests as rq



async def card_buider(xcaption, srcid, message):
    album_builder = MediaGroupBuilder(
        caption=xcaption
    )
    album_builder.add(
        type = "photo",
        media = FSInputFile(f"{srcid}.jpg"),
        # caption="Подпись к конкретному медиа"
    )
    await message.answer_media_group(
        # Не забудьте вызвать build()
        media = album_builder.build()
    )


router = Router()

@router.message(CommandStart())
async def firstmessage(message: Message):
    await rq.setuser(message.from_user.id)
    await message.answer(f'Привет, {message.from_user.first_name}, ты попал в МИРЭА карточки мирэа карты мира', reply_markup=kb.main)
    # await message.answer('7'*58)


@router.message(F.text == 'Получить карточку')
async def newcardmessage(message: Message):
    a = await rq.mozno(message.from_user.id)
    
    if a[1] > 0:
        x = await rq.gamerandom(message.from_user.id) 
        await rq.update_user_time(message.from_user.id,datetime.datetime.now())
        await rq.update_user_extra(message.from_user.id,-1)
        #print(x)
        media = FSInputFile(f'{x[0][0]}.jpg')

        if x[-1]:
            await message.answer_photo(media, caption=f'Вам выпал дубликат {x[0][3][:-2].lower()}ой карточки! 🙈\n\n{x[0][1]}\n\n{x[0][2]}', reply_markup=kb.main)
        else:
            await message.answer_photo(media, caption=f'Вам выпала новая {x[0][3].lower()} карточка! 😎\n\n{x[0][1]}\n\n{x[0][2]}', reply_markup=kb.main)
    
    elif ((datetime.datetime.now() - datetime.datetime.strptime(a[0], '%Y-%m-%d %H:%M:%S.%f')) > datetime.timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=3, hours=0, weeks=0)):
        x = await rq.gamerandom(message.from_user.id) 
        await rq.update_user_time(message.from_user.id,datetime.datetime.now())
        #print(x)
        media = FSInputFile(f'{x[0][0]}.jpg')
        
        if x[-1]:
            await message.answer_photo(media, caption=f'Вам выпал дубликат {x[0][3][:-2].lower()}ой карточки! 🙈\n\n{x[0][1]}\n\n{x[0][2]}', reply_markup=kb.main)
        else:
            await message.answer_photo(media, caption=f'Вам выпала новая {x[0][3].lower()} карточка! 😎\n\n{x[0][1]}\n\n{x[0][2]}', reply_markup=kb.main)

    else:
        a = str(datetime.timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=3, hours=0, weeks=0) - (datetime.datetime.now() - datetime.datetime.strptime(a[0], '%Y-%m-%d %H:%M:%S.%f'))).split('.')[0].split(':')
        await message.answer(f'''Cлишком часто крутишь!\nCледующий раз через {int(a[1])} - минут, {int(a[2])} - сексунд''', reply_markup=kb.main)
    
    

@router.message(F.text == 'Посмотреть коллекцию')
async def collectionmessage(message):
    xx = str(await rq.get_collectnumb(message.from_user.id))
    x = ''
    if int(xx) > 0:
        x = await rq.get_collection(message.from_user.id)
        c = ''
        for i in range(len(xx)):
            if xx[i] == '1':
                c+=str(i+1)
        media = FSInputFile(f'{x[0][1]}.jpg')
        if len(x) == 1:
            await message.answer_photo(media, caption=x[0][0], reply_markup = await kb.get_callback_btns(btns={
                f'1/{len(x)}' : 'none',
                '⏩(недоступно)' : f'nonk',
                }))
        else:
            await message.answer_photo(media, caption=x[0][0], reply_markup = await kb.get_callback_btns(btns={
                f'1/{len(x)}' : 'none',
                '⏩' : f'page_{2}_{message.from_user.id}_{c}',
                }))
    else:
        media = FSInputFile('0.jpg')
        await message.answer_photo(media, caption='Вы не получили еще ни одной карточки\n\nНажмите получить карточку👇'
                , reply_markup = kb.main
                )
    del x
    del xx
    
@router.callback_query(F.data.startswith('none'))
async def afsfa(callback):
    await callback.answer('')


@router.callback_query(F.data.startswith('nonk'))
async def afsfa(callback):
    await callback.answer('У ВАС 1 КАРТОЧКАААААААА! ЧТО ВЫ ТАМ ХОТИТЕ ПОСМОТРЕТЬ???!!')    
    
@router.callback_query(F.data.startswith('page_'))
async def couter(callback):
    s = int(callback.data.split('_')[1])
    usid = callback.data.split('_')[2]

    x = callback.data.split('_')[3]
    res = await rq.get_card(int(x[s-1]))

    media = FSInputFile(f'{res[0]}.jpg')
    
    #print(s, usid, x)
    await callback.message.edit_media(InputMediaPhoto(media = media))
    
    if s == 1:
        await callback.message.edit_caption(caption = f'{res[1]}', reply_markup = await kb.get_callback_btns(btns={
            # '⏪ first' : f'page_{s-1}_{usid}_{x}',
            f'{s}/{len(x)}' : 'none',
            '⏩' : f'page_{s+1}_{usid}_{x}',
            }))
    elif s == len(x):
        await callback.message.edit_caption(caption = f'{res[1]}', reply_markup = await kb.get_callback_btns(btns={
            '⏪' : f'page_{s-1}_{usid}_{x}',
            f'{s}/{len(x)}' : 'none',
            # '⏩' : f'page_{s+1}_{usid}_{x}',
            }))
    else:
        await callback.message.edit_caption(caption = f'{res[1]}', reply_markup = await kb.get_callback_btns(btns={
            '⏪' : f'page_{s-1}_{usid}_{x}',
            f'{s}/{len(x)}' : 'none',
            '⏩' : f'page_{s+1}_{usid}_{x}',
            }))

    



    
    
    
    

@router.message(F.text == 'Команда проекта')
async def aboutusmessage(message: Message):
    album_builder = MediaGroupBuilder(
        caption='@MRAOF, @LEWFAN, @Invincible_xXx, @danieltgrm'
    )
    album_builder.add(
        type = "photo",
        media = FSInputFile('b.jpg'),
        # caption="Подпись к конкретному медиа"
    )
    album_builder.add(
        type = "photo",
        media = FSInputFile('a.jpg'),
        # caption="Подпись к конкретному медиа"
    )
    await message.answer_media_group(
        # Не забудьте вызвать build()
        media = album_builder.build()
    )



@router.message(F.text == 'Коленки')
async def kleimessage(message: Message):
    await message.reply('Придурки')


@router.message(F.text == 'id')
async def da(message: Message):
    await message.reply(f'{message.from_user.id}')