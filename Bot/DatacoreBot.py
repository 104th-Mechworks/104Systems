import asyncio
import json
import logging
import os
import aiohttp
import discord
import pomice
from discord.ext import commands
from dotenv import load_dotenv
from Bot.utils.logger import logger as log


load_dotenv()

intents = discord.Intents.all()
# log = logging.getLogger("Datacore")


class DatacoreBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.first_start = True
        self.pool = pomice.NodePool()

    async def read_nodes(self):
        with open("lavalink.json", "r") as f:
            data: dict = json.load(f)
        tasks = [asyncio.create_task(self.connect_node(key, value)) for key, value in data.items()]
        await self.wait_until_ready()
        await asyncio.gather(*tasks)
        log.info(f"We got {len(self.pool.nodes)} Nodes in total.")

    async def connect_node(self, node, values):
        identifier = node.upper()
        try:
            await self.pool.create_node(
                bot=self,
                host=values["HOST"],
                port=values["PORT"],
                password=values["PASSWORD"],
                secure=values["SECURE"],
                identifier=identifier,
                fallback=True,
                log_level=logging.WARNING,
                spotify_client_id=(
                    None if values["SPOTIFY_ID"] == "" else values["SPOTIFY_ID"]
                ),
                spotify_client_secret=(
                    None
                    if values["SPOTIFY_SECRET"] == ""
                    else values["SPOTIFY_SECRET"]
                ),
            )
            log.info(
                f"Lavalink '{identifier}' connected on {'https' if values['SECURE'] is True else 'http'}://{values['HOST']}:{values['PORT']}"
            )
        except pomice.NodeConnectionFailure:
            log.warning(
                f"Node didn't respond: Lavalink '{identifier}' didn't connect on {'https' if values['SECURE'] is True else 'http'}://{values['HOST']}:{values['PORT']}"
            )
        except pomice.LavalinkVersionIncompatible:
            log.error(
                f"Incompatible Lavalink Version:  '{identifier}' didn't connect on {'https' if values['SECURE'] is True else 'http'}://{values['HOST']}:{values['PORT']}"
            )
        except ValueError:
            log.warning(
                f"ValueError: Lavalink '{identifier}' didn't connect on {'https' if values['SECURE'] is True else 'http'}://{values['HOST']}:{values['PORT']}"
            )
        except aiohttp.ContentTypeError:
            log.warning(
                f"ContentTypeError: Lavalink '{identifier}' had issues on {'https' if values['SECURE'] is True else 'http'}://{values['HOST']}:{values['PORT']}"
            )

    async def on_ready(self) -> None:
        if self.first_start:
            log.success(
                f"Bot started as {self.user.name}#{self.user.discriminator} | {self.user.id}"
            )
            await self.read_nodes()
            self.first_start = False


bot = DatacoreBot(
    command_prefix=".",
    case_insensitive=True,
    strip_after_prefix=True,
    intents=discord.Intents.all(),
    activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="104th Battalion"
        ),
    status=discord.Status.dnd
)


@bot.slash_command()
async def reload(ctx: discord.ApplicationContext, extension: discord.Option(description="cog to reload", choices=["attendance", "brig", "info", "music", "level", "medbay"])):
    bot.reload_extension(f"cogs.{extension}")
    await ctx.respond(f"Reloaded {extension}")


def pre_start():
    bot.load_extensions("cogs", recursive=True)


if __name__ == "__main__":
    pre_start()
    bot.run(os.getenv("TOKEN"))
