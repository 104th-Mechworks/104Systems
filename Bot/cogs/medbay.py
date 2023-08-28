# cog to handeling LOAs and NFFCs across the milsim
# restrictions: GUILDS = [Main_server, Platoon_servers, Vangard_company]

import discord
from core import Cog, Context
from discord.ext.commands import command


class Medbay(Cog):
    medbay = discord.SlashCommandGroup(
        name="medbay", description="Commands for the medbay"
    )

    @Cog.listener()
    async def on_ready(self):
        """Add persistent views"""

    pass
