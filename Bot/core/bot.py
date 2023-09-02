# from os import environ, getenv, listdir, path
# from traceback import format_exception

# import discord
# from discord.ext import commands
# from dotenv import load_dotenv

# from .models import setup_db

# # get the relative path fo the folder called "cogs"
# COGS_PATH = path.join(path.dirname(__file__), "..", "cogs")
# load_dotenv()


# class CPObot(commands.Bot):
#     def __init__(self) -> None:
#         super().__init__(
#             activity=discord.Activity(
#                 type=discord.ActivityType.watching, name="104th Battalion"
#             ),
#             allowed_mentions=discord.AllowedMentions.none(),
#             auto_sync_commands=False,
#             chunk_guilds_at_startup=False,
#             # help_command=None,
#             intents=discord.Intents.all(),
#             owner_ids=[],
#             command_prefix=".",
#         )

#     def get_cogs(x) -> list[str]:
#         "return each cog in the cogs folder"
#         for file in listdir(COGS_PATH):
#             if file.endswith(".py"):
#                 yield f"cogs.{file[:-3]}"

#     # async def setup_hook(self) -> None:
#     #     "Sets up the connection to the lavalink server for music features"
#     #     node: wavelink.Node = wavelink.Node(
#     #         uri=f"{environ.get('LAVALINK_URI')}",
#     #         password=f"{environ.get('LAVALINK_PSWRD')}",
#     #     )
#     #     await wavelink.NodePool.connect(client=self, node=[node])

#     def run(self, cogs: list[str] | None = None) -> None:
#         self.load_extensions(*cogs or self.get_cogs())
#         setup_db()
#         super().run(getenv("TOKEN"))

#     async def on_ready(self) -> None:
#         "send a success message to terminal when the bot is ready"
#         print("Bot is ready")
