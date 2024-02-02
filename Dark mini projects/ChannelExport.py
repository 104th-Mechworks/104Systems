import io
import discord
import chat_exporter
from discord.ext import commands

bot = commands.Bot(command_prefix='.', intents=discord.Intents.all())


@bot.event
async def on_ready():
    print(f"{bot.user.name}")

@bot.command()
async def transcript(ctx: commands.Context):
    await ctx.message.delete()
    transcript = await chat_exporter.export(
        channel=ctx.channel,
        limit=None,
        tz_info="UTC",
        military_time=True,
        bot=bot
    )

    if transcript is None:
        return

    transcript_file = discord.File(
        io.BytesIO(transcript.encode()),
        filename=f"transcript-{ctx.channel.name}.html",
    )

    await ctx.author.send(file=transcript_file)

bot.run("OTMzMjkxNTUxNzQyOTA2NDA4.Gy-BYb.ZgqDwVullkmDLgYJQSJTi0AmeMXCoVYKBxAjxU")