import datetime
import os
from typing import Literal, Optional
from Bot.DatacoreBot import DatacoreBot
import discord
from dateutil.relativedelta import relativedelta
from discord.ext import pages, commands, tasks
from discord.ext.pages import PaginatorButton
from discord import option
from Bot.utils.DB import connect_to_db, close_db


# bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())


async def fetch_or_get_role(guild: discord.Guild, role_id: int):
    role = guild.get_role(role_id)
    if role is None:
        try:
            role = await guild._fetch_role(role_id)
        except discord.HTTPException:
            return None
    return role


def date_check(input_date: str, mode: Optional[Literal["s", "e"]] = None):
    try:
        search_date = datetime.datetime.strptime(input_date, "%d-%m-%Y")
    except ValueError:
        return "Invalid date"
    else:
        if mode == "s":
            if search_date > datetime.datetime.today():
                return "Invalid date"
        elif mode == "e":
            if search_date > datetime.datetime.now() + relativedelta(months=3):
                return "Invalid date"
        return search_date


class MainButtons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="NFFC", style=discord.ButtonStyle.grey, custom_id="main_nffc"
    )
    async def nffc_callback(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        await interaction.response.send_modal(
            modal=MedbayRequestModal(title="NFFC Request", request_type="NFFC")
        )

    @discord.ui.button(
        label="LOA", style=discord.ButtonStyle.grey, custom_id="main_loa"
    )
    async def loa_callback(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        await interaction.response.send_modal(
            modal=MedbayRequestModal(title="LOA Request", request_type="LOA")
        )


class MedbayRequestModal(discord.ui.Modal):
    def __init__(self, request_type, title):
        super().__init__(
            discord.ui.InputText(
                label="Start Date",
                style=discord.InputTextStyle.singleline,
                placeholder="dd-mm-yyyy",
                required=True,
            ),
            discord.ui.InputText(
                label="End Date",
                style=discord.InputTextStyle.singleline,
                placeholder="dd-mm-yyyy",
                required=True,
            ),
            discord.ui.InputText(
                label="Reason",
                style=discord.InputTextStyle.long,
                placeholder=f"reason for {request_type}",
            ),
            title=title,
        )
        self.type = request_type

    async def callback(self, interaction: discord.Interaction):
        db, cursor = await connect_to_db()
        await cursor.execute(f"SELECT Status FROM medbay WHERE UserID = {interaction.user.id} AND status = {1}")
        active = await cursor.fetchone()
        if active is not None:
            await interaction.response.send_message("You already have an active medbay request", ephemeral=True)
            return

        values = [self.children[0].value, self.children[1].value, self.children[2].value]

        if date_check(values[0]) == "Invalid date":
            await interaction.response.send_message(
                "Invalid start date\nmake sure its day then month then year. (e.g 01-09-2023)", ephemeral=True)
            return
        elif date_check(values[1]) == "Invalid date":
            await interaction.response.send_message(
                "Invalid end date\nmake sure its day then month then year. (e.g 01-09-2023)", ephemeral=True)
            return

        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False, view_channel=False),
            interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_messages=True)}

        await cursor.execute(f"SELECT LOAcat, NFFCcat, authIDs FROM ServerConfig WHERE ID = {interaction.guild.id}")
        ticket_setup = await cursor.fetchone()
        auth_ids = [int(i) for i in ticket_setup[2].strip('[]').split(',')]

        for i in auth_ids:
            role = await fetch_or_get_role(interaction.guild, i)
            overwrites[role] = discord.PermissionOverwrite(read_messages=True, send_messages=True,
                                                           read_message_history=True)

        embed = discord.Embed(title=f"**{interaction.user.display_name} {self.type} Request**", description=f"""
                    **Start Date:** {values[0]}
                    **End Date:** {values[1]}
                    **Reason:** {values[2]}
                    """, color=discord.Colour.from_rgb(206, 206, 206), )
        embed.timestamp = datetime.datetime.utcnow()
        category = None
        if self.type == "NFFC":
            category: discord.CategoryChannel = interaction.guild.get_channel(ticket_setup[1])
            if category is None:
                category = await interaction.guild.fetch_channel(ticket_setup[1])
        elif self.type == "LOA":
            category = interaction.guild.get_channel(ticket_setup[0])
            if category is None:
                category = await interaction.guild.fetch_channel(ticket_setup[0])
        else:
            await interaction.response.send_message("Invalid type", ephemeral=True)
        channel: discord.TextChannel = await interaction.guild.create_text_channel(
            f"{interaction.user.name}-{self.type}", category=category, overwrites=overwrites)
        await cursor.execute(
            f"""INSERT INTO medbay (UserID, Type, startDate, endDate, Reason, Status, channelID, GuildID) VALUES ({interaction.user.id}, "{self.type}", "{values[0]}", "{values[1]}", "{values[2]}", {0}, {channel.id}, {interaction.guild.id})"""
        )
        await db.commit()
        await close_db(db, cursor)
        await channel.send(embed=embed, view=SubmitButtons(), )
        await interaction.response.send_message(f"ticket can be found here: {channel.mention}", ephemeral=True)


