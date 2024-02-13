import io
import discord
import chat_exporter
from discord.ext import commands

bot = commands.Bot(command_prefix='.', intents=discord.Intents.all())

open_transcripts = 0
@bot.event
async def on_ready():
    print(f"{bot.user.name}")

@bot.command()
async def transcript(ctx: commands.Context):
    await ctx.message.delete()

    global open_transcripts
    open_transcripts +=1

    print('start |', ctx.guild.name, '|', ctx.channel.name, "open tasks |", open_transcripts)
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
    print('end |', ctx.guild.name, '|', ctx.channel.name)
    open_transcripts -= 1
    await ctx.author.send(file=transcript_file)

bot.run("OTMzMjkxNTUxNzQyOTA2NDA4.GC51if.ffThgx0jWz9mLLqoQuyPTwOWSCkZJT1tXW6Dvg")