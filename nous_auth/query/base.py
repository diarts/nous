from typing import List

from sqlalchemy import delete, select, insert
from databases import Database


async def rm_object(model, column, conn: Database, data):
    """Remove object by column data."""
    query = delete(model).where(column == data)
    return await conn.execute(query)


async def get_object_by_param(model, column, conn: Database, data):
    """Get object by column data."""
    query = select([model]).where(column == data)
    return await get_objects(conn, query)


async def get_object(conn: Database, query):
    """Get single object from DB."""
    return await conn.fetch_one(query=query)


async def get_objects(conn: Database, query):
    """Get many objects from DB."""
    return await conn.fetch_all(query=query)


async def make_object(model, conn: Database, data: dict or List[dict]):
    """Make object/objects in DB."""
    query = insert(model).values(*data)
    return await conn.execute(query=query)
