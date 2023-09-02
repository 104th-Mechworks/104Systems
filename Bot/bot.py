import discord
from discord.ext import commands


class CPObot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(
            activity=discord.Activity(
                type=discord.ActivityType.watching, name="104th Battalion"
            ),
            # allowed_mentions=discord.AllowedMentions.none(),
            auto_sync_commands=False,
            chunk_guilds_at_startup=False,
            # help_command=None,
            intents=discord.Intents.all(),
            owner_ids=[],
            command_prefix=".",
        )


class Cog(commands.Cog):
    def __init__(self, bot: CPObot) -> None:
        self.bot = bot
