from sqlalchemy import delete, select
from databases import Database


async def rm_object(model, column, conn: Database, data):
    """Remove object by column data."""
    query = delete(model).where(column == data)
    return await conn.execute(query)


async def get_object(model, column, conn: Database, data):
    """Get object by clolumn data."""
    query = select([model]).where(column == data)
    return await conn.fetch_one(query=query)
