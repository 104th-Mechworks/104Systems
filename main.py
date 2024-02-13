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
    # logger.setLevel(logging.DEBUG if debug else logging.INFO)
    logger.setLevel(logging.DEBUG)
    pre_start()
    # bot.run("MTA3ODI0OTAzMzU0NzY2NTQ4OQ.GPko32.7DLzajDZqQ1O5yskoXRgbu5Z25ioErhq0J6zAk")
    bot.run("OTMzMjkxNTUxNzQyOTA2NDA4.GztRJL.qqZj2QkkU9gq6C2Qzq3dDaJRv9gL1Fq0Ot13Yk")
    
