from discord.ext import commands
import requests, discord
from color import c

token = open("token.txt").read()
wa_key = "QJE2KJ-9KXKKEVGXX"

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=commands.when_mentioned_or("-"), intents=intents)

cogs = ["jishaku"]

for cog in cogs:
    try:
        bot.load_extension(cog)
    except Exception as e:
        print(c.Red + "Error loading cog '" + cog + "': " + e + c.c)


@bot.command()
async def hmm(ctx, *, request):
    r = requests.get(f"https://api.wolframalpha.com/v1/result?i={'+'.join(request.split(' '))}&appid={wa_key}")
    if r.status_code != 200:
        try:
            await ctx.reply(f"Hmmm... an unknown error occured... ```Status code: {r.status_code}```")
        except:
            await ctx.send(f"Hmmm... an unknown error occured... ```Status code: {r.status_code}```")
    else:
        x = str(r.content).split("'")
        x.remove(x[0])
        x.remove(x[len(x) - 1])
        x = "'".join(x)
        try:
            await ctx.reply(str(x))
        except:
            await ctx.send(str(x))
    print(c.c)


@bot.event
async def on_ready():
    print(f"{c.Green}Ready{c.c}")


bot.run(token)
