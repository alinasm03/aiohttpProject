import os

import sqlalchemy as sa
from aiopg.sa import create_engine

metadata = sa.MetaData()
tbl = sa.Table('links', metadata,
               sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
               sa.Column('new_link', sa.String(255)),
               sa.Column('old_link', sa.String(255)),
               sa.Column('user', sa.String(255)),
               )


async def init_pg():
    engine = await create_engine(user='postgres',
                             database='postgres',
                             host=os.getenv('POSTGRES_HOST', '127.0.0.1'),
                             password='0324B0324l!',
                             port=5432)
    return engine


async def insert_data(old_link, new_link, user=None):
    engine = await init_pg()
    async with engine.acquire() as conn:
        await conn.execute(tbl.insert().values(old_link=old_link,
                                               new_link=new_link,
                                               user=user))


async def get_link(new_link):
    engine = await init_pg()
    async with engine.acquire() as conn:
        result = await conn.execute(tbl.select().where(tbl.c.new_link == new_link))
        result = await result.fetchone()
        return result[2]


async def get_user_links(user_id):
    engine = await init_pg()
    async with engine.acquire() as conn:
        results = await conn.execute(tbl.select().where(tbl.c.user == str(user_id)))
        results = await results.fetchall()
        links = [f'http://127.0.0.1:8001/{result[1]} -> {result[2]}' for result in results]
        return links
