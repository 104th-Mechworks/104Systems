import discord
from discord.ext import commands
from Bot.DatacoreBot import DatacoreBot
from Bot.utils.logger import logger as log
from Bot.utils.DB import connect_to_db
from discord.commands import option

# handels the rosters for all cshop teams
"""
TABLE:
ID: member id

JsonObject handler:
"""


def cshop_team_position(ctx: discord.AutocompleteContext):
    if ctx.options["team"] == "Administration":
        return [
            "Chief of Analysis",
            "Deputy Chief of Analysis",
            "Console Level Administrator",
            "Company Level Administrator",
            "Platoon Level Administrator",
        ]
    if ctx.options["team"] == "Vanguard Security Team":
        return ["Lead", "Asst. Lead", "Support Staff"]
    if ctx.options["team"] == "Art Team":
        return [
            "Lead",
            "Senior Artist",
            "Primary Artist",
        ]
    if ctx.options["team"] == "Kaminoan Security Force":
        return [
            "Head Kaminoan Security Officer",
            "Kaminoan Customs Officer",
            "Kaminoan Security Officer",
            "Kaminoan Security Investigator",
            "Kaminoan Security Reserves",
        ]
    if ctx.options["team"] == "104th Security":
        return [
            "Desert Trooper",
        ]


class CShopObjectHandler:
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


async def team_switcher(team):
    if team == "Administration":
        return "admin"
    elif team == "Vanguard Security":
        return "vanguard_security"
    elif team == "Kaminoan Security Force":
        return "KSF"
    elif team == "104th Security":
        return "Desert"
    elif team == "Art Team":
        return "art_team"
    else:
        return None


class CShop(commands.Cog):
    def __init__(self, bot: DatacoreBot):
        self.bot = bot

    cshp = discord.SlashCommandGroup(
        "cshop", description="CShop commands"
    )

    @cshp.command(name="add", description="Add a member to a cshop team")
    @option("member", description="Member to remove from the cshop team", required=True)
    @option(
        "team",
        required=True,
        choices=[
            "Administration",
            "Vanguard Security Team",
            "Kaminoan Security Force",
            "104th Security",
            "Art Team",
        ],
    )
    @option("position", required=True, autocomplete=cshop_team_position)
    async def add(
        self,
        ctx: discord.ApplicationContext,
        member: discord.Member,
        team: str,
        position: str,
    ):
        db, cursor = await connect_to_db()
        team_table = await team_switcher(team)
        await cursor.execute(f"SELECT ID FROM members WHERE ID = {member.id} ")
        if await cursor.fetchone() is None:
            await ctx.respond(
                f"{member.name} does not exist in the database", ephemeral=True
            )
        else:
            await cursor.execute(f"SELECT ID FROM cshop WHERE ID = {member.id}")
            if await cursor.fetchone() is None:
                await cursor.execute(
                    f"INSERT INTO cshop (ID, {team_table}) VALUES ({member.id}, '{position}')"
                )
                await db.commit()
                await cursor.close()
                await db.close()
                await ctx.respond(f"Added {member.name} to {team}", ephemeral=True)
            else:
                await cursor.execute(
                    f"UPDATE cshop SET '{team_table}' = '{position}' WHERE ID = {member.id}"
                )
                await db.commit()
                await cursor.close()
                await db.close()
                await ctx.respond(f"Updated {member.name} in {team}", ephemeral=True)

    @cshp.command(name="remove", description="Remove a member from a cshop team")
    @option("member", description="Member to remove from the cshop team", required=True)
    @option(
        "team",
        required=True,
        choices=[
            "Administration",
            "Vanguard Security Team",
            "Kaminoan Security Force",
            "104th Security",
            "Art Team",
        ],
    )
    async def remove(
        self, ctx: discord.ApplicationContext, member: discord.Member, team: str
    ):
        db, cursor = await connect_to_db()
        await cursor.execute(f"SELECT ID FROM cshop WHERE ID = {member.id}")
        if await cursor.fetchone() is None:
            await ctx.respond(
                f"{member.display_name} is not in a cshop team", ephemeral=True
            )
        else:
            team_table = await team_switcher(team)
            await cursor.execute(
                f"UPDATE cshop SET {team_table} = {None} WHERE ID = {member.id}"
            )
            await db.commit()
            await cursor.close()
            await db.close()
            await ctx.respond(
                f"Removed {member.display_name} from {team} team", ephemeral=True
            )


def setup(bot: DatacoreBot):
    bot.add_cog(CShop(bot))
