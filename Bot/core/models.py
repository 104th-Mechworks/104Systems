import aiosqlite
from core import CPObot


# set up a database
async def setup_db():
    async with aiosqlite.connect("Battalion.sqlite") as db:
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS Brig (
	            ID	INTEGER PRIMARY KEY NOT NULL UNIQUE,
	            Type	TEXT NOT NULL,
	            Name	TEXT NOT NULL,
	            Reason	TEXT,
	            Evidence	TEXT,
	            Date	TEXT NOT NULL,
	            ModID	INTEGER NOT NULL,
                roles  TEXT
            )
            """
        )
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS Members (
	            ID	INTEGER PRIMARY KEY NOT NULL UNIQUE,
	            Name	TEXT UNIQUE,
	            Designation	TEXT UNIQUE,
	            Rank	TEXT,
	            Position	TEXT,
	            Company	TEXT,
	            Platoon	TEXT,
	            Squad	TEXT
            )
            """
        )
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS Sshop (
                ID INTEGER PRIMARY KEY NOT NULL UNIQUE,
	            BHQ	TEXT,
	            Art_team TEXT,
	            ST TEXT
            )
            """
        )
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS KMC (
	            ID	INTEGER PRIMARY KEY NOT NULL UNIQUE,
	            Quals	TEXT,
	            adv_quals	TEXT,
	            Instructor	TEXT,
	            AdvInstructor	TEXT,
	            Cadre	TEXT
            )   
            """
        )
        await db.commit()
    for guild in CPObot.guilds:
        await db.execute(
            f"""
			CREATE TABLE IF NOT EXISTS {guild.id} (
	            ID	INTEGER PRIMARY KEY NOT NULL UNIQUE,
	            
			)
			"""
        )
    await db.close()
