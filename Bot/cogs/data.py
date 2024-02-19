import json
import re
from discord.ext.pages import Paginator, PageGroup
import discord
from discord.commands import option
from discord.ext import commands
from Bot.DatacoreBot import DatacoreBot
from Bot.utils.DB import connect_to_db, close_db
from Bot.utils.data import company_name_switcher, rank_switcher
from Bot.utils.colours import (
    ARMY_COLOUR,
    SFC_COLOUR,
    AUX_COLOUR,
    FLEET_COLOUR,
    ARC_COLOUR,
    RC_COLOUR,
)
from Bot.utils.regex import FULL


async def company_autocomplete(ctx: discord.AutocompleteContext):
    branch = ctx.options["branch"]
    if branch == "Army":
        return [
            "None",
            "30th Ares Company",
            "44th Reaper Company",
            "82nd Havoc Company",
            "62nd Monarch Company",
            "29th Valkyrie Company",
            "48th Rogue Company",
            "34th Horizon Company",
            "22nd Vanguard Company",
            "60th Reconnaissance Company",
        ]
    elif branch == "Starfighter Corps":
        return [
            "None",
            "1st Fighter Obsidian Owls Wing",
            "13th Fighter Eagle's Talons Wing",
            "42nd Midnight Ravens Squadron",
        ]
    elif branch == "None":
        return ["None"]
    elif branch == "Fleet Command":
        return [
            "None",
            "30th Ares Company",
            "44th Reaper Company",
            "82nd Havoc Company",
            "62nd Monarch Company",
            "29th Valkyrie Company",
            "48th Rogue Company",
            "34th Horizon Company",
            "22nd Vanguard Company",
            "60th Reconnaissance Company",
            "1st Fighter Obsidian Owls Wing",
            "13th Fighter Eagle's Talons Wing",
            "42nd Midnight Ravens Squadron",
        ]
    elif branch == "Special Operations Force":
        return ["44th Special Operations Division"]


async def platoon_autocomplete(ctx: discord.AutocompleteContext):
    company = ctx.options["company"]
    match company:
        case "30th Ares Company":
            return ["None", "Howler", "Sentinel", "Taurus"]
        case "44th Reaper Company":
            return ["None", "Cerberus", "Ghost", "Scrapper"]
        case "82nd Havoc Company":
            return ["None", "Dagger", "Fenrir", "Titan"]
        case "62nd Monarch Company":
            return ["None", "Hound", "Ice", "Ravager"]
        case "29th Valkyrie Company":
            return ["None", "Dawn", "Ragnarok", "Solstice"]
        case "48th Rogue Company":
            return ["None", "Phoenix", "Spectre"]
        case "34th Horizon Company":
            return ["None", "Corvus", "Iridium"]
        case "22nd Vanguard Company":
            return ["Fang", "Storm", "Lightning"]
        case "60th Reconnaissance Company":
            return ["Royalty", "Tempest", "Hunter"]
        case "1st Fighter Obsidian Owls Wing":
            return ["None", "Amethyst", "Cinder"]
        case "13th Fighter Eagle's Talons Wing":
            return ["None", "Thunderbirds", "Ospreys"]
        case "42nd Midnight Ravens Squadron":
            return ["None", "Midnight Ravens", "Zillow"]
        case "44th Special Operations Division":
            return ["A Troop", "B Troop", "C Troop"]
        case _:
            return ["None"]


