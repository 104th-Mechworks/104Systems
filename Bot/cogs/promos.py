import datetime
import re
import logging
import discord
from discord.ext import commands

from Bot.DatacoreBot import DatacoreBot
from Bot.utils.DB import connect_to_db
from Bot.utils.Ranks import (
    rank_options,
    AUTHORIZED_RANKS,
    MainServerRole_dict,
    ARMY_dict,
    SFC_dict,
    SF1_dict,
    SF2_dict,
    AUX_dict,
    get_new_rank_data,
    OFFICER_RANKS,
    COMMAND_STAFF,
    NCO_RANKS,
    get_abv,
)
from Bot.utils.regex import FULL
from Bot.utils.logger import logger as log


async def rank_autocomplete(ctx: discord.AutocompleteContext):
    branch = ctx.options["branch"]
    if branch == "Army":
        return ARMY_dict.keys()
    elif branch == "SFC":
        return SFC_dict.keys()
    elif branch == "ARC":
        return SF1_dict.keys()
    elif branch == "RC":
        return SF2_dict.keys()
    elif branch == "AUX":
        return AUX_dict.keys()
    elif branch == "Command":
        return AUTHORIZED_RANKS


class Promo(commands.Cog):
    def __init__(self, bot: DatacoreBot):
        self.bot = bot

    @discord.slash_command(guild_ids=[1198378556137410660])
    @discord.option("member", description="Member to promote", type=discord.Member)
    @discord.option(
        "branch",
        description="Branch to promote in",
        choices=["Army", "SFC", "ARC", "RC", "AUX"],
    )
    @discord.option(
        "rank", description="Rank to promote to", autocomplete=rank_autocomplete
    )
    async def promote(
        self,
        ctx: discord.ApplicationContext,
        member: discord.Member,
        branch: str,
        rank: str,
    ):
        if ctx.user.top_role.name not in AUTHORIZED_RANKS:
            await ctx.respond(
                "You are not authorized to use this command", ephemeral=True
            )
            return
        main: discord.Guild = await self.bot.fetch_guild(1198378556137410660)
        print(main)
        channel = await main.fetch_channel(1198378558423306244)
        # resilient = await self.bot.fetch_guild(1198379770967244840)
        # triumphant = await self.bot.fetch_guild(1198380200279425084)
        # get current rank and name from member by using re and FULL regex
        new_rank = get_new_rank_data(rank)
        current_rank = re.search(FULL, member.display_name).group(1)
        name = re.match(FULL, member.display_name).group(2)
        designation = re.match(FULL, member.display_name).group(3)

        # check for clearance
        if rank in OFFICER_RANKS:
            nco = await main._fetch_role(1198378556321964135)
            officer = await main._fetch_role(1198378556338737193)
            if nco in member.roles:
                await member.remove_roles(nco)
            await member.add_roles(officer)

        if rank in COMMAND_STAFF:
            officer = await main._fetch_role(1198378556338737193)
            command = await main._fetch_role(1198378556372295796)
            if officer in member.roles:
                await member.remove_roles(officer)
            await member.add_roles(command)

        if rank in NCO_RANKS:
            nco = await main._fetch_role(1198378556321964135)
            await member.add_roles(nco)

        # main server role editing
        await member.remove_roles(member.top_role)
        main_rank_role = await main._fetch_role(new_rank[1])
        await member.add_roles(main_rank_role)

        new_rank_abv = get_abv(new_rank[0])

        await member.edit(nick=f"{new_rank_abv} {name} {designation}")
        date = f"{datetime.date.today():%d-%m-%Y}"
        db, cursor = await connect_to_db()
        await cursor.execute(
            "INSERT INTO Promos (memberID, oldRank, newRank, date) VALUES (?, ?, ?, ?)",
            (member.id, current_rank, new_rank_abv, date),
        )
        await cursor.execute(
            "UPDATE Members SET Rank = ? WHERE ID = ?", (new_rank_abv, member.id)
        )
        await db.commit()
        await cursor.close()
        await db.close()
        log.success(f"{current_rank} {name} -> {new_rank_abv}")
        # await channel.send(f"{current_rank} {name} -> {new_rank_abv}")


def setup(bot: DatacoreBot):
    bot.add_cog(Promo(bot))
    log.info("Promo cog loaded")
