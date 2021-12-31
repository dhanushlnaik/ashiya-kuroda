import discord
from discord.ext import commands
import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.environ.get("WEEBY_API_KEY")

qcid = 902509178352988220
def return_gif(arg):
    request = requests.get(f"https://weebyapi.xyz/gif/{arg}?token={str(API_KEY)}")
    rjson = json.loads(request.content)
    return rjson['url']

def make_request(): # Get Quote
    response = requests.get("https://animechan.vercel.app/api/random", verify=False)
    resp = json.loads(response.content)
    return resp['anime'], resp['character'], resp['quote']

class Anime(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command(aliases=['animequote'], brief="Get an Anime Quote!",usage="",name="quote",help="huh", extras={"emoji": "📜"},description="Get a user's Avatar!")
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.default)
    async def sendquote(self, ctx):
        anime, char, quote = make_request()
        await ctx.message.add_reaction('✅')
        emb = discord.Embed(color=discord.Color.greyple())
        emb.set_author(name=f"{quote}\n\n~ {char} | {anime}")
        await ctx.channel.send(
            embed=emb
        )


    @commands.command(name=f"zerotwo",aliases=[],description="Random ZeroTwo Gifs.")
    async def zerotwo(self, ctx):
        emb = discord.Embed(color=ctx.author.color)
        emb.set_image(url=return_gif("zerotwo"))
        await ctx.send(embed=emb)
     
def setup(bot):
    bot.add_cog(Anime(bot))
    