class SubmitButtons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Submit", style=discord.ButtonStyle.green, custom_id="submit"
    )
    async def submit(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.disable_all_items()
        button.label = "Submitted"
        button.style = discord.ButtonStyle.grey
        await interaction.message.edit(view=self)
        await interaction.response.send_message("Submitted", ephemeral=True)
        await interaction.channel.send(
            embed=discord.Embed(title="`Staff ticket controls`"),
            view=AcceptDenyButtons(requester=interaction.user),
        )

    @discord.ui.button(
        label="Cancel", style=discord.ButtonStyle.red, custom_id="cancel2"
    )
    async def cancel(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message("Cancelling...", ephemeral=True)
        db, cursor = await connect_to_db()
        await cursor.execute(
            f"DELETE FROM medbay WHERE channelID = {interaction.channel.id}"
        )
        await db.commit()
        await close_db(db, cursor)
        await interaction.channel.delete()


class AcceptDenyButtons(discord.ui.View):
    def __init__(self, requester: discord.Member):
        super().__init__(timeout=None)
        self.requester = requester

    @discord.ui.button(
        label="Approve", style=discord.ButtonStyle.green, custom_id="acpt"
    )
    async def accept(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.message.delete()
        await interaction.channel.send(
            embed=discord.Embed(title="Approved"), view=CloseButtons()
        )

    @discord.ui.button(label="Deny", style=discord.ButtonStyle.red, custom_id="deny")
    async def deny(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_modal(
            modal=DenyRequestModal(requester=self.requester)
        )


class DenyRequestModal(discord.ui.Modal):
    def __init__(self, requester: discord.Member, title="Request Deny Modal"):
        super().__init__(
            discord.ui.InputText(
                label="Reason",
                style=discord.InputTextStyle.long,
                placeholder="Reason...",
                required=True,
            ),
            title=title,
        )
        self.requester = requester

    async def callback(self, interaction: discord.Interaction):
        db, cursor = await connect_to_db()
        await cursor.execute(
            f"SELECT UserID, Type FROM medaby WHERE channelID = {interaction.channel.id}"
        )
        result = await cursor.fetchone()
        if self.requester is None:
            self.requester = await interaction.guild.fetch_member(result[0])
        embed = discord.Embed(
            title=f"{result[1]} Request Denied",
            description=f"{self.children[0].value}",
            colour=discord.Colour.from_rgb(138, 34, 26),
            timestamp=datetime.datetime.now(),
        )
        embed.set_author(name=f"{interaction.user.mention}")

        await self.requester.send(embed=embed)
        await cursor.execute(
            f"DELETE FROM medbay WHERE channelID = {interaction.channel.id}"
        )
        await db.commit()
        await cursor.close()
        await db.close()
        await interaction.response.send_message("Request denied.\nTicket closing...")
        await interaction.channel.delete()


class CloseButtons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Close", style=discord.ButtonStyle.red, custom_id="cls2")
    async def close(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.message.delete()
        await interaction.channel.delete()
        db, cursor = await connect_to_db()
        await cursor.execute(
            f"DELETE FROM medbay WHERE channelID={interaction.channel.id}"
        )

    @discord.ui.button(label="Start", style=discord.ButtonStyle.green, custom_id="strt")
    async def start(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.disable_all_items()
        button.label = "Started"
        button.style = discord.ButtonStyle.grey
        db, cursor = await connect_to_db()
        await cursor.execute(
            f"UPDATE medbay SET Status=1 WHERE channelID={interaction.channel.id}"
        )
        await db.commit()
        await cursor.execute(f"SELECT LOAr, NFFCr FROM ServerConfig WHERE ID = {interaction.guild.id}")
        roles = await cursor.fetchone()
        await cursor.close()
        await db.close()
        channel = interaction.channel
        category_name = channel.category.name
        if category_name == "LOA":
            LOA = await interaction.guild._fetch_role(roles[0])
            await interaction.user.add_roles(LOA, reason="Started LOA")
        elif category_name == "NFFC":
            NFFC = await interaction.guild._fetch_role(roles[1])
            await interaction.user.add_roles(NFFC, reason="Started LOA")

        await interaction.response.send_message(
            "your leave has now started", ephemeral=True
        )
        await interaction.message.edit(view=self)


def duration_calc(start: str, end: str) -> str:
    start_date = datetime.datetime.strptime(start, "%d-%m-%Y")
    end_date = datetime.datetime.strptime(end, "%d-%m-%Y")
    duration = end_date - start_date
    months = duration.days // 30
    weeks = (duration.days % 30) // 7
    days = (duration.days % 30) % 7
    durationstr = ", ".join(
        [
            f"{val} {unit}"
            for val, unit in zip([months, weeks, days], ["months", "weeks", "days"])
            if val != 0
        ]
    )
    return durationstr


def rank_sort(element):
    ranks = ['MCDR', 'SCDR', 'COM', 'BCDR', 'CDR', 'GEN', 'AirCPT', 'RCMAJ', 'MAJ', 'ACPT', 'MCPO', 'CPT', 'WCDR', 'RCCPT', 'NCDR', 'LT', 'GCPT', 'RCLT', 'ARCLT', 'LTCDR', '2LT', 'RC2LT', 'NLT', 'CPO', 'SGM', 'SL', 'RCSGM', 'ASGT', 'RCSGT', 'RCCPL', 'RCPVT', 'ARC', 'RC', 'PO1', 'SGT', 'FCPT', 'PO2', 'CPL', 'FLT', 'PO3', 'LCPL', 'FO', 'PO', 'CT']
    return ranks.index(element)

async def main_list_logic(platform: str):
    db, cursor = await connect_to_db()
    await cursor.execute(
        f"SELECT Members.Rank, Members.Name, Members.Designation, medbay.Type FROM members JOIN medbay ON Members.ID = medbay.userID WHERE medbay.Type IN ('LOA', 'NFFC') AND medbay.Status IN (1, 3) AND Members.ID = medbay.userID AND Members.Platform = '{platform}'")
    lst = await cursor.fetchall()
    lst = sorted(lst, key=lambda x: rank_sort(x[0]))
    embed = discord.Embed(
        title=f"{platform} Staff Medbay list",
        color=discord.Color.embed_background(),
        timestamp=datetime.datetime.utcnow()
    )
    lst = [tuple_ for tuple_ in lst if tuple_[0] not in ('CT', 'PO')]
    officer_ranks = {'MCDR', 'SCDR', 'COM', 'BCDR', 'CDR', 'GEN', 'AirCPT', 'RCMAJ', 'MAJ', 'ACPT', 'MCPO', 'CPT',
                     'WCDR', 'RCCPT', 'NCDR', 'LT', 'GCPT', 'RCLT', 'ARCLT', 'LTCDR', '2LT', 'RC2LT', 'NLT', 'CPO',
                     'SGM', 'SL', 'RCSGM', 'ASGT', 'RCSGT', 'RCCPL', 'RCPVT', 'ARC', 'RC', 'PO1'}

    # Initialize lists for officers and NCOs
    officers = []
    ncos = []
    officers_fmt = []
    ncos_fmt = []

    # Split the filtered list into officers and NCOs
    for e in lst:
        if e[0] in officer_ranks:
            officers.append(e)
        else:
            ncos.append(e)

    for o in officers:
        member = o[0] + " " + o[1] + " " + o[2]
        ltype = f"**{o[3]}**"
        officers_fmt.append(member + " : " + ltype)

    officers_fmt_str = "\n".join(officers_fmt)

    for n in ncos:
        member = n[0] + " " + n[1] + " " + n[2]
        ltype = f"**{n[3]}**"
        ncos_fmt.append(member + " : " + ltype)

    ncos_fmt_str = "\n".join(ncos_fmt)

    embed.add_field(name="Officers", value="None" if officers_fmt_str == "" else officers_fmt_str, inline=False)
    embed.add_field(name="NCOs", value="None" if ncos_fmt_str == "" else ncos_fmt_str, inline=False)
    return embed


class MainServerPlatformButtons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="PC", style=discord.ButtonStyle.red, custom_id="PC_ms1")
    async def pc_medbay_list(self, button: discord.Button, interaction: discord.Interaction):
        embed = await main_list_logic("PC")
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="Xbox", style=discord.ButtonStyle.green, custom_id="XBX_ms1")
    async def xbox_medbay_list(self, button: discord.Button, interaction: discord.Interaction):
        embed = await main_list_logic("Xbox")
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="PS", style=discord.ButtonStyle.blurple, custom_id="PS_ms1")
    async def ps_medbay_list(self, button: discord.Button, interaction: discord.Interaction):
        embed = await main_list_logic("PS")
        await interaction.response.send_message(embed=embed, ephemeral=True)


class Medbay(commands.Cog):
    def __init__(self, bot: DatacoreBot) -> None:
        super().__init__()
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(CloseButtons())
        self.bot.add_view(AcceptDenyButtons(requester=None))
        self.bot.add_view(SubmitButtons())
        self.bot.add_view(MainButtons())
        self.check_lates.start()
        self.bot.add_view(MainServerPlatformButtons())
    @tasks.loop(hours=24)
    async def check_lates(self):
        db, cursor = await connect_to_db()
        await cursor.execute(
            f"SELECT UserID, channelID, GuildID, endDate FROM medbay WHERE Status = {1}"
        )
        result = await cursor.fetchall()
        for item in result:
            user_id = item[0]
            channel_id = item[1]
            guild_id = item[2]
            end_date = datetime.datetime.strptime(item[3], "%d-%m-%Y")
            if end_date < datetime.datetime.today():
                channel: discord.TextChannel = self.bot.get_channel(channel_id)
                guild: discord.Guild = self.bot.get_guild(guild_id)
                user: discord.Member = guild.get_member(user_id)
                await cursor.execute(
                    f"UPDATE medbay SET Status = {3} WHERE UserID = {user_id} AND Status = {1}"
                )
                await db.commit()
                await channel.send(
                    f"{user.mention} your leave has ended.\n**You have 24 hours to return.**"
                )

    @commands.command()
    async def main_list(self, ctx: commands.Context):
        main_embed = discord.Embed(
            title="Staff Medbay List",
            description="List of all staff on LOA or NFFC across the MilSim",
            color=discord.Color.from_rgb(84, 91, 94)
        )
        view = MainServerPlatformButtons()
        await ctx.send(embed=main_embed, view=view)


    medbay = discord.SlashCommandGroup(
        name="medbay", description="Commands for the medbay", guild_only=True
    )

    async def get_channel(self, channel_id: int):
        channel = self.bot.get_channel(channel_id)
        if channel is None:
            channel = await self.bot.fetch_channel(channel_id)
            print("fetch")
            print(channel)
        if channel is not None:
            print("get")
            print(channel)
        return channel

    @medbay.command(name="return", description="Returns a user from the medbay")
    @discord.option(
        name="member",
        description="The member to return from the medbay",
        input_type=discord.Member,
        required=False,
    )
    async def _return(
        self, ctx: discord.ApplicationContext, member: discord.Member = None
    ):
        if member is None:
            member = ctx.author
        db, cursor = await connect_to_db()
        await cursor.execute(
            f"SELECT UserID, endDate, Status, channelID, Type FROM medbay WHERE UserID = {member.id} AND (Status = {1} OR Status = {3})"
        )
        result = await cursor.fetchone()
        if result is None:
            await ctx.respond(
                f"No active medbay ticket open for member: {member.display_name}"
            )
            await cursor.close()
            await db.close()
            return
        channel = self.bot.get_channel(result[3])
        if channel is None:
            channel = await self.bot.fetch_channel(result[3])
        if result[2] == 1:
            await cursor.execute(
                f"UPDATE medbay SET Status = {2} WHERE UserID = {member.id} AND Status = {1}"
            )
            await db.commit()
            await ctx.respond(f"Returned {member.display_name} from medbay")
        elif result[2] == 3:
            end_date = datetime.datetime.strptime(result[1], "%d-%m-%Y")
            days_late = (datetime.datetime.today() - end_date).days
            new_end_date = datetime.datetime.today().strftime("%d-%m-%Y")
            print(new_end_date)
            await cursor.execute(
                f"UPDATE medbay SET endDate = {new_end_date}, Status = {4} WHERE UserID = {member.id} AND Status = {3}"
            )
            await db.commit()
            await ctx.respond(
                f"Returned {member.display_name} from medbay. {days_late} days late"
            )

        ttype = result[4]
        await cursor.execute(f"SELECT LOAr, NFFCr FROM ServerConfig WHERE ID = {ctx.guild.id}")
        roles = await cursor.fetchone()
        await cursor.close()
        await db.close()
        if ttype == "LOA":
            LOA = await ctx.guild._fetch_role(roles[0])
            await member.remove_roles(LOA, reason="returned from LOA")
        elif ttype == "NFFC":
            NFFC = await ctx.guild._fetch_role(roles[1])
            await member.remove_roles(NFFC, reason="returned from LOA")
        await channel.delete()

    @commands.command()
    async def setup_medbay(self, ctx: commands.Context):
        embed = (
            discord.Embed(
                title="**Medbay**",
                description="""
            This is where you can request an NFFC or LOA.
            Below you can find the info for NFFCs and LOAs.
            """,
                color=discord.Colour.from_rgb(209, 209, 209),
            )
            .add_field(
                name="**NFFC**",
                value="You are not required to meet attendance requirements but are expected to be active on discord",
                inline=False,
            )
            .add_field(
                name="**LOA**",
                value="You are not required to meet attendance requirements and are not expected to be active on discord",
                inline=False,
            )
        )
        view = MainButtons()
        await ctx.channel.send(embed=embed, view=view)

    @commands.command()
    async def medbay_authroles(self, ctx: commands.Context, *roles: discord.Role):
        ids = []
        # for role in ctx.message.role_mentions:
        for role in roles:
            ids.append(role.id)
        db, cursor = await connect_to_db()
        await cursor.execute(
            "SELECT authIDs FROM ServerConfig WHERE ID = ?", (ctx.guild.id,)
        )
        result = await cursor.fetchone()
        if result is None:
            await cursor.execute(
                "INSERT INTO ServerConfig (ID, authIDs) VALUES (?, ?)",
                (ctx.guild.id, ids),
            )
        else:
            await cursor.execute(
                f"UPDATE ServerConfig SET authIDs = '{ids}' WHERE ID = {ctx.guild.id}"
            )
        await db.commit()
        await cursor.close()
        await db.close()
        await ctx.send("done")

    @commands.guild_only()
    @discord.slash_command(
        name="report", description="Lists all active medbay requests"
    )
    @discord.option(
        name="date", description="fetch all entries after this date", required=True
    )
    async def report(
        self,
        ctx: discord.ApplicationContext,
        date: str,
        member: discord.Member | None = None,
    ):
        await ctx.defer()
        Qdate = date_check(date)
        if date == "Invalid date Format":
            return await ctx.respond("Not a valid date")
        db, cursor = await connect_to_db()
        if member is None:
            resT = "p"
            await cursor.execute(
                f"SELECT userID, Type, startDate, endDate, Reason, Status, LateDate FROM medbay WHERE GuildiD = {ctx.guild.id}"
            )
        else:
            resT = "m"
            await cursor.execute(
                f"SELECT Type, startDate, endDate, Reason, Status, LateDate FROM medbay WHERE userID = {member.id}"
            )
        r = await cursor.fetchall()
        await cursor.close()
        await db.close()

        # remove tuples with start Date before date
        if resT == "m":
            r = [i for i in r if datetime.datetime.strptime(i[1], "%d-%m-%Y") > Qdate]
        elif resT == "p":
            r = [i for i in r if datetime.datetime.strptime(i[2], "%d-%m-%Y") > Qdate]

        if resT == "m":
            with open(f"{member.display_name}.txt", "w") as f:
                f.write(f"Medbay Report for: {member.display_name} \nafter: {date}\n\n")
                for entry in r:
                    mtype = entry[0]
                    start_date = entry[1]
                    end_date = entry[2]
                    reason = entry[3]
                    if entry[4] == 0:
                        status = "Pending"
                    elif entry[4] == 1:
                        status = "Active"
                    elif entry[4] == 2:
                        status = "Returned"
                    elif entry[4] == 3:
                        status = "Late"
                    f.write(
                        f"Type: {mtype}\nStart Date: {start_date}\nEnd Date: {end_date}\nReason: {reason}\nStatus: {status}\n\n"
                    )
                f.close()
            await ctx.respond(file=discord.File(f"{member.display_name}.txt"))
        elif resT == "p":
            grouped = {}
            for entry in r:
                if entry[0] not in grouped:
                    grouped[entry[0]] = []
                grouped[entry[0]].append(entry)
            with open(f"{ctx.guild.name}.txt", "w") as f:
                f.write(f"Report for {ctx.guild.name}, after: {date}")
                for key, value in grouped.items():
                    cmember: discord.Member = await self.bot.fetch_user(key)
                    f.write(f"Medbay Report for {cmember.display_name}\n\n")
                    for entry in value:
                        mtype = entry[1]
                        start_date = entry[2]
                        end_date = entry[3]
                        reason = entry[4]
                        if entry[5] == 0:
                            status = "Pending"
                        elif entry[5] == 1:
                            status = "Active"
                        elif entry[5] == 2:
                            status = "Returned"
                        elif entry[5] == 3:
                            status = "Late"
                        f.write(
                            f"Type: {mtype}\nStart Date: {start_date}\nEnd Date: {end_date}\nReason: {reason}\nStatus: {status}\n\n"
                        )
                f.close()
            await ctx.respond(file=discord.File(f"{f.name}"))
        os.remove(f"{f.name}")
        print("removed")

    @medbay.command()
    @option(
        input_type=discord.Member,
        name="member",
        description="select member to get medbay history",
    )
    async def history(self, ctx: discord.ApplicationContext, member: discord.Member):
        db, cursor = await connect_to_db()
        await cursor.execute(
            f"SELECT Type, startDate, endDate, Reason, Status FROM medbay WHERE userID = {member.id} AND (Status = {2} OR Status = {4}) ORDER BY TicketID DESC LIMIT 25"
        )
        result = await cursor.fetchall()
        print(result)
        await cursor.close()
        await db.close()
        if result is None:
            await ctx.respond(f"No medbay history for {member.display_name}")
            return
        else:
            embeds = []

            for item in result:
                lrs = "unknown"
                if item[4] == 2:
                    lrs = "Returned"
                elif item[4] == 4:
                    lrs = "Late Returned"

                embed = discord.Embed(title=f"Medbay History")
                embed.add_field(name="Type", value=item[0], inline=False)
                embed.add_field(name="Start Date", value=item[1], inline=False)
                embed.add_field(name="End Date", value=item[2], inline=False)
                embed.add_field(
                    name="Duration", value=duration_calc(item[1], item[2]), inline=False
                )
                embed.add_field(name="Reason", value=item[3], inline=False)
                embed.add_field(name="Status", value=lrs, inline=False)
                embeds.append(embed)

            page_groups = []
            for i in range(len(embeds)):
                page = pages.PageGroup(
                    pages=[embeds[i]],
                    label=f"Request: {i + 1}",
                    use_default_buttons=False,
                    show_indicator=False,
                    show_disabled=False,
                )
                page_groups.append(page)
            print(page_groups)
            try:
                paginator = pages.Paginator(
                    pages=page_groups,
                    use_default_buttons=False,
                    show_indicator=False,
                    show_disabled=False,
                    show_menu=True,
                    timeout=300,
                    menu_placeholder="Select a Request",
                )
                await paginator.respond(ctx.interaction)
            except ValueError:
                await ctx.respond("No history found")
            return

    @discord.slash_command()
    async def medbay_channel(self, ctx: discord.ApplicationContext, nffccategory: discord.CategoryChannel,
                             loacategory: discord.CategoryChannel, nffcrole: discord.Role, loarole: discord.Role):
        db, cursor = await connect_to_db()
        await cursor.execute(f"SELECT ID FROM ServerConfig WHERE ID = {ctx.guild_id}")
        result = await cursor.fetchone()
        if result is None:
            await cursor.execute(
                f"INSERT INTO ServerConfig (ID, NFFCcat, NFFCr, LOAcat, LOAr) VALUES ({ctx.guild_id}, {nffccategory.id}, {nffcrole.id}, {loacategory.id}, {loarole.id})")
        else:
            await cursor.execute(
                f"UPDATE ServerConfig SET NFFCcat = {nffccategory.id}, NFFCr = {nffcrole.id}, LOAcat = {loarole.id}, LOAr = {loarole.id} WHERE ID = {ctx.guild_id}")
        await db.commit()
        await cursor.close()
        await db.close()
        await ctx.respond(f"Updated {ctx.guild.name} medbay roles and categories", ephemeral=True)
        return


def setup(bot: DatacoreBot):
    bot.add_cog(Medbay(bot))
