import json

import aiosqlite
import discord
from discord.ext import commands
from Bot.DatacoreBot import DatacoreBot
from Bot.utils.logger import logger as log

class ResetJSONManager:
    def __init__(self):
        self.json_obj = {}

    def add(self, key, value):
        if key in self.json_obj:
            # If key already exists, append the value to the existing list
            self.json_obj[key].append(value)
        else:
            # If key doesn't exist, create a new list with the value
            self.json_obj[key] = [value]

    def get_obj(self, key=None):
        if key is None:
            # If no key is specified, return the entire dictionary
            return self.json_obj
        return self.json_obj[key]

    def sort(self):
        # Sort the dictionary by key
        self.json_obj = dict(sorted(self.json_obj.items()))
        return self


def reset_embed_generator(json_obj) -> discord.Embed:
    # Create a new embed
    embed = discord.Embed(
        title="Attendance Reset",
        description="Attendance has been reset for the following members:",
        color=discord.Color.green()
    )

    # Iterate through the dictionary and add each key/value pair to the embed
    for key, value in json_obj.items():
        embed.add_field(name=key, value=", ".join(value), inline=False)

    return embed


async def connect_to_db():
    db = await aiosqlite.connect("main.sqlite")
    cursor = await db.cursor()
    return db, cursor


class Attendance(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="attendance")
    async def attendance(self, ctx: commands.Context):
        if len(ctx.message.mentions) == 0:
            msg = await ctx.reply("Must have at least 1 member mentioned")
            await msg.delete(delay=5)
            return
        else:
            db, cursor = await connect_to_db()
            await ctx.message.add_reaction("🟠")
            for member in ctx.message.mentions:
                try:
                    await cursor.execute(f"UPDATE attendance SET attendanceNum = attendanceNum + 1 WHERE ID = {member.id}")
                    await db.commit()
                except:     # suppress E722
                    pass
            await ctx.message.remove_reaction("🟠", ctx.guild.me)
            await ctx.message.add_reaction("✅")
            return

    att = discord.SlashCommandGroup(name="attendance", description="Commands for attendance")

    @att.command(name="reset", description="Resets attendance for members in the server")
    async def _reset(self, ctx: discord.ApplicationContext):
        await ctx.defer()
        db, cursor = await connect_to_db()
        await cursor.execute(f"SELECT attwatchrole FROM ServerConfig WHERE ServerID = {ctx.guild.id}")
        roleID = await cursor.fetchone()
        role = ctx.guild.get_role(roleID[0])
        members = []
        attendance_result = ResetJSONManager()
        if role is None:
            role = await ctx.guild._fetch_role(roleID)

        for member in ctx.guild.members:
            if role in member.roles:
                members.append(member)
        for member in members:
            async with db.execute(f'''
                SELECT attendanceNum AS old_attendanceNum
                FROM attendance
                WHERE ID = {member.id}
                LIMIT 1
            ''') as cursor:
                previous_value = await cursor.fetchone()

            # Update the record and set the 'attendanceNum' field to 0
            await db.execute(f'''
                UPDATE attendance
                SET attendanceNum = 0
                WHERE ID = {member.id}
            ''')

            # Commit the changes
            await db.commit()
            attendance_result.add(previous_value[0], member.display_name)
        await ctx.respond("Reset attendance for all members in the server")
        # logger.success(f"Attendance Reset: {ctx.guild.name}")
        embed = reset_embed_generator(attendance_result.sort().get_obj())
        await ctx.respond(embed=embed)
        log.success(f"Attendance Reset: {ctx.guild.name}")
        return


def setup(bot: DatacoreBot):
    bot.add_cog(Attendance(bot))
