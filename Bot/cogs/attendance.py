import aiosqlite
import discord
from discord.ext import commands

from bot import Cog, CPObot

bot = CPObot()


async def edit_roles(member: discord.Member, add: discord.Role, remove: discord.Role):
    await member.add_roles(add)
    await member.remove_roles(remove)


class Attendance(Cog):
    @commands.Cog.listener()
    async def on_ready(self) -> None:
        print("Attendance cog loaded")

    @commands.command()
    async def attendance(self, ctx: discord.ApplicationContext):
        """Attendance command"""
        db = aiosqlite.connect("Battalion.sqlite")
        async with db.execute(
            f"SELECT A0r, A1r, A2r, A3r, A4r, A5r, A6r, A7r, A8r, A9r, A10r FROM ServerConfig WHERE guild_id = {ctx.guild.id}"
        ) as cursor:
            rolesIDs = await cursor.fetchone()
            if roles is None:
                await ctx.send("Server not setup to accept auto attendance")
                return
        await db.close()
        roles = [ctx.guild.get_role(role) for role in rolesIDs]

        for member in ctx.message.mentions:
            if roles[0] in member.roles:
                await member.remove_roles(roles[0])
                await member.add_roles(roles[1])
            elif roles[1] in member.roles:
                await member.remove_roles(roles[1])
                await member.add_roles(roles[2])
            elif roles[2] in member.roles:
                await member.remove_roles(roles[2])
                await member.add_roles(roles[3])
            elif roles[3] in member.roles:
                await member.remove_roles(roles[3])
                await member.add_roles(roles[4])
            elif roles[4] in member.roles:
                await member.remove_roles(roles[4])
                await member.add_roles(roles[5])
            elif roles[5] in member.roles:
                await member.remove_roles(roles[5])
                await member.add_roles(roles[6])
            elif roles[6] in member.roles:
                await member.remove_roles(roles[6])
                await member.add_roles(roles[7])
            elif roles[7] in member.roles:
                await member.remove_roles(roles[7])
                await member.add_roles(roles[8])
            elif roles[8] in member.roles:
                await member.remove_roles(roles[8])
                await member.add_roles(roles[9])
            elif roles[9] in member.roles:
                await member.remove_roles(roles[9])
                await member.add_roles(roles[10])

            await db.execute(
                f"UPDATE {ctx.guild.id} SET attendance = attendance + 1 WHERE ID = {member.id}"
            )
            await db.commit()
        await db.close()
        await ctx.message.add_reaction("✅")

    att = discord.SlashCommandGroup("attendance", description="Attendance commands")

    @att.command(
        name="reset",
        description="Resets the attendance for the server",
        guild_ids=[1051580806788812841],
    )
    @discord.guild_only()
    async def attendance_reset(self, ctx: discord.ApplicationContext):
        """Resets the attendance for the server"""
        await ctx.defer()
        db = aiosqlite.connect("Battalion.sqlite")
        async with db.execute(f"UPDATE {ctx.guild.id} SET attendance = 0"):
            await db.commit()
        async with db.execute(
            f"SELECT HomeRole, A0r, A1r, A2r, A3r, A4r, A5r, A6r, A7r, A8r, A9r, A10r FROM ServerConfig WHERE guild_id = {ctx.guild.id}"
        ) as cursor:
            rolesIDs = await cursor.fetchone()
            if roles is None:
                await ctx.send("Server not setup to accept auto attendance")
                return
        await db.close()
        rolesIDs = [*rolesIDs]
        home = ctx.guild.get_role(rolesIDs[0])
        rolesIDs = rolesIDs.remove(rolesIDs[0])
        # remove the first item from the list
        roles = [ctx.guild.get_role(role) for role in rolesIDs]
        for member in ctx.guild.members:
            if home not in member.roles:
                pass
            # if roles[1] to roles[n-1] in member.roles remove the role and add roles[0]
            elif any(role in member.roles for role in roles[1:]):
                await edit_roles(member, roles[0], roles[1])


def setup(bot):
    bot.add_cog(Attendance(bot))
