import discord
from Bot.DatacoreBot import DatacoreBot
from discord.ext import commands


async def promote(self, ctx, user: discord.Member, Rank):
    channel = self.client.get_channel(587245417213722627)
    guild = self.client.get_guild(337554143000526850)
    newRank = " "

    command_staff = {
        "CDR": 676879791818801162,
        "BCDR": 567059970990931979,
        "SCDR": 564628850735185941,
        "MCDR": 570996998300499968,
        "NCPT": 583045910934585477,
        "MCPO": 583044691436503130,
        "COM": 583045197676675082,
        "GEN": 676873491102040099
    }

    army_ranks = {
        "LCPL": 739975590165217301,
        "CPL": 723076260582129705,
        "SGT": 723076262867894272,
        "SGM": 524036023907516448,
        "2LT": 563759504253124613,
        "LT": 345199062917840909,
        "CPT": 345198589275930634,
        "MAJ": 562054467412033549
    }

    navy_ranks = {
        "PO3": 723079853586382869,
        "PO2": 723079688268021791,
        "PO1": 583462759514112001,
        "NLT": 583045556067237898,
        "LCDTR": 583046091885510676,
        "NCDR": 583044948358594657,
        "NCPT": 583045910934585477
    }

    sf_ranks = {
        "ARC": 653192681618669579,
        "PVT": 830926428916547604,
        "ASGT": 385907972959764491,
        "RSGT": 830926587607908363,
        "ALT": 597125161363439626,
        "ACPT": 595662978292908103,
        "COM": 583045197676675082,
        "GEN": 676873491102040099
    }

    valid = False
    if Rank in army_ranks:

        for i in army_ranks.values():
            if ctx.author.top_role.id in army_ranks.values():
                newRank = army_ranks[Rank]
                valid = True

        for i in command_staff.values():
            if ctx.author.top_role.id in command_staff.values():
                newRank = army_ranks[Rank]
                valid = True

    if Rank in sf_ranks:

        for i in army_ranks.values():
            if ctx.author.top_role.id in sf_ranks.values():
                newRank = sf_ranks[Rank]
                valid = True

        for i in command_staff.values():
            if ctx.author.top_role.id in command_staff.values():
                newRank = sf_ranks[Rank]
                valid = True

    if Rank in navy_ranks:

        for i in navy_ranks.values():
            if ctx.author.top_role.id in navy_ranks.values():
                newRank = navy_ranks[Rank]
                valid = True

        for i in command_staff.values():
            if ctx.author.top_role.id in command_staff.values():
                newRank = navy_ranks[Rank]
                valid = True

    oldnick = user.display_name
    list = user.display_name.split()
    nickLen = len(list[0])
    newNick = oldnick[nickLen:]
    newNick = Rank + newNick

    if valid:
        if ctx.author.top_role.position > user.top_role.position:
            if (user.top_role.id not in army_ranks.values()) and (user.top_role.id not in navy_ranks.values()) and (
                    user.top_role.id not in sf_ranks.values()):
                role = guild.get_role(newRank)
                await user.add_roles(role)

                newRank = guild.get_role(newRank)
                newRank = newRank.name

            else:
                await user.remove_roles(user.top_role)

                role = guild.get_role(newRank)
                await user.add_roles(role)

                newRank = guild.get_role(newRank)
                newRank = newRank.name

            await channel.send(f"{user.display_name} ---> {newRank}")
            await ctx.send(f"Successfully promoted {user.display_name} to {newRank}")
            await user.edit(nick=newNick)

        else:
            await ctx.send("You cannot promote someone to a rank equal or above your own.")

    elif not valid:
        await ctx.send(
            "The rank you put entered is not valid. Check it exists and the abbrevation is correct or that you have perms to access it.")


async def demote(self, ctx, user: discord.Member, Rank):
    channel = self.client.get_channel(587245417213722627)
    guild = self.client.get_guild(337554143000526850)
    newRank = " "

    command_staff = {
        "CDR": 676879791818801162,
        "BCDR": 567059970990931979,
        "SCDR": 564628850735185941,
        "MCDR": 570996998300499968,
        "NCDR": 583044948358594657,
        "NCPT": 583045910934585477,
        "MCPO": 583044691436503130,
        "COM": 583045197676675082,
        "GEN": 676873491102040099
    }

    army_ranks = {
        "LCPL": 739975590165217301,
        "CPL": 723076260582129705,
        "SGT": 723076262867894272,
        "SGM": 524036023907516448,
        "2LT": 563759504253124613,
        "LT": 345199062917840909,
        "CPT": 345198589275930634,
        "MAJ": 562054467412033549
    }

    navy_ranks = {
        "PO3": 723079853586382869,
        "PO2": 723079688268021791,
        "PO1": 583462759514112001,
        "NLT": 583045556067237898,
        "LCDTR": 583046091885510676,
        "NCDR": 583044948358594657,
        "NCPT": 583045910934585477
    }

    sf_ranks = {
        "ARC": 653192681618669579,
        "PVT": 830926428916547604,
        "ASGT": 385907972959764491,
        "RSGT": 830926587607908363,
        "ALT": 597125161363439626,
        "ACPT": 595662978292908103,
        "COM": 583045197676675082,
        "GEN": 676873491102040099
    }

    valid = False
    if Rank in army_ranks:

        for i in army_ranks.values():
            if ctx.author.top_role.id in army_ranks.values():
                newRank = army_ranks[Rank]
                valid = True

        for i in command_staff.values():
            if ctx.author.top_role.id in command_staff.values():
                newRank = army_ranks[Rank]
                valid = True

    if Rank in sf_ranks:

        for i in army_ranks.values():
            if ctx.author.top_role.id in sf_ranks.values():
                newRank = sf_ranks[Rank]
                valid = True

        for i in command_staff.values():
            if ctx.author.top_role.id in command_staff.values():
                newRank = sf_ranks[Rank]
                valid = True

    if Rank in navy_ranks:

        for i in navy_ranks.values():
            if ctx.author.top_role.id in navy_ranks.values():
                newRank = navy_ranks[Rank]
                valid = True

        for i in command_staff.values():
            if ctx.author.top_role.id in command_staff.values():
                newRank = navy_ranks[Rank]
                valid = True

    if Rank == 'CT':
        newRank = 'CT'
        valid = True

    oldnick = user.display_name
    list = user.display_name.split()
    nickLen = len(list[0])
    newNick = oldnick[nickLen:]
    newNick = Rank + newNick

    if valid:
        if ctx.author.top_role.position > user.top_role.position:
            if newRank == 'CT':
                await user.remove_roles(user.top_role)
                newRank = "Clone Trooper"

            else:
                await user.remove_roles(user.top_role)

                role = guild.get_role(newRank)
                await user.add_roles(role)

                newRank = guild.get_role(newRank)
                newRank = newRank.name

            await channel.send(f"{user.display_name} ---> {newRank}")
            await ctx.send(f"Successfully demoted {user.display_name} to {newRank}")
            await user.edit(nick=newNick)

        else:
            await ctx.send("You cannot demote someone a rank equal or above your own.")

    elif not valid:
        await ctx.send(
            "The rank you put entered is not valid. Check it exists and the abbrevation is correct or that you have perms to access it.")