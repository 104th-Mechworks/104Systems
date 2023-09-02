"""
5 * (lvl ^ 2) + (50 * lvl) + 100 - xp
lvl: current level
xp: how much xp alreaddy towards next level

"""
import sqlite3

import discord
from core import Cog, Context
from discord.ext import commands


class Levels(Cog):
    @discord.slash_command(name="level", description="Shows your current level")
    async def level(self, ctx: Context):
        # get xp from database: members
        # calculate level
        # send the custom image with level, xp and progress to next level
        await ctx.respond("This command is not yet implemented")
