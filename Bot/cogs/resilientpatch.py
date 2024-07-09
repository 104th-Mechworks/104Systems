import asyncio

import discord
from discord.ext import commands
import logging
from Bot.DatacoreBot import DatacoreBot
from Bot.cogs.attendance import reset_embed_generator

log = logging.getLogger("Datacore")

async def fetch_or_get_role(guild: discord.Guild, role_id: int):
    role = guild.get_role(role_id)
    if role is None:
        role = await guild._fetch_role(role_id)
    return role

class ResilientPatch(commands.Cog):
    def __init__(self, bot: DatacoreBot) -> None:
        self.bot = bot

    async def load_roles(self, guild) -> list[discord.Role]:
        g = guild
        r1 = await fetch_or_get_role(guild, 1198379770967244845) # 1
        r2 = await fetch_or_get_role(guild, 1198379770967244846)
        r3 = await fetch_or_get_role(guild, 1198379770967244847)
        r4 = await fetch_or_get_role(guild, 1198379770967244848)
        r5 = await fetch_or_get_role(guild, 1198379770967244849)
        r6 = await fetch_or_get_role(guild, 1198379770984005802)
        r7 = await fetch_or_get_role(guild, 1198379770984005803)
        r8 = await fetch_or_get_role(guild, 1198379770984005804)
        r9 = await fetch_or_get_role(guild, 1198379770984005805)
        r10 = await fetch_or_get_role(guild, 1198379770984005806)
        r11 = await fetch_or_get_role(guild, 1198379770984005807)
        r12 = await fetch_or_get_role(guild, 1198379770984005808)
        r13 = await fetch_or_get_role(guild, 1198379770984005809)
        r14 = await fetch_or_get_role(guild, 1198379770984005810)
        r15 = await fetch_or_get_role(guild, 1198379770984005811)  # 15+
        return [r1, r2, r3, r4, r5, r6, r7, r8, r9, r10, r11, r12, r13, r14, r15]

    @commands.Cog.listener()
    async def on_message(self, msg: discord.Message) -> None:
        if msg.channel.id == 1198379774544969880:
            roles = await self.load_roles(msg.guild)
            for member in msg.mentions:
                if roles[0] in member.roles:
                    await member.add_roles(roles[1])
                    await member.remove_roles(roles[0])
                elif roles[1] in member.roles:
                    await member.add_roles(roles[2])
                    await member.remove_roles(roles[1])
                elif roles[2] in member.roles:
                    await member.add_roles(roles[3])
                    await member.remove_roles(roles[2])
                elif roles[3] in member.roles:
                    await member.add_roles(roles[4])
                    await member.remove_roles(roles[3])
                elif roles[4] in member.roles:
                    await member.add_roles(roles[5])
                    await member.remove_roles(roles[4])
                elif roles[5] in member.roles:
                    await member.add_roles(roles[6])
                    await member.remove_roles(roles[5])
                elif roles[6] in member.roles:
                    await member.add_roles(roles[7])
                    await member.remove_roles(roles[6])
                elif roles[7] in member.roles:
                    await member.add_roles(roles[8])
                    await member.remove_roles(roles[7])
                elif roles[8] in member.roles:
                    await member.add_roles(roles[9])
                    await member.remove_roles(roles[8])
                elif roles[9] in member.roles:
                    await member.add_roles(roles[10])
                    await member.remove_roles(roles[9])
                elif roles[10] in member.roles:
                    await member.add_roles(roles[11])
                    await member.remove_roles(roles[10])
                elif roles[11] in member.roles:
                    await member.add_roles(roles[12])
                    await member.remove_roles(roles[11])
                elif roles[12] in member.roles:
                    await member.add_roles(roles[13])
                    await member.remove_roles(roles[12])
                elif roles[13] in member.roles:
                    await member.add_roles(roles[14])
                    await member.remove_roles(roles[13])
                else:
                    await member.add_roles(roles[0])
            await msg.add_reaction("✅")

    @commands.command(aliases=["SR", "StaffReset"], hidden=True, guild_ids=[1198379770967244840])
    async def SattR(self, ctx: commands.Context) -> None:
        if ctx.channel.id == 1198379774180081702:
            m = await ctx.send("Resetting staff roles...\n*This may take a while*")
            xbsr = await fetch_or_get_role(ctx.guild, 1198379771046920285)
            wor   = await fetch_or_get_role(ctx.guild, 1198379771193737328)
            XSM = [member for member in ctx.guild.members if (xbsr in member.roles) and (wor in member.roles)]
            roles = await self.load_roles(ctx.guild)
            roles_dict = {i: [] for i in range(16)}  # Initialize dictionary with keys 0 to 15

            roles_to_remove = {role.id: [] for role in roles}  # Store members who need each role removed
            for member in XSM:
                member_roles = [role for role in roles if role in member.roles]
                if member_roles:
                    for role in member_roles:
                        index = roles.index(role) + 1
                        roles_dict[index].append(member.display_name)
                        roles_to_remove[role.id].append(member)
                else:
                    roles_dict[0].append(member.display_name)

            roles_dict = {k: v for k, v in roles_dict.items() if v != []}

            # Remove roles from members
            for role_id, members in roles_to_remove.items():
                role_to_remove = discord.utils.get(ctx.guild.roles, id=role_id)
                if role_to_remove:
                    await asyncio.gather(*[member.remove_roles(role_to_remove) for member in members])

            e = reset_embed_generator(roles_dict)
            await ctx.send(embed=e)







            await m.edit(content="Staff roles reset.")
            await m.add_reaction("✅")



def setup(bot: DatacoreBot) -> None:
    bot.add_cog(ResilientPatch(bot))
    log.info("Resilient Patch loaded.")