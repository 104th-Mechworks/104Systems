import aiosqlite

async def connect(db_name: str):
    db = await aiosqlite.connect(db_name)
    cursor = await db.cursor()
    return db, cursor
class Members:
    async def create(self,
                     member_id: int,
                     rank: str,
                     name: str,
                     designation: str,
                     company: str = None,
                     platoon: str = None,
                     squad: str = None,
                     postioion: str = None,
                     ):
        db, cursor = await connect('Bot/data/database.db')
        await cursor.execute(f"SELECT ID FROM members WHERE ID = {member_id}")
        r = await cursor.fetchone()
        if r is not None:
            return {403: "member already exists"}
        await cursor.execute(f"INSERT INTO members (ID, Name, Designation, Section, Platform, Rank, Position, Company, Platoon, Squad) VALUES ({member_id}, {name}, {designation}, {section}, {platform}, {rank}, {position}, {company}, {platoon}, {squad})")