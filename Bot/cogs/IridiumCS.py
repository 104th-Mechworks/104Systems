import discord
from discord.ext import commands
from Bot.DatacoreBot import DatacoreBot
import aiosqlite
import re
from Bot.utils.regex import FULL
import logging


log = logging.getLogger("Datacore")
log.setLevel(logging.DEBUG)

async def fetch_or_get_role(guild, role_id):
    role = discord.utils.get(guild.roles, id=role_id)
    if role is None:
        role = await guild._fetch_role(role_id)
    return role


async def load_company_roles(guild):
    companies = {
        "Ares": await fetch_or_get_role(guild, 1198378556288405583),
        "Reaper": await fetch_or_get_role(guild, 1198378556288405582),
        "Havoc": await fetch_or_get_role(guild, 1198378556288405581),
        "Monarch": await fetch_or_get_role(guild, 1198378556288405580),
        "Valkyrie": await fetch_or_get_role(guild, 1198378556288405579),
        "Vanguard": await fetch_or_get_role(guild, 1198378556305178678),
        "Horizon": await fetch_or_get_role(guild, 1198378556288405576),
        "Rancor": await fetch_or_get_role(guild, 1198378556305178679),
    }
    return companies


async def load_platoon_roles(guild):
    platoons = {
        "Howler": await fetch_or_get_role(guild, 1206770085314830386),
        "Sentinel": await fetch_or_get_role(guild, 1206770088011763743),
        "Taurus": await fetch_or_get_role(guild, 1206770105187438633),
        "Cerberus": await fetch_or_get_role(guild, 1206770108916174928),
        "Ghost": await fetch_or_get_role(guild, 1206770125303193630),
        "Scrapper": await fetch_or_get_role(guild, 1206770142340448297),
        "Dagger": await fetch_or_get_role(guild, 1206770145830371359),
        "Fenrir": await fetch_or_get_role(guild, 1206770161684578335),
        "Titan": await fetch_or_get_role(guild, 1206770166596243496),
        "Ice": await fetch_or_get_role(guild, 1206770184875147264),
        "Ravager": await fetch_or_get_role(guild, 1206770193746100285),
        "Hound": await fetch_or_get_role(guild, 1206770202151223348),
        "Dawn": await fetch_or_get_role(guild, 1206770221558276106),
        "Solstice": await fetch_or_get_role(guild, 1206770232585363526),
        "Fang": await fetch_or_get_role(guild, 1206770237819854899),
        "Storm": await fetch_or_get_role(guild, 1206770245193441340),
        "Spectre": await fetch_or_get_role(guild, 1206770268580872262),
        "Corvus": await fetch_or_get_role(guild, 1112067702855718666451),
        "Iridium": await fetch_or_get_role(guild, 1206770292287086662),
        "Tempest": await fetch_or_get_role(guild, 1206770310310002708),
        "Hunter": await fetch_or_get_role(guild, 1206770328152313937),
        "Royalty": await fetch_or_get_role(guild, 1206770321974366299),
    }
    return platoons


def get_branch(Rank):
    if Rank[0] == "A":
        return "SOF"

    if Rank in ["NCDR", "LTCDR", "NLT", "PO1", "PO2", "PO3"]:
        return "AUX"

    if Rank in ["CT", "LCPL", "CPL", "SGT", "SGM", "WO", "2LT", "LT", "CPT", "MAJ", "CDR"]:
        return "Army"

    if Rank in ["PO", "FO", "FLT", "FCPT", "SL", "GCPT", "WCDR"]:
        return "SFC"

    if Rank in ["BCDR", "COM", "SCDR", "MCDR"]:
        return "Fleet Command"


class Iridium(commands.Cog):
    def __init__(self, bot: DatacoreBot):
        self.bot = bot

    @commands.command()
    async def iridium(self, ctx: commands.Context):
        ir = await ctx.guild._fetch_role(1198381345487986798)
        members = await ctx.guild.fetch_members(limit=None)

        ir_members = [member for member in members if ir in member.roles]
        async with aiosqlite.connect(self.bot.DB_PATH) as db:
            async with db.cursor() as cursor:
                for member in ir_members:
                    if not re.match(FULL, member.display_name):
                        continue
                    Rank, Name, Desig = re.match(FULL, member.display_name).groups()

                    await cursor.execute(f"INSERT INTO Members (ID, Rank, Name, Designation) VALUES ({member.id}, '{Rank}', '{Name}', '{Desig}')")
                    await db.commit()
                    await cursor.execute(f"INSERT INTO attendance (ID, AttendanceNum) VALUES ({member.id}, 0)")
                    await db.commit()

        await ctx.send("Iridium members added to database")

    @commands.command()
    async def csm(self, ctx: commands.Context):
        COMPANY = await load_company_roles(ctx.guild)
        PLATOON = await load_platoon_roles(ctx.guild)
        print(COMPANY)
        print(PLATOON)
        aux = await fetch_or_get_role(ctx.guild, 1198378556288405574)

        def get_company_role(member):
            matched_roles = [name for name, role in COMPANY.items() if role in member.roles]
            if len(matched_roles) == 1:
                return matched_roles[0]
            elif len(matched_roles) > 1:
                log.error(f"Member ID {member.id} has multiple company roles: {matched_roles}")
                return None
            return None

        def get_platoon_role(member):
            matched_roles = [name for name, role in PLATOON.items() if role in member.roles]
            if len(matched_roles) == 1:
                return matched_roles[0]
            elif len(matched_roles) > 1:
                log.error(f"Member ID {member.id} has multiple platoon roles: {matched_roles}")
                return None
            return None
        async with aiosqlite.connect(self.bot.DB_PATH) as db:
            async with db.cursor() as cursor:
                async for member in ctx.guild.fetch_members(limit=None):
                    if not re.match(FULL, member.display_name):
                        continue

                    Rank, Name, Desig = re.match(FULL, member.display_name).groups()
                    Company = get_company_role(member)
                    Platoon = get_platoon_role(member)
                    Branch = get_branch(Rank)
                    try:
                        await cursor.execute(f"INSERT INTO Members (ID, Rank, Name, Designation, Company, Platoon, Branch) VALUES ({member.id}, '{Rank}', '{Name}', '{Desig}', '{Company}', '{Platoon}', '{Branch}')")
                        await cursor.execute(f"INSERT INTO attendance (ID, AttendanceNum) VALUES ({member.id}, 0)")
                    except aiosqlite.IntegrityError:
                        log.info(f"Member {member.display_name} already exists in database")
                        continue

                    await db.commit()





            # Iterate over each member and get their company role



def setup(bot: DatacoreBot):
    bot.add_cog(Iridium(bot))

