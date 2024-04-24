# import aiosqlite
import discord
from discord import option
from discord.ext import commands
from Bot.DatacoreBot import DatacoreBot
# from Bot.utils.DB import connect_to_db
# from Bot.utils.kmcbitroles import RoleSwitcher

"""
Table:
ID | RoleInt |
"""




def role_select(ctx: discord.AutocompleteContext):
    path = ctx.options["path"]
    match path:
        case "Anti-Armour":
            return [
                "Anti-Armour", "Advanced Anti-Armour", "Anti-Armour Instructor", "Advanced Anti-Armour Instructor",
                "Anti-Armour Cadre", "Head Anti-Armour Cadre"
                    ]
        case "Marksman":
            return [
                "Marksman", "Advanced Marksman", "Marksman Instructor", "Advanced Marksman Instructor", "Marksman Cadre",
                "Head Marksman Cadre"
                    ]
        case "Rifleman":
            return [
                "Rifleman", "Advanced Rifleman", "Rifleman Instructor", "Advanced Rifleman Instructor", "Rifleman Cadre",
                "Head Rifleman Cadre"
                    ]
        case "ARC":
            return [
                "ARC Candidate", "Advanced Recon Commando", "ARC Instructor", "ARC Cadre", "Head ARC Cadre"
                    ]
        case "RC":
            return [
                "RC Candidate", "Republic Commando", "RC Instructor", "RC Cadre", "Head RC Cadre"
                    ]



class KMC(commands.Cog):
    def __init__(self, bot: DatacoreBot):
        self.bot = bot

    kmc = discord.SlashCommandGroup("kmc", guild_only=True)

    @kmc.command()
    @option(name="path", description="Pathway", choices=["Anti-Armour", "Rifleman", "Marksman", "ARC", "RC"])
    @option(name="role", desciption="Role to add", autocomplete=role_select)
    async def _add(self, ctx: discord.ApplicationContext, path: str):
        pass


# def setup(bot: DatacoreBot):
#     bot.add_cog(KMC(bot))
