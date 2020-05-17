from sqlalchemy import delete
from databases import Database


async def rm_object(model, column, conn: Database, data):
    """Remove object by column data."""
    query = delete(model).where(column == data)
    return await conn.execute(query)
