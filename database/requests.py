from database.models import asyncsesion
from database.models import User, Category, Item
from sqlalchemy import select, update

import random

# o - обычные, r - редкие, s - суперы(ну как в бравле)

o = 2
r = 2
s = 1

async def setuser(tg_id):
    async with asyncsesion() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()
            result = await session.execute(select(User))
            user = result.scalars().all()

            result = await session.execute(select(Item))
            item = result.scalars().all()
            for i in user:
                if i.tg_id == tg_id:
                    await update_user_save(i.id,'0'*len(item))
                    break

async def fetch_users():
    async with asyncsesion() as session:
        result = await session.execute(select(Item))
        prepods = result.scalars().all()
        return prepods


async def update_user_save(user_id: int, new_save_value: str):
    async with asyncsesion() as session:
        stmt = (
            update(User)
            .where(User.id == user_id)
            .values(save=new_save_value)
        )
        await session.execute(stmt)
        await session.commit()


async def card_finder(item, x, rar):
    c = []
    for i in item:
        if i.rarity == rar:
            c.append((i.id,i.name,i.description))
    b = random.choice(c) 
    i = x.save
    if i[b[0]] == '1':
        c = 1
    else:
        i = i[:b[0]-1] + '1' + i[b[0]:]
        c = 0
    return (i,b,c)


async def gamerandom(tg_id):
    async with asyncsesion() as session:
        result = await session.execute(select(User))
        user = result.scalars().all()
        for i in user:
            if i.tg_id == tg_id:
                x = i
                break
        
        result = await session.execute(select(Item))
        item = result.scalars().all()
        r = random.randint(0,100)
        if r < 25:
            i = await card_finder(item, x, 'rare')
            await update_user_save(x.id,i[0])
            return (i[2],f'Редкая карта - {i[1][1]}\n\n{i[1][2]}')

        elif r < 35:
            i = await card_finder(item, x, 'super')
            await update_user_save(x.id,i[0])
            return (i[2],f'Суперская карта - {i[1][1]}\n\n{i[1][2]}')
            
        else:
            i = await card_finder(item, x, 'common')
            await update_user_save(x.id,i[0])
            return (i[2],f'Обычная карта - {i[1][1]}\n\n{i[1][2]}')



