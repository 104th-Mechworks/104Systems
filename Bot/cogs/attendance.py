import datetime
import json
import os

import aiosqlite
import discord
from discord.ext import commands
from Bot.DatacoreBot import DatacoreBot
from Bot.utils.logger import logger as log
from Bot.utils.DB import connect_to_db, close_db



def createResetFile(json_obj):
    """
    create a file to store the reset data with the format:
    Attendance: 0
    member1
    member2

    Attendance: 1
    ...
    """
    with open("reset.txt", "w") as f:
        for key, value in json_obj.items():
            f.write(f"Attendance: {key}\n")
            for member in value:
                f.write(f"{member}\n")
            f.write("\n")
    return os.path.abspath("reset.txt")







class ResetJSONManager:
    """
    Class to manage the JSON object for the reset command
    """
    def __init__(self):
        self.json_obj = {}

    def add(self, key, value) -> None:
        """
        Add a key/value pair to the dictionary
        :param key: int
        :param value: str
        """
        if key in self.json_obj:
            # If key already exists, append the value to the existing list
            self.json_obj[key].append(value)
        else:
            # If key doesn't exist, create a new list with the value
            self.json_obj[key] = [value]

    def get_obj(self, key=None):
        """
        Get the dictionary or a specific key from the dictionary
        :param key: (optional)
        :return: list[str] or dict
        """
        if key is None:
            # If no key is specified, return the entire dictionary
            return self.json_obj
        return self.json_obj[key]

    def sort(self):
        # Sort the dictionary by key
        self.json_obj = dict(sorted(self.json_obj.items()))
        return self


def reset_embed_generator(json_obj) -> discord.Embed:
    """
    Creates the embed message that contains list of members and their attendance
    """
    embed = discord.Embed(
        title="Attendance Reset",
        description="Attendance has been reset for the following members:",
        color=discord.Color.green(),
    )

    # Iterates through the dictionary and add each key/value pair to the embed
    for key, value in json_obj.items():
        values = "\n".join(value)
        embed.add_field(name=f"Attendance: {key}", value=values, inline=False)

    return embed


