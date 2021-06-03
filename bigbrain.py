from discord.ext import commands
from color import c
import discord, requests, config

class BigBrain(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener(name="on_message")
    async def on_message(self, message):
        if message.author == self.bot.user: return

        if message.content.lower().startswith(("how", "when", "where", "why", "what", "which", "who")):
            if message.content.endswith("?"):
                await self.waget(message, message.content)
            else:
                await message.reply('A proper question ends with a question mark lol', delete_after=5)
        if message.content.lower().startswith("define"):
            m = message.content.split(" ")
            if len(m) == 1:
                try:
                    await message.reply(f"What do you want me to define?")
                except:
                    await message.send(f"What do you want me to define?")
            else:
                await self.waget(message, message.content)

    @commands.command(aliases=["bigbrain","?","¿"])
    async def hmm(self, ctx, *, request):
        await self.waget(ctx, request)

    async def check_message(self, ctx, request, m):
        qna = {
            "who are you?":"I am Big Brain Bot, powered by Wolfram Alpha.",
            "who made you?":"I was made by Zanderp25. You can come see his server here: *https://discord.gg/672yY5v*.\nI also use the Wolfram Alpha API that was made by Stephen Wolfram and his team.",
            "define yeet":"(╯°□°）╯︵ ┻━┻",
            "where am i?":"I don't know. Discord doesn't tell me.",
            "what is my ip address?":"I don't know. Discord doesn't tell me.",
            "what's the weather like today?":"Today, it's cloudy with a chance of meatballs.",
            "question":"Answer",
        }
        result = qna.get(request.lower(), False)
        if result is not False:
            await m.edit(content=result)
            return result
        else:
            return False

    async def waget(self, ctx, request):
        m = ctx.reply("Loading...")
        print(f"{c.Yellow}Request: {c.c}{request} {c.YellowDark}Requested By: {c.c}{ctx.author}")
        x = await self.check_message(ctx, request, m)
        if x is False:
            pass
        else:
            print(f"{c.Grey}Offline {c.Cyan}Answer:{c.c} {x}")
            await m.edit(content=str(x))
            return
        request = "%2b".join(request.split("+"))
        request = "+".join(request.split(" "))
        r = requests.get(f"https://api.wolframalpha.com/v1/result?i={request}&appid={config.Token.wolfram}")
        if r.status_code != 200:
            if r.status_code == 501:
                print(f"{c.Red}No answer found - Returned 501{c.c}")
                await m.edit(f"Hmm... I don't seem to have an answer for that.")
            elif r.status_code == 403:
                print(f"{c.Red}Permission Denied - Returned 403{c.c}")
                await m.edit(content=f"For some reason, I don't have permission to process your request. Consult the owner of the bot for more info.")
            elif r.status_code == 404:
                print(f"{c.Red}Not Found - Returned 404{c.c}")
                await m.edit(content=f"For some reason, I am unable to process your request. Consult the owner of the bot for more info.")
            else:
                print(f"{c.Red}Unknown Error - Returned {r.status_code}{c.c}")
                await m.edit(content=f"Hmmm... an unknown error occured... ```Status code: {r.status_code}```")
        else:
            x = r.content.decode()
            print(f"{c.Cyan}Answer:{c.c} {x}")
            await m.edit(content=str(x))

def setup(bot):
    bot.add_cog(BigBrain(bot))
