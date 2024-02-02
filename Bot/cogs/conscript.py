import re
from sqlite3 import IntegrityError

import aiosqlite
import discord
from aiosqlite import Connection
from discord.ext import commands
from Bot.DatacoreBot import DatacoreBot
import logging

from Bot.utils.regex import FULL

log = logging.getLogger("Datacore")

bot = commands.Bot(intents=discord.Intents.all())
# resilient: discord.Guild = bot.get_guild(722211485505421442)
# triumphant: discord.Guild = bot.get_guild(584701143968514048)


async def connect():
    db = await aiosqlite.connect("main.sqlite")
    cursor = await db.cursor()
    return db, cursor


async def terminate(db: Connection, cursor) -> None:
    try:
        await cursor.close()
        await db.close()
    except Exception as e:
        raise e


# MSCroles = {
#     # main server company role ids: [branch server id, branch72222082877056631 server company role id]
#     723079290346012723: ["Ares", resilient, 6],  # ares
#     723081780285931602: ["Reaper", resilient, 722220831949979718],  # reaper
#     723080192268173412: ["Havoc", resilient, 722220830846877727],  # havoc
#     802593631008981012: ["Valkyrie", resilient, 803047054526906369],  # valkyrie
#     802593654203482140: ["Monarch", resilient, 803042505482305566],  # monarch
#     823291208826355722: ["Horizon", resilient, 722220834072297523],  # horizon.
#     723084217122291818: ["Vanguard", resilient, 803049514171629568],  # vanguard
#     750752796781052024: ["Rogue", resilient, 803323879883407372],  # rogue
#     723093092764352592: ["Rancor", resilient, 722220853571485697],  # rancor
#     723086687495913492: ["", triumphant],  # owls
#     723086680608735262: ["", triumphant],  # eagles
# }

CtoP = {
    # branch server company role id: {platoon role id: platoon server id}
    722220828770566316: {
        722224116891123723: 564954432928874506,  # howler
        722224129570504805: 565549847479058453,  # senti
        722224114177278013: 665361949483073562,  # taurus
    }
}


def check_company(ids: list[int] | int):
    companies = {
        723079290346012723: "Ares",
        723081780285931602: "Reaper",
        723080192268173412: "Havoc",
        802593631008981012: "Valkyrie",
        802593654203482140: "Monarch",
        823291208826355722: "Horizon",
        723084217122291818: "Vanguard",
        750752796781052024: "Rogue",
        723093092764352592: "Rancor",
        723086687495913492: "Owls",
        723086680608735262: "Eagles",
    }
    if isinstance(ids, list):
        for id1 in ids:
            if id1 in companies:
                return companies.get(id1)
            else:
                return None
    elif isinstance(ids, int):
        if ids in companies:
            return companies.get(ids)
        else:
            return None


def check_platoon(ids):
    platoons = {
        722224116891123723: "Howler",  # howler
        722224114177278013: "Taurus",  # taurus
        722224129570504805: "Sentinel",  # sentinel
        722224115720781824: "Cerberus",  # cerberus
        722224130581201016: "Ghost",  # ghost
        722224131910926376: "Scrapper",  # scrapper
        722224135987527701: "Dagger",  # dagger
        722224134897008731: "Fenrir",  # fenrir
        722224138193993809: "Titan",  # titan
        722224151993122892: "Hound",  # hound
        722224140680953968: "Ice",  # ice
        722224141532397648: "Dawn",  # dawn
        722224144959144037: "Ragnarok",  # ragnarok
        722226009247711306: "Solstice",  # solstice
        722224146058182686: "Phoenix",  # phenix
        740678291018481816: "Spectre",  # spectre
        817384107147264010: "Corvus",  # corvus
        817384110372683776: "Iridium",  # iridium
        722224153351946261: "Lightning",  # lightning
        722224146389532673: "Storm",  # storm
        725401028094197850: "Hunter",  # hunter
        722227653989498931: "Royalty",  # royalty
        722227656799682641: "Tempest",  # tempest
        793562406541459457: "Crystal",  # crystal squadron
        793562408051802164: "Cinder",  # cinder
        1074889828119883868: "Amethyst",  # amethyst
        703276079342944396: "Ospreys",
        703276080932454570: "Thunder Birds",
    }
    if isinstance(ids, list):
        for id1 in ids:
            if id1 in platoons:
                return platoons.get(id1)
            else:
                return None
    elif isinstance(ids, int):
        if ids in platoons:
            return platoons.get(ids)
        else:
            return None


def check_position(ids):
    positions = {
        722221890982248448: "FCOM",
        722220339089637446: "BCDR",
        722220398602747945: "MAJ",
        722216994102837330: "CCO",
        722233995332550696: "CXO",
        933874881525870643: "CNCO",
        722216949077114900: "PCO",
        722220835615539290: "PXO",
        722221196309037056: "PNCO",
        722221580435849306: "SL",
        722221591756537936: "SNCO",
    }
    if isinstance(ids, list):
        for id1 in ids:
            if id1 in positions:
                return positions.get(id1)
            else:
                return None
    elif isinstance(ids, int):
        if ids in positions:
            return positions.get(ids)
        else:
            return None


