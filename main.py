from argparse import ArgumentParser
import logging
import discord
import os
from dotenv import load_dotenv
from Bot.DatacoreBot import DatacoreBot


load_dotenv()


logger = logging.getLogger("Datacore")

# intents for verification
intents = discord.Intents.default()
intents.message_content = True
intents.members = True


bot = DatacoreBot(
    command_prefix=".",
    case_insensitive=True,
    strip_after_prefix=True,
    intents=intents,
    activity=discord.Activity(
        type=discord.ActivityType.custom, name="Maintenance..."
    ),
    status=discord.Status.dnd,
)


# function to load all cogs before bot starts
def pre_start():
    # bot.load_extensions("Bot.cogs", recursive=True)
    cogdir = os.path.join(os.path.dirname(__file__), "Bot", "cogs")

    for cog in os.listdir(cogdir):
        if cog.endswith(".py"):
            try:
                bot.load_extension(f"Bot.cogs.{cog[:-3]}")
                logger.debug(f"loaded cog: {cog[:-3]}")
            except Exception as e:
                logger.error(f"Failed to load cog {cog[:-3]}: {e}")


if __name__ == "__main__":
    # basic CLI interface for starting the bot with different parameters

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
        "-m",
        "--main",
        action="extend",
        help="run in main bot",
    )
    args = parser.parse_args()
    debug = args.cogs is not None

    # load environment variables
    load_dotenv(".env")
    logger.setLevel(logging.DEBUG if debug else logging.INFO)

    # load necessary files before bot starts
    pre_start()

    # Starts the bot and connects to Discord API
    bot.run(os.getenv("MAIN_TOKEN" if not debug else "DMAIN_TOKEN"))