async def position_autocomplete(ctx: discord.AutocompleteContext):
    branch = ctx.options["branch"]
    rlist = []
    if branch == "Army":
        rlist = [
            "Army Commanding Officer",
            "Army Executive Officer",
            "Head of Console",
            "Company Commanding Officer",
            "Company Executive Officer",
            "Company Non-Commissioned Officer",
            "Platoon Commanding Officer",
            "Platoon Executive Officer",
            "Platoon Non-Commissioned Officer",
            "Squad Leader",
            "Squad Non-Commissioned Officer",
            "Fireteam Leader",
            "CT",
        ]
    elif branch == "Starfighter Corps":
        rlist = [
            "Starfighter Corps Command",
            "Wing Commander",
            "Wing Executive",
            "Wing Coordinator",
            "Group Captain",
            "Squadron Commander",
            "Squadron Executive",
            "Flight Commander",
            "Flight Executive",
            "Pilot",
        ]
    elif branch == "Fleet Command":
        rlist = [
            "Fleet Commanding Officer",
            "Fleet Executive Officer",
            "Head of Disciplinary",
            "Disciplinary Officer",
        ]
    return rlist


async def get_branch_colour(branch=None, rank=None) -> discord.Colour:
    if branch == "Army":
        return ARMY_COLOUR
    elif branch == "Starfighter Corps":
        return SFC_COLOUR
    elif branch == "Naval Auxiliary":
        return AUX_COLOUR
    elif branch == "Special Operations Force":
        if rank[0] == "A":
            return ARC_COLOUR
        else:
            return RC_COLOUR
    elif rank in ["MCDR", "SCDR", "MCPO", "CPO"] or branch == "Fleet Command":
        return FLEET_COLOUR
    else:
        return discord.Colour.from_rgb(61, 67, 69)


def position_sort(element):
    positions = ['CCO', 'CXO', 'CNCO', 'PCO', 'PXO', 'PNCO', 'SL', 'SNCO', 'FTL']
    return positions.index(element)

def rank_sort(element):
    ranks = ['MCDR', 'SCDR', 'COM', 'BCDR', 'CDR', 'GEN', 'AirCPT', 'RCMAJ', 'MAJ', 'ACPT', 'MCPO', 'CPT', 'WCDR', 'RCCPT', 'NCDR', 'LT', 'GCPT', 'RCLT', 'ARCLT', 'LTCDR', '2LT', 'RC2LT', 'NLT', 'CPO', 'SGM', 'SL', 'RCSGM', 'ASGT', 'RCSGT', 'RCCPL', 'RCPVT', 'ARC', 'RC', 'PO1', 'SGT', 'FCPT', 'PO2', 'CPL', 'FLT', 'PO3', 'LCPL', 'FO', 'PO', 'CT']
    return ranks.index(element)

def is_allowed(ctx):
    allowed_users = [618502892449693727, 434076591052685322]  # Example list of allowed user IDs
    is_admin = ctx.author.permissions.administrator
    is_allowed = ctx.author.id in allowed_users
    return is_admin or is_allowed

