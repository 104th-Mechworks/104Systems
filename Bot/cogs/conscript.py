from Bot.DatacoreBot import DatacoreBot
import discord
from discord.ext import commands
from Bot.utils.DB import connect_to_db
import re

ARMY_COMPANIES = {
    "Ares": 1198378556288405583,
    "Reaper": 1198378556288405582,
    "Havoc": 1198378556288405581,
    "Monarch": 1198378556288405580,
    "Valkyrie": 1198378556288405579,
    "Vanguard": 1198378556305178678,
    "Horizon": 1198378556288405576,
    "Rancor": 1198378556305178679,
}
SFC_WINGS = {
    "Owls": 1198378556305178684,
    "Eagles": 1198378556305178682,
    "Ravens": 1198378556305178681,
}

PLATFORM = {
    "Xbox": ["Ares", "Havoc", "Reaper", "Owls"],
    "PC": ["Vanguard", "Horizon", "Ravens"],
    "PS": ["Monarch", "Valkyrie", "Eagles"],
}


async def name_check(name: str) -> tuple[str, str, str]:
    if re.match(
            pattern=r"^([A-Z0-9]{2,4}) ([A-Z][A-Za-z]+) ([A-Z]{1,3}-(?:[0-9]+|(?:\d+-\d+)|(?:\d+-\d+\/\d+)|(?:\d+-\d{4})))$",
            string=name):
        dname = name.split(" ")
        return dname[0], dname[1], dname[2]

async def branch_check(roles: list):
    branch = None
    if any(role in ARMY_COMPANIES.values() for role in roles):
        branch = "Army"
    elif any(role in SFC_WINGS.values() for role in roles):
        branch = "SFC"

    # 2nd checks
    if 1198378556288405574 in roles:
        branch = "Aux"
    if 1198378556305178680 in roles:
        branch = "SOF"

    return branch


async def get_company(roles, branch):
    if branch == "Army":
        for role in roles:
            for key, value in ARMY_COMPANIES.items():
                if role == value:
                    return key
    elif branch == "SFC":
        for role in roles:
            for key, value in SFC_WINGS.items():
                if role == value:
                    return key
    elif branch == "Aux":
        return "Aux"
    elif branch == "SOF":
        return "SOF"
    else:
        return None


async def get_platform(company):
    if company in PLATFORM["Xbox"]:
        return "Xbox"
    elif company in PLATFORM["PC"]:
        return "PC"
    elif company in PLATFORM["PS"]:
        return "PS"
    else:
        return None


class Conscript(commands.Cog):
    def __init__(self, bot: DatacoreBot):
        self.bot = bot

    @commands.command()
    async def membadd(self, ctx: commands.Context):
        db, cursor = await connect_to_db()
        async for member in ctx.guild.fetch_members(limit=None):
            if (not re.match(
            pattern=r"^([A-Z0-9]{2,4}) ([A-Z][A-Za-z]+) ([A-Z]{1,3}-(?:[0-9]+|(?:\d+-\d+)|(?:\d+-\d+\/\d+)|(?:\d+-\d{4})))$",
            string=member.display_name)):
                continue
            roles=[]
            for role in member.roles:
                roles.append(role.id)
            rank, name, desg = await name_check(member.display_name)
            branch = await branch_check(roles)
            company = await get_company(roles, branch)
            platform = await get_platform(company)
            await cursor.execute(f"SELECT ID FROM Members WHERE ID = {member.id}")
            r = await cursor.fetchone()
            if r is None:
                await cursor.execute(f"INSERT INTO Members (ID, Rank, Name, Designation, Branch, Company, Platform) VALUES ({member.id}, '{rank}', '{name}', '{desg}', '{branch}', '{company}', '{platform}')")
                await cursor.execute(f"INSERT INTO attendance (ID, AttendanceNum) VALUES ({member.id}, 0)")
            else:
                await cursor.execute(f"UPDATE Members SET Rank = '{rank}', Name = '{name}', Designation = '{desg}', Branch = '{branch}', Company = '{company}', Platform = '{platform}' WHERE ID = {member.id}")
            print(member.display_name)
            await db.commit()
        await cursor.close()
        await db.close()
        print("done")



def setup(bot: DatacoreBot):
    bot.add_cog(Conscript(bot))