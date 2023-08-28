from discord.ext import commands

from .bot import CPObot
from .context import Context

__all__ = (
    "CPObot",
    "Cog",
    "Context",
)


class Cog(commands.Cog):
    """Base class for all cogs"""

    def __init__(self, bot: CPObot) -> None:
        self.bot = bot