class Attendance(commands.Cog):
    def __init__(self, bot: DatacoreBot):
        self.bot = bot

    @commands.command(name="attendance")
    async def attendance(self, ctx: commands.Context):
        # checks there is at least 1 member to log attendance for
        if len(ctx.message.mentions) == 0:
            msg = await ctx.reply("Must have at least 1 member mentioned")
            await msg.delete(delay=5)
            return
        else:
            db, cursor = await connect_to_db()
            # if this reaction isn't removed the user knows there has been a problem
            await ctx.message.add_reaction(b'\xf0\x9f\x9f\xa0'.decode())
            for member in ctx.message.mentions:
                counter = 0
                try:
                    await cursor.execute("SELECT attendanceNum FROM attendance WHERE ID=?", (member.id,))
                    num = await cursor.fetchone()
                    await cursor.execute(
                        "UPDATE attendance SET attendanceNum = attendanceNum + 1 WHERE ID = ?", (member.id,)
                    )
                    await db.commit()
                    await cursor.execute("SELECT attendanceNum FROM attendance WHERE ID=?", (member.id,))
                    unum = await cursor.fetchone()
                    # if fails try until it updates the record for the specified member (usually due to file locking)
                    while (unum[0] == num[0]) and (counter < 5):
                        counter += 1
                        print("not updated correctly")
                        await cursor.execute("SELECT attendanceNum FROM attendance WHERE ID=?", (member.id,))
                        num = await cursor.fetchone()
                        await cursor.execute(
                            "UPDATE attendance SET attendanceNum = attendanceNum + 1 WHERE ID = ?", (member.id,)
                        )
                        await db.commit()
                        await cursor.execute("SELECT attendanceNum FROM attendance WHERE ID=?", (member.id,))
                        unum = await cursor.fetchone()
                    await db.commit()
                    if counter == 5:
                        await ctx.message.remove_reaction(b'\xf0\x9f\x9f\xa0'.decode(), ctx.guild.me)
                        await ctx.message.add_reaction(b'\xe2\x9d\x8c'.decode())
                        await ctx.send(f"Failed to update {member.display_name}'s attendance, previous members were updated")
                        return
                except:  # suppress E722 (blank exception clause)
                    pass
            await ctx.message.remove_reaction(b'\xf0\x9f\x9f\xa0'.decode(), ctx.guild.me)
            await ctx.message.add_reaction(b'\xe2\x9c\x85'.decode())
            return

    att = discord.SlashCommandGroup(
        name="attendance", description="Commands for attendance"
    )

    @att.command(name="setup", description="Sets up attendance for the server")
    async def _setup(
        self,
        ctx: discord.ApplicationContext,
        role: discord.Role,
        channel: discord.TextChannel,
    ):
        """
        selects the channel to which the control messages are sent and which role is associated with that platoon
        or company. Only members with the chosen role are reset
        """
        db, cursor = await connect_to_db("main.sqlite")
        await cursor.execute(
            f"SELECT AchannelID, attwatchrole FROM ServerConfig WHERE ID = {ctx.guild.id}"
        )
        result = await cursor.fetchone()
        if result is None:
            await cursor.execute(
                f"INSERT INTO ServerConfig (ID, AchannelID, attwatchrole) VALUES ({ctx.guild.id}, {channel.id}, {role.id})"
            )
        else:
            await cursor.execute(
                f"UPDATE ServerConfig SET AchannelID = {channel.id}, attwatchrole = {role.id} WHERE ID = {ctx.guild.id}"
            )
        await db.commit()
        await cursor.close()
        await db.close()
        await ctx.respond(
            f"Updated {ctx.guild.name} attendance channel and role", ephemeral=True
        )


    @att.command(
        name="reset", description="Resets attendance for members in the server"
    )
    @commands.has_permissions(manage_roles=True)
    async def _reset(self, ctx: discord.ApplicationContext):
        """
        resets attendance for all members in the server with the specified role from the setup command
        """
        await ctx.defer()

        resettingEmbed = discord.Embed(
            title="Resetting attendance",
            description="Please hold all raid-logs until attendance has been reset",
            color=discord.Color.red(),
            timestamp=datetime.datetime.utcnow(),
        ).set_footer(
            text=f"{ctx.user.display_name}"
        )

        resetEmbed = discord.Embed(
            title="Attendance Reset",
            description="Raid-logs can resume",
            color=discord.Color.green(),
            timestamp=datetime.datetime.utcnow(),
        ).set_footer(
            text=f"{ctx.user.display_name}"
        )

        async with aiosqlite.connect("main.sqlite") as db:
            async with db.execute(
                    f"SELECT attwatchrole FROM ServerConfig WHERE ID = {ctx.guild.id}"
            ) as cursor:
                roleID = await cursor.fetchone()

            async with db.execute(
                    f"SELECT AchannelID FROM ServerConfig WHERE ID = {ctx.guild.id}"
            ) as cursor:
                channelID = await cursor.fetchone()

            achannel = ctx.guild.get_channel(channelID[0])
            if achannel is None:
                achannel = await ctx.guild.fetch_channel(channelID[0])

            msg = await achannel.send(embed=resettingEmbed)

            role = ctx.guild.get_role(roleID[0])
            if role is None:
                role = await ctx.guild._fetch_role(roleID[0])

            members = []
            attendance_result = ResetJSONManager()

            for member in ctx.guild.members:
                if role in member.roles:
                    members.append(member)

            for member in members:
                async with db.execute(
                        f"""
                    SELECT attendanceNum AS old_attendanceNum
                    FROM attendance
                    WHERE ID = {member.id}
                    LIMIT 1
                """
                ) as cursor:
                    previous_value = await cursor.fetchone()

                await db.execute(
                    f"""
                    UPDATE attendance
                    SET attendanceNum = 0
                    WHERE ID = {member.id}
                """
                )
                await db.commit()
                if previous_value is None:
                    continue

                # Commit the changes

                attendance_result.add(previous_value[0], member.display_name)
        await ctx.respond("Reset attendance for all members in the server")
        # logger.success(f"Attendance Reset: {ctx.guild.name}")
        json_obj = attendance_result.sort().get_obj()
        embed = reset_embed_generator(json_obj)

        await msg.edit(embed=resetEmbed)
        try:
            await ctx.respond(embed=embed)
        except discord.HTTPException:
            await ctx.respond("Too many members to display", ephemeral=True)
             # create a file to store the reset data, send the file then delete the file on the machine
            createResetFile(json_obj)
            await ctx.respond(file=discord.File("reset.txt"))

            os.remove("reset.txt")
        await msg.edit(embed=resetEmbed)
        log.success(f"Attendance Reset: {ctx.guild.name}")
        return

    @att.command(name="view", description="View attendance for a member")
    async def _view(
        self, ctx: discord.ApplicationContext, member: discord.Member = None
    ) -> None:
        """
        Command to view the attendance of a member

        :param member: discord.Member - The member to view the attendance of
        """
        if member is None:
            member = ctx.author

        async with aiosqlite.connect("main.sqlite") as db:
            async with db.execute(
                    f"SELECT attendanceNum FROM attendance WHERE ID = {member.id}"
            ) as cursor:
                result = await cursor.fetchone()

        if result is None:
            await ctx.respond(
                f"{member.display_name} not in database. Run `/data add` to add them"
            )
        else:
            await ctx.respond(f"{member.display_name} has attended {result[0]} events", ephemeral=True)
        return

    # debugging commands. These are not meant to be used in production

    @commands.command()
    async def set_att(self, ctx: commands.Context, member: discord.Member, num: int):
        """
        Manually set attendance number for specified member
        :param ctx: commands.Context
        :param member: discord.Member
        :param num: int
        """
        db, cursor = await connect_to_db("main.sqlite")
        await cursor.execute(
            f"UPDATE attendance SET attendanceNum = {num} WHERE ID = {member.id}"
        )
        await db.commit()
        await cursor.close()
        await db.close()
        await ctx.reply(
            f"Attendance set to {num} for {member.display_name}", ephemeral=True
        )

    @commands.is_owner()
    @commands.command()
    async def man_add(self, ctx: commands.Context, ID: int, *name: str):
        db, cursor = await connect_to_db()
        name = str(name).split(" ")

        await cursor.execute(
            f"INSERT INTO attendance (ID, attendanceNum) VALUES ({ID}, 0)"
        )
        await cursor.execute(
            f"INSERT INTO members (ID, Rank, Name, Designation) VALUES ({ID}, {name[0]}, {name[1]}, {name[2]})"
        )
        await db.commit()
        await cursor.close()
        await db.close()
        await ctx.reply(f"Member added to database, {ctx.author.d}", ephemeral=True)


    @commands.is_owner()
    @commands.command()
    async def mset(self, ctx: commands.Context):
        async with aiosqlite.connect(self.bot.DB_PATH) as db:
            async with db.cursor() as cursor:
                for member in ctx.guild.members:
                    await cursor.execute(
                        f"INSERT IGNORE INTO Members (ID) VALUES ({member.id})"
                    )
                    await cursor.execute(
                        f"INSERT INTO attendance (ID, attendanceNum) VALUES ({member.id}, 0)"
                    )
                await db.commit()

        await ctx.reply("Members added to database", ephemeral=True)


def setup(bot: DatacoreBot):
    bot.add_cog(Attendance(bot))
