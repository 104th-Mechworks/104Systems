import datetime

import aiosqlite
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())


async def connect_to_db():
    db = await aiosqlite.connect("main.sqlite")
    cursor = await db.cursor()
    return db, cursor


async def fetch_or_get_role(guild: discord.Guild, role_id: int):
    role = guild.get_role(role_id)
    if role is None:
        role = await guild._fetch_role(role_id)
    return role


class MainButtons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="NFFC", style=discord.ButtonStyle.grey)
    async def nffc(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_modal(
            modal=MedbayModal(title="Submission Confirmation")
        )

    @discord.ui.button(label="LOA", style=discord.ButtonStyle.grey)
    async def loa(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_modal(
            modal=MedbayModal(ttype="LOA", title="Submission Confirmation")
        )


class MedbayModal(discord.ui.Modal):
    def __init__(self, ttype, title="Submission Confirmation"):
        super().__init__(
            discord.ui.InputText(
                label="Start Date",
                style=discord.InputTextStyle.singleline,
                placeholder="dd/mm/yyyy",
                required=True,
            ),
            discord.ui.InputText(
                label="End Date",
                style=discord.InputTextStyle.singleline,
                placeholder="dd/mm/yyyy",
                required=True,
            ),
            discord.ui.InputText(
                label="Reason",
                style=discord.InputTextStyle.long,
                placeholder="Reason for NFFC",
                required=True,
            ),
            title=title,
        )
        self.type = ttype

    async def callback(self, interaction: discord.Interaction):
        db, cursor = await connect_to_db()
        await cursor.execute(
            f"SELECT Active FROM medbay WHERE user_id = {interaction.user.id} AND Active = 1"
        )
        active = await cursor.fetchone()
        if active is not None:
            await interaction.response.send_message(
                "You already have an active medbay request", ephemeral=True
            )
            return

        self.values = [
            self.children[0].value,
            self.children[1].value,
            self.children[2].value,
        ]
        await cursor.execute(
            "SELECT NFFCcat, LOAcat FROM ServerConfig WHERE ID = ?",
            (interaction.guild.id,),
        )
        categories = await cursor.fetchone()
        await cursor.execute(
            f"SELECT SNCO, SL, PNCO, PXO, PCO FROM ServerConfig WHERE ID = {interaction.guild.id}"
        )
        roles = await cursor.fetchone()
        roles = list(roles)
        SNCO = await fetch_or_get_role(interaction.guild, roles[0])
        SL = await fetch_or_get_role(interaction.guild, roles[1])
        PNCO = await fetch_or_get_role(interaction.guild, roles[2])
        PXO = await fetch_or_get_role(interaction.guild, roles[3])
        PCO = await fetch_or_get_role(interaction.guild, roles[4])

        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(
                read_messages=False
            ),
            interaction.user: discord.PermissionOverwrite(
                view_channel=True, send_messages=True, read_messages=True
            ),
            SL: discord.PermissionOverwrite(
                view_channel=True, send_messages=True, read_messages=True
            ),
            SNCO: discord.PermissionOverwrite(
                view_channel=True, send_messages=True, read_messages=True
            ),
            PCO: discord.PermissionOverwrite(
                view_channel=True, send_messages=True, read_messages=True
            ),
            PXO: discord.PermissionOverwrite(
                view_channel=True, send_messages=True, read_messages=True
            ),
            PNCO: discord.PermissionOverwrite(
                view_channel=True, send_messages=True, read_messages=True
            )
        }

        embed = discord.Embed(
            title=f"**{interaction.user.display_name} NFFC Request**",
            description=f"""
            **Start Date:** {self.values[0]}
            **End Date:** {self.values[1]}
            **Reason:** {self.values[2]}
            """,
            color=discord.Colour.from_rgb(206, 206, 206),
        )
        embed.timestamp = datetime.datetime.utcnow()
        if self.type == "NFFC":
            category = interaction.guild.get_channel(categories[0])
        elif self.type == "LOA":
            category = interaction.guild.get_channel(categories[1])
        channel: discord.TextChannel = await interaction.guild.create_text_channel(
            f"{interaction.user.name}-NFFC",
            category=category,
            overwrites=overwrites,
        )
        await cursor.execute(
            "INSERT INTO medbay (user_id, start_date, end_date, reason, Active, channel_id) VALUES (?, ?, ?, ?, 1, ?)",
            (
                interaction.user.id,
                self.values[0],
                self.values[1],
                self.values[2],
                channel.id,
            ),
        )
        await db.commit()
        await db.close()
        await channel.send(
            embed=embed,
            view=SubmitButtons(),
        )
        await interaction.response.send_message(f"ticket can be found here: {channel.mention}")


class SubmitButtons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Submit", style=discord.ButtonStyle.green)
    async def submit(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message("Submitted", ephemeral=True)
        await interaction.channel.send(
            embed=discord.Embed(title="`Staff ticket controls`"),
            view=AcceptDenyButtons(),
        )

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.red)
    async def cancel(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message("Cancelling...", ephemeral=True)
        await interaction.channel.delete()


class AcceptDenyButtons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Accept", style=discord.ButtonStyle.green)
    async def accept(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.message.delete()
        await interaction.channel.send(
            embed=discord.Embed(title="`Accepted`"), view=CloseButtons()
        )
        db, cursor = await connect_to_db()
        await cursor.execute(f"UPDATE medbay SET Active=1 WHERE channel_id={interaction.channel.id}")
        await db.commit()
        await cursor.close()
        await db.close()


class CloseButtons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Close", style=discord.ButtonStyle.red)
    async def close(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.message.delete()
        await interaction.channel.delete()

    @discord.ui.button(label="Start", style=discord.ButtonStyle.green)
    async def start(self, button: discord.ui.Button, interaction: discord.Interaction):
        button.disabled = True
        button.label = "Started"
        button.style = discord.ButtonStyle.grey
        await interaction.message.edit(view=self)


class ForceModal(discord.ui.Modal):
    def __init__(self, ttype, target: discord.Member, title):
        super().__init__(
            discord.ui.InputText(
                label="Start Date",
                style=discord.InputTextStyle.singleline,
                placeholder="dd/mm/yyyy",
                required=True,
            ),
            discord.ui.InputText(
                label="End Date",
                style=discord.InputTextStyle.singleline,
                placeholder="dd/mm/yyyy",
                required=True,
            ),
            discord.ui.InputText(
                label="Reason",
                style=discord.InputTextStyle.long,
                placeholder="Reason",
                required=True,
            ),
            title=title,
        )
        self.target = target
        self.type = ttype

    async def callback(self, interaction: discord.Interaction):
        db, cursor = await connect_to_db()
        await cursor.execute(
            f"SELECT Active FROM medbay WHERE user_id = {interaction.user.id} AND Active = 1"
        )
        active = await cursor.fetchone()
        if active is not None:
            await interaction.response.send_message(
                f"{self.target.display_name} already has an active medbay request", ephemeral=True
            )
            return

        self.values = [
            self.children[0].value,
            self.children[1].value,
            self.children[2].value,
        ]
        await cursor.execute(
            "SELECT NFFCcat, LOAcat FROM ServerConfig WHERE ID = ?",
            (interaction.guild.id,),
        )
        categories = await cursor.fetchone()
        await cursor.execute(
            f"SELECT SNCO, SL, PNCO, PXO, PCO FROM ServerConfig WHERE ID = {interaction.guild.id}"
        )
        roles = await cursor.fetchone()
        roles = list(roles)
        SNCO = await fetch_or_get_role(interaction.guild, roles[0])
        SL = await fetch_or_get_role(interaction.guild, roles[1])
        PNCO = await fetch_or_get_role(interaction.guild, roles[2])
        PXO = await fetch_or_get_role(interaction.guild, roles[3])
        PCO = await fetch_or_get_role(interaction.guild, roles[4])

        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(
                read_messages=False
            ),
            interaction.user: discord.PermissionOverwrite(
                view_channel=True, send_messages=True, read_messages=True
            ),
            SL: discord.PermissionOverwrite(
                view_channel=True, send_messages=True, read_messages=True
            ),
            SNCO: discord.PermissionOverwrite(
                view_channel=True, send_messages=True, read_messages=True
            ),
            PCO: discord.PermissionOverwrite(
                view_channel=True, send_messages=True, read_messages=True
            ),
            PXO: discord.PermissionOverwrite(
                view_channel=True, send_messages=True, read_messages=True
            ),
            PNCO: discord.PermissionOverwrite(
                view_channel=True, send_messages=True, read_messages=True
            )
        }

        embed = discord.Embed(
            title=f"**{self.target.display_name} {self.type} Forced**",
            description=f"""
                    **Start Date:** {self.values[0]}
                    **End Date:** {self.values[1]}
                    **Reason:** {self.values[2]}
                    """,
            color=discord.Colour.from_rgb(206, 206, 206),
        ).set_footer(text=f"User: {interaction.user.display_name}")

        embed.timestamp = datetime.datetime.utcnow()

        if self.type == "NFFC":
            tcategory: discord.CategoryChannel = interaction.guild.get_channel(categories[0])
        elif self.type == "LOA":
            tcategory: discord.CategoryChannel = interaction.guild.get_channel(categories[1])

        channel: discord.TextChannel = await interaction.guild.create_text_channel(
            f"{interaction.user.name}-NFFC",
            category=tcategory,
            overwrites=overwrites,
        )
        await cursor.execute(
            "INSERT INTO medbay (user_id, start_date, end_date, reason, Active, channel_id) VALUES (?, ?, ?, ?, 1, ?)",
            (
                interaction.user.id,
                self.values[0],
                self.values[1],
                self.values[2],
                channel.id,
            ),
        )
        await db.commit()
        await db.close()
        await channel.send(
            embed=embed,
            view=Close()
        )
        await interaction.response.send_message(f"ticket made and authorised: {channel.mention}", ephemeral=True)


class Close(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Close", style=discord.ButtonStyle.red)
    async def close(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.message.delete()
        await interaction.channel.delete()
        db, cursor = await connect_to_db()
        await cursor.execute(f"UPDATE medbay SET Active=0 WHERE channel_id={interaction.channel.id}")
        await db.commit()
        await cursor.close()
        await db.close()


class Medbay(commands.Cog):
    def __init__(self, bot) -> None:
        super().__init__()
        self.bot = bot

    medbay = discord.SlashCommandGroup(
        name="medbay", description="Commands for the medbay"
    )

    @medbay.command(name="return", description="Returns a user from the medbay")
    @discord.option(
        name="member",
        description="The member to return from the medbay",
        input_type=discord.Member,
        required=False,
    )
    async def _return(self, ctx: commands.Context, member: discord.Member):
        if member is None:
            member = ctx.author

        db, cursor = await connect_to_db()
        await cursor.execute(
            "SELECT * FROM medbay WHERE user_id = ? AND Active = ?", (member.id, 1)
        )
        user_data = await cursor.fetchone()
        if user_data is None:
            await ctx.channel.send("This user does not have an active medbay request")
            return
        await cursor.execute(
            f"UPDATE medbay SET Active = {0} WHERE user_id = {member.id}",
        )
        await db.commit()
        await db.close()
        await ctx.reply(
            f"{member.mention} has been returned from the medbay", ephemeral=True
        )

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

    @discord.slash_command()
    async def setup(
            self,
            ctx: discord.ApplicationContext,
            snco: discord.Role,
            sl: discord.Role,
            pnco: discord.Role,
            pxo: discord.Role,
            pco: discord.Role,
            nffcr: discord.Role,
            nffcc: discord.CategoryChannel,
            loar: discord.Role,
            loac: discord.CategoryChannel
    ):
        db = await aiosqlite.connect("main.sqlite")
        cursor = await db.cursor()
        await cursor.execute(f"SELECT ID FROM ServerConfig WHERE ID = {ctx.guild.id}")
        r = await cursor.fetchone()
        if r is None:
            await cursor.execute(
                f"INSERT INTO ServerConfig (ID, NFFCcat, LOAcat, NFFCr, LOAr, SNCO, SL, PNCO, PXO, PCO) VALUES (?, ?, ?, ?, ?, ?, ? ,?, ?, ?)",
                (
                    ctx.guild.id,
                    nffcc.id,
                    loac.id,
                    nffcr.id,
                    loar.id,
                    snco.id,
                    sl.id,
                    pnco.id,
                    pxo.id,
                    pco.id
                )

            )
        else:
            await cursor.execute(
                f"UPDATE ServerConfig SET (NFFCcat = {nffcc.id}, NFFCr = {nffcr.id}, LOAcat = {loac.id}, LOAr = {loar.id}, SNCO = {snco.id}, SL = {sl.id}, PNCO = {pnco.id}, PXO = {pxo.id}, PCO = {pco.id}) WHERE ID = {ctx.guild.id}")
        await ctx.respond(f"Medbay set up")
        await db.commit()
        await cursor.close()
        await db.close()

    @medbay.command()
    async def force(self, ctx: discord.ApplicationContext, member: discord.Member,
                    type=discord.Option(choices=["LOA", "NFFC"])):
        await ctx.response.send_modal(
            modal=ForceModal(ttype=type, target=member, title=f"Forced Leave Form {member.display_name}"))

    @medbay.command(name="return", description="Returns an nffc or loa")
    async def _return(self, ctx: discord.ApplicationContext, member: discord.Member | None = None):
        if member is None:
            member = ctx.author
        db, cursor = await connect_to_db()
        await cursor.execute(
            f"SELECT * FROM medbay WHERE user_id = {member.id} AND Active = 1"
        )
        user_data = await cursor.fetchone()
        if user_data is None:
            await ctx.respond("This user does not have an active medbay request")
            return
        await cursor.execute(
            f"UPDATE medbay SET Active = 0 WHERE user_id = {member.id} AND Active = 1"
        )
        await db.commit()
        await cursor.close()
        await db.close()
        await ctx.respond("User returned from medbay")

    @medbay.command(name="report", description="Lists all active medbay requests")
    @discord.option(name="date", description="fetch all entries after this date", required=True)
    async def report(
        self,
        ctx: discord.ApplicationContext,
        date: discord.Option(
            input_type=str,
            name="date",
            description="fetch entries after this date: dd-mm-yyyy",
            required=True),
        member: discord.Option(
            input_type=discord.Member,
            name="Member",
            description="specify a specific member",
            required=False
            )
    ):

        if member is None:
            member.id = "*"
        date = date_check(date)
        if date = "Invalid date Format":
            await ctx.respond("Not a valid date")
        db, cursor = await connect_to_db()
        await cursor.execute(f"SELECT * FROM medbay WHERE start_date >= date")




def date_check(input_date):
    # Define the input date formats to check
    date_formats = ["%d/%m/%y", "%d.%m.%Y", "%m/%d/%y"]

    # Initialize a variable to store the parsed date
    parsed_date = None

    # Try parsing the input date with each format
    for date_format in date_formats:
        try:
            parsed_date = datetime.strptime(input_date, date_format)
            break  # Exit the loop if parsing succeeds
        except ValueError:
            pass  # Continue to the next format if parsing fails

    # Check if a valid date was parsed
    if parsed_date:
        return parsed_date.strftime("%d-%m-%Y")
    else:
        return "Invalid date format"



def setup(bot: commands.Bot):
    bot.add_cog(Medbay(bot))
