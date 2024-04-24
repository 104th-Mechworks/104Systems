import asyncio
import discord
from discord.ext import commands
from discord.ext.commands import Context, errors
import logging

log = logging.getLogger("Datacore")


async def command_error_handler(ctx, exception):
    if isinstance(exception, asyncio.TimeoutError):
        log.error(exception)
    if isinstance(exception, commands.CommandInvokeError):
        log.error(exception)
    if isinstance(exception, commands.CommandOnCooldown):
        if isinstance(ctx, discord.ApplicationContext):
            await ctx.respond(
                f"Command is on cooldown, try again in {exception.retry_after:.2f} seconds.",
                ephemeral=True,
            )
        elif isinstance(ctx, commands.Context):
            await ctx.send(
                f"Command is on cooldown, try again in {exception.retry_after:.2f} seconds."
            )
    if isinstance(exception, commands.CheckFailure):
        log.error(exception)
        if isinstance(ctx, discord.ApplicationContext):
            await ctx.respond(
                "You do not have permission to run this command.", ephemeral=True
            )
        elif isinstance(ctx, commands.Context):
            await ctx.send("You do not have permission to run this command.")
    if isinstance(exception, commands.MissingRequiredArgument):
        log.error(exception)
        if isinstance(ctx, discord.ApplicationContext):
            await ctx.respond("You are missing a required argument.", ephemeral=True)
        elif isinstance(ctx, commands.Context):
            await ctx.send("You are missing a required argument.")
    if isinstance(exception, commands.BadArgument):
        log.error(exception)
        if isinstance(ctx, discord.ApplicationContext):
            await ctx.respond("You have provided a bad argument.", ephemeral=True)
        elif isinstance(ctx, commands.Context):
            await ctx.send("You have provided a bad argument.")
    else:
        log.error(exception)
        raise exception
