import aiosqlite
import discord
from discord.ext import commands
from Bot.DatacoreBot import DatacoreBot
from typing import Tuple



class AdminList(discord.ui.View):
    def __init__(self, bot: DatacoreBot):
        self.bot = bot
        super().__init__(timeout=None)

    @discord.ui.button(label="Admin List", style=discord.ButtonStyle.primary)
    async def admin_list(self, button: discord.ui.Button, interaction: discord.Interaction):
        async with aiosqlite.connect(self.bot.DB_PATH) as db:
            async with db.execute("SELECT Members.Rank, Members.Name, Members.Designation, Admin.Rank FROM Members, Admin") as cursor:
                admin_list: Tuple[Tuple[str]] = await cursor.fetchall()
        embed = discord.Embed(title="Admin List", description="Administration Department Roster", color=discord.Color.blurple())
        embed.add_field(name="**Head of Administration**", value="Admin 1")
        embed.add_field(name="Admin 2", value="Admin 2")
        embed.add_field(name="Admin 3", value="Admin 3")
        await interaction.response.send_message(embed=embed, ephemeral=True)
        self.stop()
