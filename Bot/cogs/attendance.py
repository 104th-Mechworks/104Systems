import datetime

import aiosqlite
import discord
from discord import Embed
from discord.ext import commands


async def check_cache(guild: discord.Guild):
    r0 = discord.utils.get(guild.roles, name="Game Attendance: 0")
    r1 = discord.utils.get(guild.roles, name="Game Attendance: 1")
    r2 = discord.utils.get(guild.roles, name="Game Attendance: 2")
    r3 = discord.utils.get(guild.roles, name="Game Attendance: 3")
    r4 = discord.utils.get(guild.roles, name="Game Attendance: 4")
    r5 = discord.utils.get(guild.roles, name="Game Attendance: 5")
    r6 = discord.utils.get(guild.roles, name="Game Attendance: 6")
    r7 = discord.utils.get(guild.roles, name="Game Attendance: 7")
    r8 = discord.utils.get(guild.roles, name="Game Attendance: 8")
    r9 = discord.utils.get(guild.roles, name="Game Attendance: 9")
    r10 = discord.utils.get(guild.roles, name="Game Attendance: 10+")
    if any([r0, r1, r2, r3, r4, r5, r6, r7, r8, r9, r10]) is None:
        return 404
    else:
        return [r0, r1, r2, r3, r4, r5, r6, r7, r8, r9, r10]


async def fetch_Aroles(guild: discord.Guild):
    db = await aiosqlite.connect("main.sqlite")
    cursor = await db.cursor()
    await cursor.execute(
        f"SELECT A0r, A1r, A2r, A3r, A4r, A5r, A6r, A7r, A8r, A9r, A10r FROM ServerConfig WHERE ID = {guild.id}"
    )
    roles = await cursor.fetchone()
    if roles is None:
        await cursor.close()
        await db.close()

    Arolesg = []
    for roleid in roles:
        role = guild.get_role(roleid)
        if role is None:
            try:
                role = await guild._fetch_role(roleid)
                if role is None:
                    Arolesf = await _fetch_Aroles(guild=guild, rolesID=roles)
                    return Arolesf
            except:
                print("error")
        Arolesg.append(role)
    return Arolesg


async def _fetch_Aroles(guild: discord.Guild, rolesID: list | tuple):
    Aroles: list = []
    rolesL = await guild.fetch_roles()
    for rid in rolesID:
        for role in rolesL:
            if role.id == rid:
                Aroles.append(role)

    return Aroles


async def channel_query(guild_id: int):
    db = await aiosqlite.connect("main.sqlite")
    cursor = await db.cursor()
    await cursor.execute(f"SELECT AchannelID FROM ServerConfig WHERE ID = {guild_id}")
    channel_id = await cursor.fetchone()
    await cursor.close()
    await db.close()
    if channel_id is None:
        return "Not found"
    else:
        return channel_id[0]


