import sqlite3
from os import environ, getenv, listdir, path

from dotenv import load_dotenv

from bot import CPObot


def setup_db():
    db = sqlite3.connect("Battalion.sqlite")
    db.execute(
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
    db.execute(
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
    db.execute(
        """
            CREATE TABLE IF NOT EXISTS Sshop (
                ID INTEGER PRIMARY KEY NOT NULL UNIQUE,
	            BHQ	TEXT,
	            Art_team TEXT,
	            ST TEXT
            )
            """
    )
    db.execute(
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
    db.commit()
    db.close()


# get the relative path fo the folder called "cogs"
COGS_PATH = path.join(path.dirname(__file__), "cogs")
load_dotenv()


bot = CPObot()


def get_cogs() -> list[str]:
    "return each cog in the cogs folder"
    cogs = []
    for file in listdir(COGS_PATH):
        if file.endswith(".py"):
            cogs.append(f"cogs.{file[:-3]}")
    return cogs


@bot.event
async def on_ready() -> None:
    "send a success message to terminal when the bot is ready"
    print("Bot is ready")


for cog in get_cogs():
    bot.load_extension(cog)
setup_db()
bot.run(getenv("TOKEN"))
