import discord
from discord.ext import commands
from Bot.DatacoreBot import DatacoreBot
from Bot.utils.DB import connect_to_db


class DataEvents(commands.Cog):
    def __init__(self, bot: DatacoreBot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_member_leave():
        pass

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        pass