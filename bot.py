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

@bot.event
async def on_ready():
    print(f"{c.Green}Ready{c.c}")

@bot.event
async def on_message(message):
    if message.author == bot.user: return

    if message.content.startswith(("How", "When", "Where" "Why", "What", "Which")):
        if message.content.endswith("?"):
            await waget(message, message.content)
        else:
            await message.reply('A proper question ends with a question mark')
    else:
        # if message.channel == 710474717584425071:
        #     await message.reply(f'Sorry to bother, but the processed message does not contain a question.\nMessage content: ```{message.content}```')
    if message.content.startswith("Define"):
        m = message.content.split(" ")
        if len(m) == 1:
            try:
                await message.reply(f"What do you want me to define?")
            except:
                await message.send(f"What do you want me to define?")
        else:
            await waget(message, message.content)
    await bot.process_commands(message)

@bot.command()
async def hmm(ctx, *, request):
    await waget(ctx, request)

async def waget(ctx, request):
    print(f"{c.Green}Request: {c.c}{request} {c.Green}Requested By: {c.c}{ctx.author}")
    request = "%2b".join(request.split("+"))
    request = "+".join(request.split(" "))
    r = requests.get(f"https://api.wolframalpha.com/v1/result?i={request}&appid={wa_key}")
    if r.status_code != 200:
        if r.status_code == 501:
            print(f"{c.Red}No answer found - Returned 501{c.c}")
            try:
                await ctx.reply(f"Hmm... I don't seem to have an answer for that.")
            except:
                await ctx.send(f"Hmm... I don't seem to have an answer for that.")
        elif r.status_code == 403:
            print(f"Permission Denied - Returned 403")
            try:
                await ctx.reply(f"For some reason, I don't have permission to process your request. Consult the owner of the bot for more info.")
            except:
                await ctx.send(f"For some reason, I don't have permission to process your request. Consult the owner of the bot for more info.")
        elif r.status_code == 404:
            try:
                await ctx.reply(f"For some reason, I am unable to process your request. Consult the owner of the bot for more info.")
            except:
                await ctx.send(f"For some reason, I am unable to process your request. Consult the owner of the bot for more info.")
        else:
            try:
                await ctx.reply(f"Hmmm... an unknown error occured... ```Status code: {r.status_code}```")
            except:
                await ctx.send(f"Hmmm... an unknown error occured... ```Status code: {r.status_code}```")
    else:
        if str(r.content).startswith(("b'", 'b"')):
            if str(r.content).startswith("b'"):
                x = str(r.content).split("'")
            elif str(r.content).startswith('b"'):
                x = str(r.content).split('"')
            x.remove(x[0])
            x.remove(x[len(x) - 1])
            x = '"'.join(x)
        else:
            x = str(r.content)
        try:
            await ctx.reply(str(x))
        except:
            await ctx.send(str(x))

bot.run(token)
