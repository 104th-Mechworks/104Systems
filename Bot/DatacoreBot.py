import asyncio
import json
import logging

import os
from contextlib import suppress

import aiohttp
import discord
import pomice
from discord import ApplicationContext, DiscordException
from discord.ext import commands
from discord.ext.commands import errors
from dotenv import load_dotenv

# from Bot.utils.DB import connect_to_db
from Bot.utils.handlers import command_error_handler
from Bot.utils.logger import logger as log

load_dotenv()

intents = discord.Intents.all()
# log = logging.getLogger("Datacore")
log.setLevel(logging.DEBUG)


def get_db_path() -> str:
    current_dir = os.path.dirname(__file__)
    parent_dir = os.path.dirname(current_dir)
    file_path = os.path.join(parent_dir, 'main.sqlite')
    return file_path


class DatacoreBot(commands.Bot):
    """
    Main Bot Class for the Datacore Bot, this handles start up and connection to the Lavalink nodes.
    Also handles command errors that are not handled by the cogs directly.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.first_start = True
        self.pool = pomice.NodePool()
        self.DB_PATH = get_db_path()

    async def read_nodes(self):
        with open("lavalink.json", "r") as f:
            data: dict = json.load(f)
        tasks = [
            asyncio.create_task(self.connect_node(key, value))
            for key, value in data.items()
        ]
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
                spotify_client_id=(
                    None if values["SPOTIFY_ID"] == "" else values["SPOTIFY_ID"]
                ),
                spotify_client_secret=(
                    None if values["SPOTIFY_SECRET"] == "" else values["SPOTIFY_SECRET"]
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
            await self.wait_until_ready()
            log.success(
                f"Bot started as {self.user.name}#{self.user.discriminator} | {self.user.id}"
            )
            await self.read_nodes()
            self.first_start = False
            self.status = discord.Status.dnd
            self.activity = discord.Activity(
                type=discord.ActivityType.watching, name=f"{len(self.guilds)}: Servers"
            )

    async def on_command_error(self, ctx: commands.Context, exception) -> None:
        if isinstance(exception, errors.CommandNotFound):
            suppress(errors.CommandNotFound)
        else:
            await command_error_handler(ctx, exception)

    async def on_application_command_error(
        self, ctx: ApplicationContext, exception: DiscordException
    ) -> None:
        await command_error_handler(ctx, exception)
