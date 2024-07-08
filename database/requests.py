from database.models import asyncsesion
from database.models import User, Category, Item
from sqlalchemy import select, update

import random


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


async def update_user_time(user_tg_id: int, new_save_value: str):
    async with asyncsesion() as session:
        stmt = (
            update(User)
            .where(User.tg_id == user_tg_id)
            .values(time=new_save_value)
        )
        await session.execute(stmt)
        await session.commit()


async def update_user_extra(user_tg_id: int, new_save_value: str):
    async with asyncsesion() as session:
        stmt = (
            update(User)
            .where(User.tg_id == user_tg_id)
            .values(extra=User.extra+new_save_value)
        )
        await session.execute(stmt)
        await session.commit()


async def update_card_masters(item_id: int):
    async with asyncsesion() as session:
        stmt = (
            update(Item)
            .where(Item.id == item_id)
            .values(masters=Item.masters+1)
        )
        await session.execute(stmt)
        await session.commit()

async def mozno(tg_id):
    async with asyncsesion() as session:
        result = await session.execute(select(User))
        user = result.scalars().all()
        for i in user:
            if i.tg_id == tg_id:
                return (i.time, i.extra)


async def card_finder(item, x, rar):
    c = []
    for i in item:
        if i.rarity == rar:
            c.append((i.id,i.name,i.description,i.rarity))
    b = random.choice(c) 
    i = x.save
    if i[b[0]-1] == '1':
        c = 1
    else:
        i = i[:b[0]-1] + '1' + i[b[0]:]
        c = 0
        await update_card_masters(b[0])
    return (i,b,c)



async def get_collectnumb(tg_id):
    async with asyncsesion() as session:
        result = await session.execute(select(User))
        user = result.scalars().all()
        for i in user:
            if i.tg_id == tg_id:
                return i.save


async def get_collection(tg_id):
    async with asyncsesion() as session:
        result = await session.execute(select(User))
        user = result.scalars().all()
        for i in user:
            if i.tg_id == tg_id:
                break
        
        save = i.save
        
        result = await session.execute(select(Item))
        item = result.scalars().all()
        c = 0
        a = []
        for i in item:
            a.append((f'{i.rarity} карта - {i.name}\n\n{i.description}',i.id))
        b = []
        for i in save:
            if int(i):
                b.append(a[c])
            c+=1

        return b
            

async def get_card(item_id):
    async with asyncsesion() as session:
        result = await session.execute(select(Item))
        items = result.scalars().all()

        for i in items:
            
            if i.id == item_id:
                return(i.id,f'{i.rarity} карта - {i.name}\n\n{i.description}')


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
            i = await card_finder(item, x, 'Редкая')

        elif r < 55:
            i = await card_finder(item, x, 'Суперская')
            
        else:
            i = await card_finder(item, x, 'Обычная')
            
        await update_user_save(x.id,i[0])
        return i[1:]



