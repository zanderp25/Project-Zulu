from discord.ext import commands
from discord import app_commands
from color import c
import discord, requests, config, re, asyncio

class BigBrain(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
        self.ctx_menu = app_commands.ContextMenu(
            name='Ask Big Brain',
            callback=self.message_context,
        )
        self.bot.tree.add_command(self.ctx_menu)

    async def cog_unload(self) -> None:
        self.bot.tree.remove_command(self.ctx_menu.name, type=self.ctx_menu.type)

    @commands.Cog.listener(name="on_message")
    async def on_message(self, message:discord.Message):
        if message.author.bot: return

        match = re.match(rf"<@!?{self.bot.user.id}>", message.content)
        if match:
            if message.content != match.group(0):
                await message.reply(await self.waget(message.author, message.guild, message.content.replace(match.group(0), '').strip(), message=True))
            else:
                await message.reply(
                    embed=discord.Embed(
                        title="Big Brain Bot",
                        description="Big Brain Bot is a bot by Zanderp25 that can answer various questions like"
                        "\"Why is the sky blue?\" or \"What is the capital of Colombia?\" \n\n"
                        "To use BigBrain, simply type the question you want to ask after the bot's mention.\n"
                        "For example, if you want to ask \"Why is the sky blue?\", type:\n"
                        f"```@{self.bot.user} Why is the sky blue?```\n"
                        "This bot is powered by the Wolfram Alpha API. For more information, visit: "
                        "https://www.wolframalpha.com/",
                ).set_author(
                    name="Big Brain Bot",
                    icon_url=self.bot.user.avatar.url,
                )
            )

    @commands.hybrid_command(name="question", description="Ask a question to Big Brain Bot.")
    @app_commands.describe(question="The question you want to ask.")
    async def question(self, ctx: commands.Context, question: str):
        await ctx.interaction.response.defer()
        await ctx.reply(await self.waget(ctx.author, ctx.guild, question))

    async def message_context(self, interaction: discord.Interaction, message: discord.Message):
        await interaction.response.defer()
        await message.reply(await self.waget(interaction.user, interaction.guild, message.content, ctx_menu=True))
        m = await interaction.followup.send("Sent!")
        await asyncio.sleep(5)
        await m.delete()

    async def check_message(self, request):
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
            return (result)
        else:
            return False

    async def waget(self, author, guild, request, *, ctx_menu=False, message=False):
        if ctx_menu: print(f"{c.RedDark}Context Menu ", end="")
        if message: print(f"{c.RedDark}Message ", end="")
        print(f"{c.Yellow}Request: {c.c}{request} {c.YellowDark}Requested By: {c.c}{author} {c.YellowDark}Guild: {c.c}{guild}")
        x = await self.check_message(request)
        if x != False:
            print(f"{c.Grey}Offline {c.Cyan}Answer:{c.c} {x}")
            return (str(x))
        request = "%2b".join(request.split("+"))
        request = "%26".join(request.split("&"))
        request = "+".join(request.split(" "))
        r = requests.get(f"https://api.wolframalpha.com/v1/result?i={request}&appid={config.Token.wolfram}")
        if r.status_code != 200:
            if r.status_code == 501:
                print(f"{c.Red}No answer found - Returned 501{c.c}")
                return (f"Hmm... I don't seem to have an answer for that.")
            elif r.status_code == 403:
                print(f"{c.Red}Permission Denied - Returned 403{c.c}")
                return (f"For some reason, I don't have permission to process your request. Consult the owner of the bot for more info.")
            elif r.status_code == 404:
                print(f"{c.Red}Not Found - Returned 404{c.c}")
                return (f"For some reason, I am unable to process your request. Consult the owner of the bot for more info.")
            else:
                print(f"{c.Red}Unknown Error - Returned {r.status_code}{c.c}")
                return (f"Hmmm... an unknown error occured... ```Status code: {r.status_code}```")
        else:
            x = r.content.decode()
            print(f"{c.Cyan}Answer:{c.c} {x}")
            return (str(x))

async def setup(bot):
    await bot.add_cog(BigBrain(bot))
