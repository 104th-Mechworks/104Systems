import sqlite3

# from .bot import CPObot


# set up a database
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
