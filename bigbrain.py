from discord.ext import commands
from color import c
import discord, requests, config

class BigBrain(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener(name="on_message")
    async def on_message(self, message):
        if message.author == self.bot.user: return

        if message.content.lower().startswith(("how", "when", "where", "why", "what", "which")):
            if message.content.endswith("?"):
                await self.waget(message, message.content)
            else:
                await message.reply('A proper question ends with a question mark lol', delete_after=5)
        else:
            pass
            # if message.channel == 710474717584425071:
            #     await message.reply(f'Sorry to bother, but the processed message does not contain a question.\nMessage content: ```{message.content}```')
        if message.content.lower().startswith("define"):
            m = message.content.split(" ")
            if len(m) == 1:
                try:
                    await message.reply(f"What do you want me to define?")
                except:
                    await message.send(f"What do you want me to define?")
            else:
                await self.waget(message, message.content)
        await self.bot.process_commands(message)

    @commands.command(aliases=["bigbrain","?","¿"])
    async def hmm(self, ctx, *, request):
        await self.waget(ctx, request)

    async def waget(self, ctx, request):
        print(f"{c.Yellow}Request: {c.c}{request} {c.YellowDark}Requested By: {c.c}{ctx.author}")
        request = "%2b".join(request.split("+"))
        request = "+".join(request.split(" "))
        r = requests.get(f"https://api.wolframalpha.com/v1/result?i={request}&appid={config.Token.wolfram}")
        if r.status_code != 200:
            if r.status_code == 501:
                print(f"{c.Red}No answer found - Returned 501{c.c}")
                try:
                    await ctx.reply(f"Hmm... I don't seem to have an answer for that.")
                except:
                    await ctx.send(f"Hmm... I don't seem to have an answer for that.")
            elif r.status_code == 403:
                print(f"{c.Red}Permission Denied - Returned 403{c.c}")
                try:
                    await ctx.reply(f"For some reason, I don't have permission to process your request. Consult the owner of the bot for more info.")
                except:
                    await ctx.send(f"For some reason, I don't have permission to process your request. Consult the owner of the bot for more info.")
            elif r.status_code == 404:
                print(f"{c.Red}Not Found - Returned 404{c.c}")
                try:
                    await ctx.reply(f"For some reason, I am unable to process your request. Consult the owner of the bot for more info.")
                except:
                    await ctx.send(f"For some reason, I am unable to process your request. Consult the owner of the bot for more info.")
            else:
                print(f"{c.Red}Unknown Error - Returned {r.status_code}{c.c}")
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
            print(f"{c.Cyan}Answer:{c.c} {x}")
            try:
                await ctx.reply(str(x))
            except:
                await ctx.send(str(x))

def setup(bot):
    bot.add_cog(BigBrain(bot))