async def get_branchserver(self, company) -> discord.Guild:
    if company in [
        "Ares",
        "Reaper",
        "Havoc",
        "Valkyrie",
        "Monarch",
        "Horizon",
        "Vanguard",
        "Rogue",
        "Rancor",
    ]:
        branchserver: discord.Guild = self.bot.get_guild(722211485505421442)
        # if branchserver is None:
        #     branchserver: discord.Guild = await self.bot.fetch_guild(722211485505421442)
        return branchserver
    elif company in ["Owls", "Eagles"]:
        branchserver: discord.Guild = self.bot.get_guild(584701143968514048)
        return branchserver


def branch_type(company):
    if company in [
        "Ares",
        "Reaper",
        "Havoc",
        "Valkyrie",
        "Monarch",
        "Horizon",
        "Vanguard",
        "Rogue",
        "Rancor",
    ]:
        return "Army"
    elif company in ["Owls", "Eagles"]:
        return "SFC"


def get_branch(name):
    if "company" in name.lower():
        return "Army"
    elif "squadron" or "wing" in name.lower():
        return "SFC"
    else:
        return None


def map_company(id):
    companies = {
        723079290346012723: "Ares",
        723081780285931602: "Reaper",
        723080192268173412: "Havoc",
        802593631008981012: "Valkyrie",
        802593654203482140: "Monarch",
        823291208826355722: "Horizon",
        723084217122291818: "Vanguard",
        750752796781052024: "Rogue",
        723093092764352592: "Rancor",
        723086687495913492: "Owls",
        723086680608735262: "Eagles",
    }
    return companies.get(id)


class Conscript(commands.Cog):
    def __init__(self, bot_: DatacoreBot):
        self.bot = bot_

    @commands.Cog.listener()
    async def on_ready(self):
        log.info("Conscript ready")

    @commands.command()
    async def spop(self, ctx: commands.Context):
        print("Start")
        pattern = (
            r"^([A-Z]{2,4}) ([A-Z][a-z]+) ([A-Z]{1,2}-(?:[0-9]+|(?:\d-\d+\/\d+)))$"
        )
        count = 1
        db = await aiosqlite.connect("main.sqlite")
        cursor = await db.cursor()
        async for member in ctx.guild.fetch_members(limit=15000):
            print(member.id)
            if re.match(pattern, member.display_name):
                print(f"{member.display_name:-<40}{count}")
                count += 1
                CT = member.display_name.split(sep=" ")
                NAME: str = CT[1]
                DESG: str = CT[2]
                RANK: str = CT[0]
                platoon = None
                position = None
                branch = None
                company = None
                for role in member.roles:
                    company = check_company(role.id)
                    if company is not None:
                        branchserver = await get_branchserver(self, company)
                        branch = branch_type(company)
                        try:
                            member1 = await branchserver.fetch_member(member.id)
                        except Exception as e:
                            break
                        for role1 in member1.roles:
                            if platoon is None:
                                platoon = check_platoon(role1.id)
                            if position is None:
                                position = check_position(role1.id)
                        print(f"{member.display_name} | {company} | {platoon}")

                await cursor.execute(
                    f"INSERT INTO Members (ID, Rank, Name, Designation, Branch, Company, Platoon, Position, XP, LVL) VALUES (?,?,?,?,?,?,?,?,?,?)",
                    (
                        member.id,
                        RANK,
                        NAME,
                        DESG,
                        branch,
                        company,
                        platoon,
                        position,
                        0,
                        0,
                    ),
                )
                await db.commit()
        await cursor.close()
        await db.close()
        print("done :)")

    @commands.is_owner()
    @discord.slash_command(name="conscript", description="adds members to the database")
    async def rolebasedconscript(self, ctx: discord.ApplicationContext):
        await ctx.defer()
        counter = 0
        db, cursor = await connect()
        # pattern = r"^([A-Z0-9]{2,4}) ([A-Z][a-z]+) ([A-Z]{1,2}-(?:[0-9]+|(?:\d-\d+\/\d+)))$"
        async for member in ctx.guild.fetch_members(limit=12000):
            print(counter, member.display_name)
            if re.match(FULL, member.display_name):
                name_info = member.display_name.split(" ")
                RANK = name_info[0]
                NAME = name_info[1]
                DESG = name_info[2]
                try:
                    await cursor.execute(
                        f"INSERT INTO Members (ID, Rank, Name, Designation) VALUES ({member.id}, '{RANK}', '{NAME}', '{DESG}')"
                    )
                    counter += 1
                except IntegrityError:
                    pass
        await db.commit()
        await terminate(db, cursor)
        await ctx.respond(f"added {counter}", ephemeral=True)


def setup(bot: commands.Bot):
    bot.add_cog(Conscript(bot))
