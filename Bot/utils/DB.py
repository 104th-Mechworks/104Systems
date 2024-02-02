import aiosqlite


async def connect_to_db(
    name: str = "main.sqlite",
) -> tuple[aiosqlite.Connection, aiosqlite.Cursor]:
    db = await aiosqlite.connect(name)
    cursor = await db.cursor()
    return db, cursor


async def close_db(db: aiosqlite.Connection, cursor: aiosqlite.Cursor) -> None:
    await cursor.close()
    await db.close()
    return
