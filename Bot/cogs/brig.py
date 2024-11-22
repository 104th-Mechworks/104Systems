import discord
from discord.ext import commands
import os
import fitz
from pylatex import Command, Document, Tabular, Package, PageStyle, Foot, Figure
from pylatex.utils import NoEscape, bold
from Bot.DatacoreBot import DatacoreBot



image_filename = os.path.join(os.path.dirname(__file__), "images", "RAS.png")

    # Document with `\maketitle` command activated


def dp_action_form(vcref_number: str, staff_member: str, member: discord.Member, action: str, reason: str):
    filepath = os.path.join(os.path.dirname(__file__), "VCL", f"{vcref_number}")
    doc = Document()
    doc.packages.append(Package('xcolor'))
    doc.packages.append(Package('graphicx'))
    doc.packages.append(Package('geometry', options=['a5paper', 'margin=0.5in', 'bottom=0.75in']))
    doc.change_document_style("empty")

    # create a table

    # with doc.create(MiniPage(align="c")):
    #     doc.append(LargeText(bold("Disciplinary Action Form")))

    doc.append(NoEscape(r"\begin{center}\Large{\textbf{Disciplinary Action Form}}\\[0.5cm]\end{center}"))
    with doc.create(Figure(position="h!")) as logo:
        logo.add_image(image_filename, width="100px")

    doc.append(Command('centering'))
    with doc.create(Tabular("|l|p{6cm}|", width=2, row_height=1.2)) as table:
        table.add_hline()
        table.add_row((bold("Date"), NoEscape(r"\today")))
        table.add_hline()
        table.add_row((bold("Case Ref Number"), vcref_number))
        table.add_hline()
        table.add_row((bold("Classification Level"), NoEscape(r"\textcolor{red}{None}")))
        table.add_hline()
        table.add_row((bold("Staff Member"), staff_member))
        table.add_hline()
        table.add_row((bold("Member Name"), member.display_name))
        table.add_hline()
        table.add_row((bold("Member ID"), member.display_name))
        table.add_hline()
        table.add_row((bold("Action Taken"), action))
        table.add_hline()

    doc.append(NoEscape(r"\vspace{1cm}"))
    doc.append(NoEscape(r"\section*{Reason}"))
    doc.append(NoEscape(r"\noindent\fbox{\begin{minipage}[t][6cm][t]{12cm}"))
    doc.append(reason)
    doc.append(NoEscape(r"\end{minipage}}"))

    header = PageStyle("header")
    with header.create(Foot("C")):
        header.append(NoEscape(r"\textcolor{gray}{104th Battalion MilSim - RAS Vanguard}"))
    doc.preamble.append(header)
    doc.change_document_style("header")

    doc.generate_pdf(filepath, clean_tex=True, clean=True, silent=True)

    doc = fitz.open(filepath + '.pdf')
    page = doc.load_page(0)
    pixmap = page.get_pixmap(dpi=300)
    img = pixmap.tobytes()
    doc.close()
    with open(f"{filepath}.png", 'wb') as f:
        f.write(img)




class Brig(commands.Cog):
    def __init__(self, bot: DatacoreBot, counter: int = 0):
        self.bot = bot
        self.counter = counter

    def case_ref(self, dtype: str):
        self.counter += 1
        return f"VCL-{dtype.upper()[0]}-{str(self.counter).zfill(4)}"

    brig = discord.SlashCommandGroup(name="brig", description="Commands for the Brig")

    @brig.command()
    async def suspend(self, ctx: discord.ApplicationContext, member: discord.Member, reason: str):
        ref = self.case_ref("Suspended")
        dp_action_form(ref, ctx.author.display_name, member, "Suspended", reason)
        file = discord.File(os.path.join(os.path.dirname(__file__), f"VCL/{ref}.png"))

        archive_guild: discord.Guild = self.bot.get_guild(1040820793950605363) or await self.bot.fetch_guild(1040820793950605363)
        archive_channel: discord.ForumChannel = archive_guild.get_channel(1276507291956543488) or await archive_guild.fetch_channel(1276507291956543488)
        tag: discord.ForumTag = discord.utils.get(archive_channel.available_tags, name="Suspension")
        await archive_channel.create_thread(name=f"{ref}", content=f"Case Ref: {ref}\nMember Name: {member.display_name}\nMember ID: {member.id}", file=file, auto_archive_duration=1440, applied_tags=[tag])
        await ctx.response.send_message(f"Suspended {member.mention} for {reason} Vanguard Case Report has been sent", ephemeral=True)

    @commands.command()
    async def ras(self, ctx: commands.Context):
        server = await self.bot.fetch_guild(667872108810076160)
        for channel in server.channels:
            print(f"{channel.name} | {channel.id}")

def setup(bot):
    bot.add_cog(Brig(bot))
