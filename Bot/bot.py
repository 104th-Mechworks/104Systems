import datetime
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.all()

bot = commands.Bot(
    command_prefix=".",
    intents=intents,
    activity=discord.Activity(
        type=discord.ActivityType.watching, name="104th Battalion Milsim"
    ),
)

cogs_list = [
    "attendance",
    "brig",
    "info",
    "music",
    "level",
    "medbay",
]

for cog in cogs_list:
    bot.load_extension(f"cogs.{cog}")


@bot.event
async def on_ready():
    print(
        f"Bot logged in\nName: {bot.user.name}\nID: {bot.user.id}\nStart: {datetime.datetime.now()}"
    )
    global start_time
    start_time = datetime.datetime.now()


bot.run(os.getenv("TOKEN"))