class Data(commands.Cog):
    def __init__(self, bot: DatacoreBot):
        self.bot = bot

    data = discord.SlashCommandGroup(
        name="data", description="Data commands", guild_only=True
    )

    @data.command(name="add", description="Add data to the database")
    @option(
        "branch",
        description="Branch the member belongs to",
        choices=[
            "Fleet Command",
            "Army",
            "Starfighter Corps",
            "Naval Auxiliary",
            "Special Operations Force",
        ],
        required=True,
    )
    @option(
        "company",
        description="Company the member belongs to",
        autocomplete=company_autocomplete,
        default=None,
    )
    @option(
        "platoon",
        description="Platoon the member belongs to",
        autocomplete=platoon_autocomplete,
        default=None,
    )
    @option(
        "position",
        description="Position the member holds",
        autocomplete=position_autocomplete,
        default=None,
    )
    async def _add(
        self,
        ctx: discord.ApplicationContext,
        member: discord.Member,
        branch: str,
        company: str,
        platoon: str,
        position: str,
    ):
        db, cursor = await connect_to_db()
        # pattern = r"^([A-Z0-9]{2,4}) ([A-Z][a-z]+) ([A-Z]{1,2}-(?:[0-9]+|(?:\d-\d+\/\d+)))$"
        await cursor.execute(f"SELECT ID FROM members WHERE ID = {member.id}")
        if await cursor.fetchone() is None:
            if re.match(FULL, member.display_name):
                CT = member.display_name.split(sep=" ")
                name: str = CT[1]
                designation: str = CT[2]
                rank: str = CT[0]
                if branch == "Starfighter Corps":
                    branch = "SFC"
                elif branch == "Naval Auxiliary":
                    branch = "AUX"
                elif branch == "Special Operations Force":
                    branch = "SOF"
                company = await company_name_switcher(company)
                try:
                    await cursor.execute(
                        f"INSERT INTO Members (ID, Rank, Name, Designation, Branch, Company, Platoon, Position) VALUES ({member.id}, '{rank}', '{name}', '{designation}', '{branch}','{company}', '{platoon}', '{position}')"
                    )
                    await cursor.execute(
                        f"INSERT INTO attendance (ID, attendanceNum) VALUES ({member.id}, 0)"
                    )
                except:
                    await ctx.respond(
                        f"Error adding {member.name} to the database", ephemeral=True
                    )
                await db.commit()
                await cursor.close()
                await db.close()
                await ctx.respond(
                    f"Added {member.name} to the database", ephemeral=True
                )
            else:
                await ctx.respond(
                    f"{member.name} does not have a valid CT name", ephemeral=True
                )
        else:
            await ctx.respond(
                f"{member.name} already exists in the database", ephemeral=True
            )

    @data.command()
    @option(
        "branch",
        description="Branch the member belongs to",
        choices=[
            "Army",
            "Starfighter Corps",
            "Naval Auxiliary",
            "Special Operations Force",
            "Fleet Command",
            "None",
        ],
    )
    @option(
        "company",
        description="Company the member belongs to",
        autocomplete=company_autocomplete,
        default=None,
    )
    @option(
        "platoon",
        description="Platoon the member belongs to",
        autocomplete=platoon_autocomplete,
        default=None,
    )
    @option(
        "position",
        description="Position the member holds",
        autocomplete=position_autocomplete,
        default=None,
    )
    async def edit(
        self,
        ctx: discord.ApplicationContext,
        member: discord.Member,
        branch: str,
        company: str,
        platoon: str,
        position: str,
    ):
        db, cursor = await connect_to_db()
        query = "UPDATE Members SET "
        if branch is not None:
            if branch == "None":
                branch = None
            query += f"Branch = '{branch}',"
        if company is not None:
            if company == "None":
                company = None
            query += f"Company = '{company}',"
        if platoon is not None:
            if platoon == "None":
                platoon = None
            query += f"Company = '{platoon}',"
        if position is not None:
            if position == "None":
                position = None
            query += f"Position = '{position}',"

        query = query.rstrip(",") + f" WHERE ID = {member.id}"

        await cursor.execute(query)
        await db.commit()
        await close_db(db, cursor)
        await ctx.respond(f"Updated {member.name}'s data", ephemeral=True)

    @data.command(name="get", description="Get member from the database")
    async def _get(self, ctx: discord.ApplicationContext, member: discord.Member):
        db, cursor = await connect_to_db()
        await cursor.execute(
            f"SELECT Members.Rank, Members.name, Members.Designation, Members.Branch, Members.Company, Members.Platoon, Members.Position, attendance.AttendanceNum FROM Members JOIN attendance ON Members.ID = attendance.ID WHERE Members.ID = {member.id}"
        )

        rnd = await cursor.fetchone()
        await cursor.execute(
            f"SELECT art_team, admin, event, vanguard_security, KSF FROM cshop WHERE ID = {member.id}"
        )
        cshop = await cursor.fetchone()
        await cursor.execute(
            f"SELECT rifleman, antiarmour, marksman, arf, aerial, SOF FROM quals WHERE ID = {member.id}"
        )
        kmc = await cursor.fetchone()
        await cursor.close()
        await db.close()
        display_name = f"{rnd[0]} {rnd[1]} {rnd[2]}"
        colour = await get_branch_colour(rnd[3], rnd[0])
        comp_name = await company_name_switcher(rnd[4])
        rnd_embed = discord.Embed(
            title=f"{display_name} Info",
            color=colour,
            description=f"**RANK**: {rank_switcher(rnd[0])}\n**DESIGNATION**: {rnd[2]}",
        )
        if rnd[3] is not None:
            rnd_embed.add_field(name="Branch", value=rnd[3], inline=False)
        else:
            rnd_embed.add_field(name="Branch", value="None", inline=False)
        if rnd[4] is not None:
            rnd_embed.add_field(name="Company", value=comp_name, inline=False)
        if rnd[5] is not None:
            rnd_embed.add_field(name="Platoon", value=rnd[5], inline=False)
        if rnd[6] is not None:
            rnd_embed.add_field(name="Position", value=rnd[6], inline=False)

        if rnd[7] is not None:
            rnd_embed.add_field(name="Attendance", value=rnd[7], inline=False)
        rnd_embed.set_thumbnail(url=member.avatar.url)

        cshop_embed = discord.Embed(title=f"{display_name} C-Shop Info", color=colour)
        if cshop is None:
            cshop_embed.add_field(name="C-Shop", value="No C-Shop roles", inline=False)
        else:
            if cshop[0] is not None:
                cshop_embed.add_field(name="Art Team", value=cshop[0], inline=False)
            if cshop[1] is not None:
                cshop_embed.add_field(
                    name="Administration", value=cshop[1], inline=False
                )
            if cshop[2] is not None:
                cshop_embed.add_field(name="Event", value=cshop[2], inline=False)
            if cshop[3] is not None:
                cshop_embed.add_field(
                    name="Vanguard Security Team", value=cshop[3], inline=False
                )
            if cshop[4] is not None:
                cshop_embed.add_field(
                    name="Kaminoan Security Force", value=cshop[4], inline=False
                )

        kmc_embed = discord.Embed(title=f"{display_name} KMC Info", color=colour)
        if kmc is None:
            kmc_embed.add_field(name="KMC", value="No KMC roles", inline=False)
        else:
            if kmc[0] is not None:
                kmc_embed.add_field(name="Rifleman", value=kmc[0], inline=False)
            if kmc[1] is not None:
                kmc_embed.add_field(name="Anti-Armour", value=kmc[1], inline=False)
            if kmc[2] is not None:
                kmc_embed.add_field(name="Marksman", value=kmc[2], inline=False)
            if kmc[3] is not None:
                kmc_embed.add_field(name="ARF", value=kmc[3], inline=False)
            if kmc[4] is not None:
                kmc_embed.add_field(name="Aerial", value=kmc[4], inline=False)
            if kmc[5] is not None:
                kmc_embed.add_field(
                    name="Special Operations Division", value=kmc[5], inline=False
                )

        page_groups = []
        rnd_page = PageGroup(
            pages=[rnd_embed], label="Main Info Page", use_default_buttons=False
        )
        cshop_page = PageGroup(
            pages=[cshop_embed], label="C-Shop Info Page", use_default_buttons=False
        )
        kmc_page = PageGroup(
            pages=[kmc_embed], label="KMC Info Page", use_default_buttons=False
        )
        page_groups.append(rnd_page)
        page_groups.append(cshop_page)
        page_groups.append(kmc_page)

        paginator = Paginator(
            pages=page_groups,
            use_default_buttons=False,
            show_indicator=False,
            show_menu=True,
            show_disabled=False,
            timeout=300,
            menu_placeholder="Select a Request",
        )
        await paginator.respond(ctx.interaction)

    @data.command(
        name="name_check",
        description="Check if a member has a valid CT name and numbers and is available",
    )
    async def _name_check(self, ctx: discord.ApplicationContext, name: str):
        # pattern = r"^([A-Z0-9]{2,4}) ([A-Z][a-z]+) ([A-Z]{1,2}-(?:[0-9]+|(?:\d-\d+\/\d+)))$"
        reserved = r"(?:CT-[0-6][0-9]{3}$)"
        match = re.match(FULL, name)
        Name = match.group(2)
        desg = match.group(3)
        if match is not None:
            if re.match(reserved, desg) is not None:
                await ctx.respond(
                    f"{name} is reserved and cannot be reused", ephemeral=True
                )
            else:
                db, cursor = await connect_to_db()
                await cursor.execute(
                    f"SELECT ID, Rank, Name, Designation FROM members WHERE Name = '{Name}'"
                )
                result = await cursor.fetchone()
                if result is None:
                    await ctx.respond(f"{name} is available", ephemeral=True)
                else:
                    owner = await self.bot.get_or_fetch_user(result[0])
                    await ctx.respond(
                        f"{name} is not available\nCurrently held by: {result[1] + ' ' + result[2] + ' ' + result[3]} | {owner.mention}",
                        ephemeral=True,
                    )
        else:
            await ctx.respond(f"{name} is not a valid CT name", ephemeral=True)

    @data.command(name="remove", description="Remove a member from the database")
    async def _remove(self, ctx: discord.ApplicationContext, member: discord.Member):
        db, cursor = await connect_to_db()
        await cursor.execute(f"SELECT ID FROM members WHERE ID = {member.id}")
        result = await cursor.fetchone()
        if result is not None:
            await cursor.execute(f"DELETE FROM Members WHERE ID = {member.id}")
            await cursor.execute(f"DELETE FROM attendance WHERE ID = {member.id}")
            await db.commit()
            await cursor.close()
            await db.close()
            await ctx.respond(
                f"Removed {member.name} from the database", ephemeral=True
            )
        else:
            await ctx.respond(
                f"{member.name} does not exist in the database", ephemeral=True
            )

    @data.command(name="platoon", description="Get info on a platoon")
    @option(
        "branch",
        description="Branch the member belongs to",
        choices=[
            "Army",
            "Starfighter Corps",
            "Naval Auxiliary",
            "Special Operations Force",
            "Fleet Command",
            "None",
        ],
    )
    @option(
        "company",
        description="Company the member belongs to",
        autocomplete=company_autocomplete,
        required=True,
    )
    @option(
        "platoon",
        description="Platoon the member belongs to",
        autocomplete=platoon_autocomplete,
        required=True,
    )
    async def _get_platoon(
        self, ctx: discord.ApplicationContext, branch: str, company: str, platoon: str
    ):
        company = await company_name_switcher(company)
        db, cursor = await connect_to_db()
        await cursor.execute(
            f"SELECT Members.Rank, Members.Name, Members.Designation, Members.Position FROM Members WHERE Platoon = '{platoon}' AND Company = '{company}'"
        )
        r = await cursor.fetchall()
        print(r)
        r = sorted(r,key=position_sort(r[i][3]))
        pass

    @data.command()
    async def check_bans(self, ctx: discord.ApplicationContext, member: discord.Member = None, id=None):
        with open('bans.json') as f:
            data = json.load(f)

        if id is not None:
            # Check if id is a valid integer
            try:
                id = int(id)
            except ValueError:
                await ctx.respond("Please provide a valid integer user ID.", ephemeral=True)
                return

        if member is None:
            if id is None:
                await ctx.respond("Please provide a member or a user ID to check.", ephemeral=True)
                return
            try:
                member = await self.bot.fetch_user(id)
            except discord.NotFound:
                await ctx.respond("User not found.", ephemeral=True)
                return

        for user_data in data:
            if str(user_data['user_id']) == str(id):
                await ctx.respond(f"{member.display_name} has been banned previously.", ephemeral=True)
                return

        await ctx.respond("No ban history for that member.", ephemeral=True)

    @check_bans.error
    async def check_bans_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.respond("Missing permissions", ephemeral=True)




def setup(bot):
    bot.add_cog(Data(bot))
