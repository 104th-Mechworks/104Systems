
from Bot.DatacoreBot import DatacoreBot

import io
import discord
import chat_exporter
from discord.ext import commands


open_transcripts = 0

class CExport(commands.Cog):
    def __init__(self, bot: DatacoreBot):
        self.bot = bot

    @commands.slash_command()
    async def ctranscript(self, ctx: discord.ApplicationContext):
        await ctx.defer()

        global open_transcripts
        open_transcripts += 1

        if open_transcripts == 4:
            await ctx.respond("max open processes", ephemeral=True)

        print('start |', ctx.guild.name, '|', ctx.channel.name, "open tasks |", open_transcripts)
        transcript = await chat_exporter.export(
            channel=ctx.channel,
            limit=None,
            tz_info="UTC",
            military_time=True,
            bot=self.bot
        )

        if transcript is None:
            return

        transcript_file = discord.File(
            io.BytesIO(transcript.encode()),
            filename=f"transcript-{ctx.channel.name}.html",
        )
        print('end |', ctx.guild.name, '|', ctx.channel.name)
        open_transcripts -= 1
        await ctx.user.send(file=transcript_file)
        await ctx.respond("done", ephemeral=True)

def setup(bot: DatacoreBot):
    bot.add_cog(CExport(bot))
