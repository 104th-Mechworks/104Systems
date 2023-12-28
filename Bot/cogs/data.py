import re

import discord
from discord.ext import commands
import aiosqlite
from discord.commands import option

from Bot.utils.DB import connect_to_db, close_db


async def company_autocomplete(ctx: discord.AutocompleteContext):
    branch = ctx.options["branch"]
    if branch == "Army":
        return [
            "30th Mechanised Ares Company",
            "44th Infantry Reaper Company",
            "82nd Armoured Havoc Company",
            "29th Infantry Valkyrie Company",
            "48th Infantry Rogue Company",
            "34th Mechanised Horizon Company",
            "22nd Vanguard Company",
            "60th Reconnaissance Company",
        ]
    elif branch == "Starfighter Corps":
        return [
            "1st Fighter Obsidian Owls Wing",
            "13th Fighter Eagle's Talons Wing",
            "42nd Midnight Ravens Squadron",
        ]


async def platoon_autocomplete(ctx: discord.AutocompleteContext):
    company = ctx.options["company"]


async def position_autocomplete(ctx: discord.AutocompleteContext):
    branch = ctx.options["branch"]
    if branch == "Army":
        return [
            "Army Company Commander",
            "Army Executive Officer",
            "Head of Console"
            "Company Commanding Officer",
            "Company Executive Officer",
            "Company Non-Commissioned Officer",
            "Platoon Commanding Officer",
            "Platoon Executive Officer",
            "Platoon Non-Commissioned Officer",
            "Squad Leader",
            "Squad Non-Commissioned Officer",
            "CT",
        ]
    elif branch == "Starfighter Corps":
        return ["not implemented"]

class Data(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    data = discord.SlashCommandGroup(name="data", description="Data commands")

    @data.command(name="add", description="Add data to the database")
    @option("branch", description="Branch the member belongs to", choices=["Army", "Starfighter Corps", "Naval Auxiliary", "Special Operations Force"])
    @option("company", description="Company the member belongs to", autocomplete=company_autocomplete, default=None)
    @option("platoon", description="Platoon the member belongs to", autocomplete=platoon_autocomplete, default=None)
    @option("position", description="Position the member holds", autocomplete=position_autocomplete, default="CT")
    async def add(self, ctx: discord.AutocompleteContext, member: discord.Member, branch: str, company: str, platoon: str, position: str):
        db, cursor = await connect_to_db("tmain.db")
        pattern = r"^[A-Z0-9]{2,4} [A-Za-z ]{0,12} [A-Za-z0-9/-]+$"
        await cursor.execute(f"SELECT ID FROM members WHERE ID = {member.id}")
        if await cursor.fetchone() is None:
            if re.match(pattern, member.display_name):
                CT = member.display_name.split(sep=" ")
                name: str = CT[1]
                designation: str = CT[2]
                rank: str = CT[0]
                await cursor.execute(f"INSERT INTO members VALUES ({member.id}, '{rank}', '{name}', '{designation}', '{branch}', '{company}', '{platoon}', '{position}', {None})")
                await db.commit()
                await close_db(db, cursor)
            await ctx.send(f"Added {member.name} to the database")
        else:
            await ctx.send(f"{member.name} already exists in the database")

def setup(bot):
    bot.add_cog(Data(bot))
