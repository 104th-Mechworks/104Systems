# handels all disciplinary commands
# restrictions: GUILDS = All

import aiosqlite
import discord
from core import Cog
from discord.ext import commands


async def role_search(guild: discord.Guild, role: str) -> discord.Role:
    """Searches for a role in a guild"""
    for r in guild.roles:
        if r.name == role:
            ret_role = await guild.get_role(r.id)
    if ret_role is None:
        await guild.fetch_roles()
        await role_search(guild, role)
    return ret_role


class Brig(Cog):
    @discord.slash_command()
    async def suspend(
        self, ctx: discord.ApplicationContext, member: discord.Member, reason: str
    ):
        roles: list = []
        for role in member.roles:
            await member.remove_roles(role)
            roles.append(role)

        async with aiosqlite.connect("Battalion.sqlite") as db:
            await db.execute(
                f"""
                INSERT INTO Brig (Type, Name, Reason, Date, ModID, roles)
                VALUES ("Suspend", "{member}", "{reason}", "{ctx.message.created_at}", "{ctx.author.id}"
                """
            )
            await db.commit()

        await ctx.respond(f"{member} has been suspended for {reason}")
