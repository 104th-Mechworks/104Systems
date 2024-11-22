# import aiosqlite
import json
from typing import List

import aiosqlite
import discord
from discord import option
from discord.ext import commands

from Bot.DatacoreBot import DatacoreBot

# from Bot.utils.DB import connect_to_db
# from Bot.utils.kmcbitroles import RoleSwitcher

"""
Table:
ID | RoleInt |
"""


def role_select(ctx: discord.AutocompleteContext):
    path = ctx.options["path"]
    match path:
        case "Anti-Armour":
            return ["Anti-Armour", "Advanced Anti-Armour", "Anti-Armour Instructor", "Advanced Anti-Armour Instructor",
                "Anti-Armour Cadre", "Head Anti-Armour Cadre"]
        case "Marksman":
            return ["Marksman", "Advanced Marksman", "Marksman Instructor", "Advanced Marksman Instructor",
                "Marksman Cadre", "Head Marksman Cadre"]
        case "Rifleman":
            return ["Rifleman", "Advanced Rifleman", "Rifleman Instructor", "Advanced Rifleman Instructor",
                "Rifleman Cadre", "Head Rifleman Cadre"]
        case "ARC":
            return ["ARC Candidate", "Advanced Recon Commando", "ARC Instructor", "ARC Cadre", "Head ARC Cadre"]
        case "RC":
            return ["RC Candidate", "Republic Commando", "RC Instructor", "RC Cadre", "Head RC Cadre"]


async def fetch_or_get_role(guild, role_id):
    role = discord.utils.get(guild.roles, id=role_id)
    if role is None:
        role = await guild._fetch_role(role_id)
    return role


class KMC(commands.Cog):
    def __init__(self, bot: DatacoreBot):
        self.bot = bot

    kmc = discord.SlashCommandGroup("kmc")

    @kmc.command()
    async def purge(self, ctx: discord.ApplicationContext):
        c1 = ctx.guild.get_role()
        async for member in ctx.guild.fetch_members(limit=None):
            if member.bot:
                continue
            if member.roles == [c1, c2, c3]:
                k = check_kmc_kicks(member)
                if k == 3:
                    await member.ban(reason="KMC Purge")
                else:
                    pass

    @kmc.command()
    @option(name="path", description="Pathway", choices=["Anti-Armour", "Rifleman", "Marksman", "ARC", "RC"])
    @option(name="role", desciption="Role to add", autocomplete=role_select)
    async def _add(self, ctx: discord.ApplicationContext, path: str):
        pass

    @commands.command()
    async def scrape(self, ctx: commands.Context):
        roles = {}
        for role in ctx.guild.roles:
            roles[role.name] = role.id
        with open("roles.json", "w") as f:
            json.dump(roles, f, indent=4)

    @commands.command()
    async def collate(self, ctx: commands.Context):
        roles = {
            "Ace Qualification": await fetch_or_get_role(ctx.guild, 1198467310025973831),
            "ARF Qualification": await fetch_or_get_role(ctx.guild, 1198467310038548483),
            "Aerial Qualification": await fetch_or_get_role(ctx.guild, 1198467310025973829),
            "Marksman Qualification": await fetch_or_get_role(ctx.guild, 1198467310025973832),
            "Anti-Armor Qualification": await fetch_or_get_role(ctx.guild, 1198467310025973834),
            "Rifleman Qualification": await fetch_or_get_role(ctx.guild, 1198467310038548481),
            "AT-RT Qualification": await fetch_or_get_role(ctx.guild, 1198467310038548484),
            "Advanced Aerial": await fetch_or_get_role(ctx.guild, 1198467310025973830),
            "Advanced Marksman": await fetch_or_get_role(ctx.guild, 1198467310025973833),
            "Advanced Anti-Armor - TX-130": await fetch_or_get_role(ctx.guild, 1198467310038548480),
            "Advanced Rifleman": await fetch_or_get_role(ctx.guild, 1198467310038548482),
            "Ace Instructor": await fetch_or_get_role(ctx.guild, 1198467310038548486),
            "ARF Instructor": await fetch_or_get_role(ctx.guild, 1198467310038548487),
            "Rising Phoenix Instructor": await fetch_or_get_role(ctx.guild, 1198467310038548488),
            "Marksman Instructor": await fetch_or_get_role(ctx.guild, 1198467310038548489),
            "Anti-Armor Instructor": await fetch_or_get_role(ctx.guild, 1198467310046941225),
            "Rifleman Instructor": await fetch_or_get_role(ctx.guild, 1198467310046941226),
            "Advanced Instructor": await fetch_or_get_role(ctx.guild, 1198467310046941227),
            "Ace Cadre": await fetch_or_get_role(ctx.guild, 1198467310046941229),
            "Ace Head Cadre": await fetch_or_get_role(ctx.guild, 1198467310046941230),
            "ARF Cadre": await fetch_or_get_role(ctx.guild, 1261026001085792410),
            "ARF Head Cadre": await fetch_or_get_role(ctx.guild, 1198467310046941231),
            "Rising Phoenix Cadre": await fetch_or_get_role(ctx.guild, 1198467310046941232),
            "Rising Phoenix Head Cadre": await fetch_or_get_role(ctx.guild, 1261026004672053308),
            "Marksman Cadre": await fetch_or_get_role(ctx.guild, 1198467310046941233),
            "Marksman Head Cadre": await fetch_or_get_role(ctx.guild, 1261026260772196463),
            "Anti-Armor Cadre": await fetch_or_get_role(ctx.guild, 1198467310046941234),
            "Anti-Armor Head Cadre": await fetch_or_get_role(ctx.guild, 1198467310055333990),
            "Rifleman Cadre": await fetch_or_get_role(ctx.guild, 1198467310055333991),
            "Rifleman Head Cadre": await fetch_or_get_role(ctx.guild, 1261025770025783417),
            "Advanced Recon Commando": await fetch_or_get_role(ctx.guild, 1198467310067908616),
            "Commando": await fetch_or_get_role(ctx.guild, 1198467310067908617)
                 }
        async with aiosqlite.connect(self.bot.DB_PATH) as db:
            async with db.cursor() as cursor:
                for role in roles:
                    await cursor.execute(f"INSERT INTO kmc (ID, Quals, adv_quals, Instructor, AdvInstructor, Cadre) VALUES ('{role}', {roles[role].id})")
                await db.commit()


    @commands.slash_command()
    async def purge(self, ctx: discord.ApplicationContext):
        l3r = await fetch_or_get_role(ctx.guild, 1)
        l2r = await fetch_or_get_role(ctx.guild, 2)
        l1r = await fetch_or_get_role(ctx.guild, 3)
        l0r = await fetch_or_get_role(ctx.guild, 4)
        console_list = [
            await fetch_or_get_role(ctx.guild, 5),
            await fetch_or_get_role(ctx.guild, 6),
            await fetch_or_get_role(ctx.guild, 7),
            await fetch_or_get_role(ctx.guild, 8),
            await fetch_or_get_role(ctx.guild, 9),
        ]
        trial_group: List[discord.Role] = []
        def check_cp(member):
            if member.bot:
                return False
            if member.roles == [l3r, l2r, l1r, l0r]:
                return True
            return False


        async for member in ctx.guild.fetch_members(limit=None):



def setup(bot: DatacoreBot):
    bot.add_cog(KMC(bot))