class Attendance(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        print("attendance cog ready")

    @commands.command()
    async def attendance(self, ctx: commands.Context):
        Aroles = await check_cache(ctx.guild)
        if Aroles == 404:
            Aroles = await fetch_Aroles(ctx.guild)
        await ctx.message.add_reaction("🟠")

        for member in ctx.message.mentions:
            if Aroles[0] in member.roles:
                await member.remove_roles(Aroles[0])
                await member.add_roles(Aroles[1])
            elif Aroles[1] in member.roles:
                await member.remove_roles(Aroles[1])
                await member.add_roles(Aroles[2])
            elif Aroles[2] in member.roles:
                await member.remove_roles(Aroles[2])
                await member.add_roles(Aroles[3])
            elif Aroles[3] in member.roles:
                await member.remove_roles(Aroles[3])
                await member.add_roles(Aroles[4])
            elif Aroles[4] in member.roles:
                await member.remove_roles(Aroles[4])
                await member.add_roles(Aroles[5])
            elif Aroles[5] in member.roles:
                await member.remove_roles(Aroles[5])
                await member.add_roles(Aroles[6])
            elif Aroles[6] in member.roles:
                await member.remove_roles(Aroles[6])
                await member.add_roles(Aroles[7])
            elif Aroles[7] in member.roles:
                await member.remove_roles(Aroles[7])
                await member.add_roles(Aroles[8])
            elif Aroles[8] in member.roles:
                await member.remove_roles(Aroles[8])
                await member.add_roles(Aroles[9])
            elif Aroles[9] in member.roles:
                await member.remove_roles(Aroles[9])
                await member.add_roles(Aroles[10])
            elif Aroles[10] in member.roles:
                await member.remove_roles(Aroles[10])
                await member.add_roles(Aroles[0])

        await ctx.message.remove_reaction("🟠", ctx.guild.me)
        await ctx.message.add_reaction("✅")

    att = discord.SlashCommandGroup(
        name="attendance", description="Attendance commands"
    )

    @att.command(name="reset", description="Reset attendance roles")
    async def _reset(self, ctx: discord.ApplicationContext):
        await ctx.interaction.response.defer()
        Aroles = await check_cache(ctx.guild)
        if Aroles == 404:
            Aroles = await fetch_Aroles(ctx.guild)

        embed1: Embed = discord.Embed(
            title="Attendance Reset",
            description=f"Hold raid logs till further notice",
            color=discord.Color.from_rgb(236, 40, 40),
        )
        embed1.set_footer(text=f"Requested by {ctx.user.display_name}")
        embed1.timestamp = datetime.datetime.utcnow()

        embed2 = discord.Embed(
            title="Attendance Reset",
            description=f"Attendance has been reset. Raid logs may resume",
            color=discord.Color.from_rgb(27, 192, 27),
        )
        embed2.set_footer(text=f"Requested by {ctx.user.display_name}")
        embed2.timestamp = datetime.datetime.utcnow()
        RLogChannel = await channel_query(ctx.guild.id)
        RLogChannel = ctx.guild.get_channel(RLogChannel)
        if RLogChannel is None:
            RLogChannel = ctx.guild.fetch_channel(RLogChannel)
        msg = await RLogChannel.send(embed1)

        l0 = []
        l1 = []
        l2 = []
        l3 = []
        l4 = []
        l5 = []
        l6 = []
        l7 = []
        l8 = []
        l9 = []
        l10 = []

        for member in ctx.guild.members:
            if Aroles[1] in member.roles:
                await member.remove_roles(Aroles[1])
                await member.add_roles(Aroles[0])
                l1.append(member.display_name)
            elif Aroles[2] in member.roles:
                await member.remove_roles(Aroles[2])
                await member.add_roles(Aroles[0])
                l2.append(member.display_name)
            elif Aroles[3] in member.roles:
                await member.remove_roles(Aroles[3])
                await member.add_roles(Aroles[0])
                l3.append(member.display_name)
            elif Aroles[4] in member.roles:
                await member.remove_roles(Aroles[4])
                await member.add_roles(Aroles[0])
                l4.append(member.display_name)
            elif Aroles[5] in member.roles:
                await member.remove_roles(Aroles[5])
                await member.add_roles(Aroles[0])
                l5.append(member.display_name)
            elif Aroles[6] in member.roles:
                await member.remove_roles(Aroles[6])
                await member.add_roles(Aroles[0])
                l6.append(member.display_name)
            elif Aroles[7] in member.roles:
                await member.remove_roles(Aroles[7])
                await member.add_roles(Aroles[0])
                l7.append(member.display_name)
            elif Aroles[8] in member.roles:
                await member.remove_roles(Aroles[8])
                await member.add_roles(Aroles[0])
                l8.append(member.display_name)
            elif Aroles[9] in member.roles:
                await member.remove_roles(Aroles[9])
                await member.add_roles(Aroles[0])
                l9.append(member.display_name)
            elif Aroles[10] in member.roles:
                await member.remove_roles(Aroles[10])
                await member.add_roles(Aroles[1])
                l10.append(member.display_name)
            elif Aroles[0] in member.roles:
                l0.append(member.display_name)
            else:
                pass

        await msg.edit(embed=embed2)
        embed = discord.Embed(
            title="Attendance Reset",
        )
        if len(l0) != 0:
            l0str = "\n".join(str(x) for x in l0)
            embed.add_field(
                name="Game Attendance: 0",
                value=f"{len(l0)} members had game attendance 0\n**members:**\n{l0str}",
                inline=False,
            )
        if len(l1) != 0:
            l1str = "\n".join(str(x) for x in l1)
            embed.add_field(
                name="Game Attendance: 1",
                value=f"{len(l1)} members had game attendance 1\n**members:**\n{l1str}",
                inline=False,
            )
        if len(l2) != 0:
            l2str = "\n".join(str(x) for x in l2)
            embed.add_field(
                name="Game Attendance: 2",
                value=f"{len(l2)} members had game attendance 2\n**members:**\n{l2str}",
                inline=False,
            )
        if len(l3) != 0:
            l3str = "\n".join(str(x) for x in l3)
            embed.add_field(
                name="Game Attendance: 3",
                value=f"{len(l3)} members had game attendance 3\n**members:**\n{l3str}",
                inline=False,
            )
        if len(l4) != 0:
            l4str = "\n".join(str(x) for x in l4)
            embed.add_field(
                name="Game Attendance: 4",
                value=f"{len(l4)} members had game attendance 4\n**members:**\n{l4str}",
                inline=False,
            )
        if len(l5) != 0:
            l5str = "\n".join(str(x) for x in l5)
            embed.add_field(
                name="Game Attendance: 5",
                value=f"{len(l5)} members had game attendance 5\n**members:**\n{l5str}",
                inline=False,
            )
        if len(l6) != 0:
            l6str = "\n".join(str(x) for x in l6)
            embed.add_field(
                name="Game Attendance: 6",
                value=f"{len(l6)} members had game attendance 6\n**members:**\n{l6str}",
                inline=False,
            )
        if len(l7) != 0:
            l7str = "\n".join(str(x) for x in l7)
            embed.add_field(
                name="Game Attendance: 7",
                value=f"{len(l7)} members had game attendance 7\n**members:**\n{l7str}",
                inline=False,
            )
        if len(l8) != 0:
            l8str = "\n".join(str(x) for x in l8)
            embed.add_field(
                name="Game Attendance: 8",
                value=f"{len(l8)} members had game attendance 8\n**members:**\n{l8str}",
                inline=False,
            )
        if len(l9) != 0:
            l9str = "\n".join(str(x) for x in l9)
            embed.add_field(
                name="Game Attendance: 9",
                value=f"{len(l9)} members had game attendance 9\n**members:**\n{l9str}",
                inline=False,
            )
        if len(l10) != 0:
            l10str = "\n".join(str(x) for x in l10)
            embed.add_field(
                name="Game Attendance: 10",
                value=f"{len(l10)} members had game attendance 10\n**members:**\n{l10str}",
                inline=False,
            )
        tmstp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S") + " UTC"
        embed.set_footer(text=f"Reset by {ctx.user.display_name} at {tmstp}")

        await ctx.followup.send(embed=embed, ephemeral=True)
        await ctx.user.send(embed=embed)

    @commands.is_owner()
    @commands.guild_only()
    @att.command(name="setup", description="Setup attendance system")
    async def _setup(
        self,
        ctx: discord.ApplicationContext,
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
        attendance_channel: discord.TextChannel,
    ):
        db = await aiosqlite.connect("main.sqlite")
        cursor = await db.cursor()
        await cursor.execute(f"SELECT ID FROM ServerConfig WHERE ID = {ctx.guild.id}")
        result = await cursor.fetchone()
        if result is None:
            try:
                await cursor.execute(
                    f"INSERT INTO ServerConfig (ID, A0r, A1r, A2r, A3r, A4r, A5r, A6r, A7r, A8r, A9r, A10r, AchannelID) VALUES ({ctx.guild.id}, {a0.id}, {a1.id}, {a2.id}, {a3.id}, {a4.id}, {a5.id}, {a6.id}, {a7.id}, {a8.id}, {a9.id}, {a10.id}, {attendance_channel.id})"
                )
                await db.commit()
                await ctx.respond("Attendance system setup", ephemeral=True)
            except Exception as e:
                print(e)
                await ctx.interaction.response.send_message(
                    "Something went wrong", ephemeral=True
                )
                await db.rollback()
                await db.commit()
                await db.close()
                return
        else:
            await ctx.respond("Attendance system is already setup", ephemeral=True)

    @att.command(name="vc", description="loggs attendance for people in a vc")
    async def _vc(
        self,
        ctx: discord.ApplicationContext,
        AType: discord.Option(
            input_type=str, name="type", description="Type of attendance"
        ),
    ):
        if ctx.user.voice is None:
            await ctx.respond("You are not in a vc", ephemeral=True)
            return
        else:
            if len(ctx.user.voice.channel.members) == 1:
                await ctx.respond("There must be at least 2 people in the vc")
                return
            else:
                db = await aiosqlite.connect("main.sqlite")
                cursor = await db.cursor()
                await cursor.execute(
                    f"SELECT AchannelID FROM ServerConfig WHERE ID={ctx.guild.id}"
                )
                AlogID = await cursor.fetchone()
                await cursor.close()
                await db.close()
                Alog: discord.TextChannel = ctx.guild.get_channel(AlogID)
                if Alog is None:
                    Alog: discord.TextChannel = ctx.guild.fetch_channel(AlogID)
                members = ctx.user.voice.channel.members
                memberMentions: list = []
                for member in members:
                    if member.bot:
                        members.remove(member)
                    else:
                        memberMentions.append(member.mention)

                msg = await Alog.send(
                    f"Attendance\nType: {AType}\nDate: {datetime.date.today().strftime('%d-%m-%Y')}\nAttendees:\n{memberMentions}"
                )
                Aroles = await check_cache(ctx.guild)
                if Aroles == 404:
                    Aroles = await fetch_Aroles(ctx.guild)
                await msg.add_reaction("🟠")

                for member in ctx.message.mentions:
                    if Aroles[0] in member.roles:
                        await member.remove_roles(Aroles[0])
                        await member.add_roles(Aroles[1])
                    elif Aroles[1] in member.roles:
                        await member.remove_roles(Aroles[1])
                        await member.add_roles(Aroles[2])
                    elif Aroles[2] in member.roles:
                        await member.remove_roles(Aroles[2])
                        await member.add_roles(Aroles[3])
                    elif Aroles[3] in member.roles:
                        await member.remove_roles(Aroles[3])
                        await member.add_roles(Aroles[4])
                    elif Aroles[4] in member.roles:
                        await member.remove_roles(Aroles[4])
                        await member.add_roles(Aroles[5])
                    elif Aroles[5] in member.roles:
                        await member.remove_roles(Aroles[5])
                        await member.add_roles(Aroles[6])
                    elif Aroles[6] in member.roles:
                        await member.remove_roles(Aroles[6])
                        await member.add_roles(Aroles[7])
                    elif Aroles[7] in member.roles:
                        await member.remove_roles(Aroles[7])
                        await member.add_roles(Aroles[8])
                    elif Aroles[8] in member.roles:
                        await member.remove_roles(Aroles[8])
                        await member.add_roles(Aroles[9])
                    elif Aroles[9] in member.roles:
                        await member.remove_roles(Aroles[9])
                        await member.add_roles(Aroles[10])
                    elif Aroles[10] in member.roles:
                        await member.remove_roles(Aroles[10])
                        await member.add_roles(Aroles[0])

                await msg.remove_reaction("🟠", ctx.guild.me)
                await msg.add_reaction("✅")


def setup(bot: commands.Bot):
    bot.add_cog(Attendance(bot))
