import aiosqlite
import discord
from discord.ext import commands

from bot import Cog, CPObot


class Server(Cog):
    @commands.Cog.listener()
    async def on_ready(self) -> None:
        print("Server cog loaded")

    @discord.slash_command(guild_ids=[1051580806788812841])
    async def setup(
        self,
        ctx: discord.ApplicationContext,
        hrole: discord.Role,
        a0: discord.Role,
        a1: discord.Role,
        a2: discord.Role,
        a3: discord.Role,
        a4: discord.Role,
        a5: discord.Role,
        a6: discord.Role,
        a7: discord.Role,
        a8: discord.Role,
        a9: discord.Role,
        a10: discord.Role,
        nffccat: discord.CategoryChannel,
        nffcr: discord.Role,
        loacat: discord.CategoryChannel,
        loar: discord.Role,
    ):
        """Setup command"""
        db = aiosqlite.connect("Battalion.sqlite")
        async with db.execute(
            f"SELECT ID FROM ServerConfig WHERE guild_id = {ctx.guild.id}"
        ) as cursor:
            if await cursor.fetchone is None:
                await cursor.execute(
                    f"INSERT INTO ServerConfig (guild_id, HomeRole, A1r, A2r, A3r, A4r, A5r, A6r, A7r, A8r, A9r, A10r, NFFCcat, NFFCr, LOAcat, LOAr) VALUES ({ctx.guild.id}, {hrole.id}, {a0.id}, {a1.id}, {a2.id}, {a3.id}, {a4.id}, {a5.id}, {a6.id}, {a7.id}, {a8.id}, {a9.id}, {a10.id}, {nffccat.id}, {nffcr.id}, {loacat.id}, {loar.id})"
                )

                db.execute(f"CREATE TABLE {ctx.guild.id} (ID int, attendance int)")
                await db.commit()
                await db.close()

                await ctx.send("Setup complete")


def setup(bot: CPObot):
    bot.add_cog(Server(bot))
