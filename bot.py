from discord.ext import commands
import requests, discord
from color import c
import config

token = config.Token.bot

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="-", intents=intents)

cogs = ["jishaku", "bigbrain"]

@bot.event
async def on_ready():
    for cog in cogs:
        await bot.load_extension(cog)
    await bot.tree.sync()
    print(f"{c.Green}Logged in as {c.Yellow}{bot.user}{c.c}")

bot.run(token)
