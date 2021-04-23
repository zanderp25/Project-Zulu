from discord.ext import commands
import requests, discord
from color import c
import config

token = config.Token.bot

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=commands.when_mentioned_or("-"), intents=intents)

cogs = ["jishaku", "bigbrain"]

for cog in cogs:
    try:
        bot.load_extension(cog)
    except Exception as e:
        print(c.Red + "Error loading cog '" + cog + "': " + e + c.c)

@bot.event
async def on_ready():
    print(f"{c.Green}Ready{c.c}")

bot.run(token)
