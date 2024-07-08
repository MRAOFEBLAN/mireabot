from sqlalchemy import BigInteger, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3')

asyncsesion = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    save: Mapped[str] = mapped_column()
    time: Mapped[str] = mapped_column()
    extra: Mapped[int] = mapped_column()

class Category(Base):
    __tablename__ = 'kafedras'

    id: Mapped[int] = mapped_column(primary_key=True)
    kafedra: Mapped[str] = mapped_column()
    
class Item(Base):
    __tablename__ = 'prepod'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    rarity: Mapped[str] = mapped_column()
    kafedra: Mapped[str] = mapped_column(ForeignKey('kafedras.id'))
    masters: Mapped[int] = mapped_column()

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


