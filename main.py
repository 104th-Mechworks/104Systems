from argparse import ArgumentParser
import asyncio
import logging
import discord
import os
from dotenv import load_dotenv
from Bot.DatacoreBot import DatacoreBot
from Bot.utils.DB import connect_to_db
from discord.ext import commands
import re

load_dotenv()

bot = DatacoreBot(
    command_prefix=".",
    case_insensitive=True,
    strip_after_prefix=True,
    intents=discord.Intents.all(),
    activity=discord.Activity(
        type=discord.ActivityType.watching, name="104th Battalion"
    ),
    status=discord.Status.dnd,
)



exp = r"^([A-Z0-9]{2,4}) ([A-ZÁÉÍÓÚÜ][A-ZÁÉÍÓÚÜa-záéíóúü]+) ((?:[A-Z]{1,3}-)(?:(?:[0-9]{4,5})|(?:[0-9]{2}-[0-9]{3})|(?:\d+-\d+\/\d+)|(?:\d+-\d{4})))$"

bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())


@bot.command()
async def nget(ctx: commands.Context):
    i=0
    with open("names.txt", "w") as f:
        f.write("104th Names reverse order\n")
        async for message in ctx.channel.history(limit=1000000000):
            match = re.match(exp, message.content)
            if match:
                print(f"{i} | {' '.join(match.groups())}")
                f.write(f"{' '.join(match.groups())}\n")
                i +=1
                asyncio.sleep(0.2)
                continue


def pre_start():
    bot.load_extensions("Bot.cogs", recursive=True)


if __name__ == "__main__":
    parser = ArgumentParser(prog="Datacore")
    parser.add_argument(
        "-d",
        "--debug",
        dest="cogs",
        action="extend",
        nargs="*",
        help="run in debug mode",
    )
    parser.add_argument(
        "-s",
        "--sync",
        action="store_true",
        help="synchronize commands",
    )
    args = parser.parse_args()
    debug = args.cogs is not None

    load_dotenv(".env")

    logger = logging.getLogger("Datacore")
    logger.setLevel(logging.DEBUG if debug else logging.INFO)

    pre_start()
    bot.run("MTA3ODI0OTAzMzU0NzY2NTQ4OQ.GAaX-e.qC3W27emPb-Wk5lCepdt2vL3fjwlcyguzzw7v8")
# # TOKEN = "OTMzMjkxNTUxNzQyOTA2NDA4.Gy-BYb.ZgqDwVullkmDLgYJQSJTi0AmeMXCoVYKBxAjxU"
    
