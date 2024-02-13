# import json
# import os
# import discord
# from discord.ext import commands
#
# bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())
#
# @bot.command()
# async def hist(ctx: commands.Context):
#     with open(f"join-dates {ctx.guild.name}", "w") as f:
#         f.write("104th Join Dates\n")
#         async for member in ctx.guild.fetch_members(limit=None):
#             f.write(f"{member.display_name} | {member.joined_at.date()}\n")
#
#         f.close()
#
#
# @bot.command()
# async def ejs(ctx: commands.Context):
#     base_path = "icons/"
#     i = 1
#     async for guild in bot.fetch_guilds(limit=None):
#         print(f"Processing {guild.name}| number in list {i}: {len(bot.guilds)}")
#         i += 1
#         guild_path = base_path + guild.name.replace(" ", "-")
#
#         # Create the guild directory if it doesn't exist
#         os.makedirs(guild_path, exist_ok=True)
#         if not os.path.exists(guild_path):
#             emoji_path = os.path.join(guild_path, "emojis")
#             os.makedirs(emoji_path, exist_ok=True)
#
#             emojis = await guild.fetch_emojis()
#             for e in emojis:
#                 file_path = os.path.join(emoji_path, f"{e.name.replace(' ', '-')}.png")
#
#                 if e.animated:
#                     file_path = os.path.join(emoji_path, f"{e.name.replace(' ', '-')}.gif")
#                     await e.save(file_path)
#                 else:
#                     await e.save(file_path)
#
#             sticker_path = os.path.join(guild_path, "stickers")
#             os.makedirs(sticker_path, exist_ok=True)
#
#             stickers = await guild.fetch_stickers()
#             for s in stickers:
#                 file_path = os.path.join(sticker_path, f"{s.name.replace(' ', '-')}.png")
#                 try:
#                     await s.save(file_path)
#                 except Exception as e:
#                     print(guild)
#                     continue
#
# @bot.command()
# async def bl(ctx: commands.Context):
#     ban_list = []
#     async for ban_entry in ctx.guild.bans():
#         ban_data = {
#             'user_id': ban_entry.user.id,
#             'user_name': ban_entry.user.name,
#             'reason': ban_entry.reason
#         }
#         ban_list.append(ban_data)
#
#         # Write ban information to a JSON file
#     with open('bans.json', 'w') as json_file:
#         json.dump(ban_list, json_file, indent=4)
#         json_file.close()
#
#
# @bot.command()
# async def bb(ctx: commands.Context):
#     with open('bans.json', 'r') as json_file:
#         data = json.load(json_file)
#         json_file.close()
#
#     for ban in data:
#         await ctx.guild.ban(discord.Object(id=ban['user_id']), reason=ban['reason'])
#         print(f"Banned {ban['user_name']} | {ban['user_id']}")
#
#
# @bot.event
# async def on_ready():
#     print(f"{bot.user.name} is ready")
#
# bns = json.load(open("bans.json", "r"))
# print(len(bns))
#
# @bot.command()
# async def banm(ctx: commands.Context, id: int):
#     await ctx.guild.ban(discord.Object(id=id), reason="Banned by command")
#
# # bot.run("OTMzMjkxNTUxNzQyOTA2NDA4.GyfbZ5.P1IPcu9OSj13tujMxkWBTZ88e3XvkLkvcBdCZI")
# bot.run("MTA3ODI0OTAzMzU0NzY2NTQ4OQ.GPko32.7DLzajDZqQ1O5yskoXRgbu5Z25ioErhq0J6zAk")


import aiosqlite
import asyncio


def new_value_gen(current_value):
    match current_value:
        case "Company Commanding Officer":
            return "CCO"
        case "Company Executive Officer":
            return "CXO"
        case "Company Non-Commissioned Officer":
            return "CNCO"
        case "Platoon Commanding Officer":
            return "PCO"
        case "Platoon Executive Officer":
            return "PXO"
        case "Platoon Non-Commissioned Officer":
            return "PNCO"
        case "Squad Leader":
            return "SL"
        case "Squad Non-Commissioned Officer":
            return "SNCO"



async def replace_values():
    # Open a connection to the SQLite database
    async with aiosqlite.connect('your_database.db') as db:
        # Create a cursor object
        cursor = await db.cursor()

        # Execute a SELECT query to retrieve the values from the column you want to update
        await cursor.execute("SELECT ID, Position FROM Members")

        # Fetch all rows from the result set
        rows = await cursor.fetchall()

        # Iterate over the rows and replace the values with something else
        for row in rows:
            current_value = row[0]  # Assuming there's only one column in the result set
            # Replace the current value with something else (e.g., 'new_value')
            new_value = new_value_gen(current_value)
            # Execute an UPDATE query to replace the current value with the new value
            await cursor.execute("UPDATE Members SET Position = ? WHERE ID = ?", (new_value, current_value))

        # Commit the transaction to make the changes persistent
        await db.commit()

# Run the async function
asyncio.run(replace_values())

