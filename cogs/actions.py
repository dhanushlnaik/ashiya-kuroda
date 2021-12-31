import discord
from discord.ext import commands
from PIL import Image, ImageDraw
from io import BytesIO
import requests
import json
import random
from dotenv import load_dotenv
import os


load_dotenv()
API_KEY = os.environ.get("WEEBY_API_KEY")

def return_gif(arg):
    request = requests.get(f"https://weebyapi.xyz/gif/{arg}?token={str(API_KEY)}")
    rjson = json.loads(request.content)
    return rjson['url']



class Actions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name=f"hug",aliases=[],usage="@user",description="Hug a User.")
    async def hug(self, ctx, m: discord.Member = None):
        if m == None:
            await ctx.send("Please mention someone to hug!")
        elif m == ctx.author:
            await ctx.send(f"{ctx.author.mention} Do you need someone to hug..? I can hug you :)")
        else:
            emb = discord.Embed(description=f"{ctx.author.mention} hugs {m.mention} ~~ awiee!", color=ctx.author.color)
            emb.set_image(url=return_gif("hug"))
            await ctx.send(embed=emb)

    @commands.command(name=f"pat",aliases=["pats"],usage="@user",description="Pat a User.")
    async def pat(self, ctx, m: discord.Member = None):
        if m == None:
            await ctx.send("Please mention someone to pat!")
        elif m == ctx.author:
            await ctx.send(f"{ctx.author.mention} Do you need someone to pat..? I can pat you :)")
        else:
            emb = discord.Embed(description=f"{ctx.author.mention} pats {m.mention} ~~ awiee!", color=ctx.author.color)
            emb.set_image(url=return_gif("pat"))
            await ctx.send(embed=emb)
    
    @commands.command(name=f"punch",aliases=[],usage="@user",description="Punches a User.")
    async def punch(self, ctx, m: discord.Member = None):
        if m == None:
            await ctx.send("Please mention someone to punch!")
        elif m == ctx.author:
            await ctx.send(f"{ctx.author.mention} You want to punch yourself..? Are you sure..?")
        elif m.id == self.bot.user.id:
            emb = discord.Embed(description=f"no u {ctx.author.mention}", color=0x2e69f2)
            emb.set_image(url="https://c.tenor.com/eaAbCBZy0PoAAAAS/reverse-nozumi.gif")
            await ctx.reply(embed=emb)
        else:
            emb = discord.Embed(description=f"{ctx.author.mention} punches {m.mention} ~ OwO", color=0x2e69f2)
            req = requests.get('https://shiro.gg/api/images/punch')
            rjson = json.loads(req.content)
            emb.set_image(url=rjson['url'])
            await ctx.send(embed=emb)

    @commands.command(name=f"kiss",aliases=[],usage="@user",description="Kiss a User.")
    async def kiss(self, ctx, m: discord.Member = None):
        if m == None:
            await ctx.send("Please mention someone to kiss!")
        elif m == ctx.author:
            await ctx.send(f"{ctx.author.mention} You want to kiss yourself ...? I can give you a kiss :)")
        emb = discord.Embed(description=f"{ctx.author.mention} kisses {m.mention} ~ cute", color=0x2e69f2)
        emb.set_image(url=return_gif("kiss"))
        await ctx.send(embed=emb)
    
    @commands.command(name=f"cuddle",aliases=[],usage="@user",description="Cuddle a User.")
    async def cuddle(self, ctx, m: discord.Member = None):
        if m == ctx.author:
            await ctx.reply("aww, you want a cuddle? I can give you a cuddle :)")
        elif m == None:
            await ctx.reply("Please `mention` someone to cuddle!")
        else:
            emb = discord.Embed(description=f"{ctx.author.mention} cuddles {m.mention} ~ kyaaa!", color=0x2e69f2)
            emb.set_image(url=return_gif("cuddle"))
            await ctx.send(embed=emb)
    
    @commands.command(name=f"slap",aliases=[],usage="@user",description="Slap a User.")
    async def slap(self, ctx, m: discord.Member = None):
        if m == None:
            m = ctx.author
        else:
            emb = discord.Embed(description=f"{ctx.author.mention} slaps {m.mention} ~ baakaah", color=0x2e69f2)
            emb.set_image(url=return_gif("slap"))
            await ctx.send(embed=emb)
    
    @commands.command(name=f"pout",aliases=[],usage="@user",description="Pout.")
    async def pout(self, ctx, m: discord.Member = None):
        if m == None:
            m = ctx.author
        emb = discord.Embed(description=f"{ctx.author.mention} pouts at {m.mention} ~ hmph", color=0x2e69f2)
        req = requests.get('https://shiro.gg/api/images/pout')
        rjson = json.loads(req.content)
        emb.set_image(url=rjson['url'])
        await ctx.send(embed=emb)

    @commands.command(name=f"smug",aliases=[],usage="@user",description="Smug.")
    async def smug(self, ctx, m: discord.Member = None):
        if m == None:
            m = ctx.author
        emb = discord.Embed(description=f"{ctx.author.mention} smugs at {m.mention} ~ blehh", color=0x2e69f2)
        emb.set_image(url=return_gif("smug"))
        await ctx.send(embed=emb)

    @commands.command(name=f"tickle",aliases=[],usage="@user",description="Tickles a User.")
    async def tickle(self, ctx, m: discord.Member = None):
        if m == None:
            m = ctx.author
        emb = discord.Embed(description=f"{ctx.author.mention} tickles {m.mention} ~_~", color=0x2e69f2)
        emb.set_image(url=return_gif("tickle"))
        await ctx.send(embed=emb)

    @commands.command(name=f"kill",aliases=[],usage="@user",description="Kills a User.")
    async def kill(self, ctx, m: discord.Member = None):
        if m == None:
            await ctx.reply("Who do you want to `kill`?")
        else:
            emb = discord.Embed(description=f"{ctx.author.mention} kills {m.mention} ~ RIP", color=0x2e69f2)
            print(return_gif("kill"))
            emb.set_image(url=return_gif("kill"))
            await ctx.send(embed=emb)

    @commands.command(name=f"bonk",aliases=[],usage="@user",description="Bonks a User.")
    async def bonk(self, ctx, m: discord.Member = None):
        if m == None:
            m = ctx.author
        emb = discord.Embed(description=f"{ctx.author.mention} bonks {m.mention} ~ >.<", color=0x2e69f2)
        emb.set_image(url=return_gif("bonk"))
        await ctx.send(embed=emb)

    @commands.command(name=f"highfive",aliases=[],usage="@user",description="HighFive's a User.")
    async def highfive(self, ctx, m: discord.Member = None):
        if m == None:
            m = ctx.author
        emb = discord.Embed(description=f"{ctx.author.mention} high fives {m.mention} ~ yoshh!", color=0x2e69f2)
        emb.set_image(url=return_gif('highfive'))
        await ctx.send(embed=emb)

    @commands.command(name=f"nom",aliases=[],usage="@user",description="Ur Mom Nom Nom")
    async def nom(self, ctx, m: discord.Member = None):
        if m == None:
            m = ctx.author
        emb = discord.Embed(description=f"{ctx.author.mention} noms {m.mention} ~ nyaa!", color=0x2e69f2)
        req = requests.get('https://shiro.gg/api/images/nom')
        rjson = json.loads(req.content)
        emb.set_image(url=rjson['url'])
        await ctx.send(embed=emb)

    @commands.command(name=f"pokes",usage="@user",description="Pokes.",aliases=['boop'])
    async def pokes(self, ctx, m: discord.Member = None):
        if m == None:
            m = ctx.author
        emb = discord.Embed(description=f"{ctx.author.mention} pokes {m.mention} ~ OwO", color=0x2e69f2)
        req = requests.get('https://shiro.gg/api/images/poke')
        rjson = json.loads(req.content)
        emb.set_image(url=rjson['url'])
        await ctx.send(embed=emb)

    @commands.command(name=f"blush",aliases=[],usage="@user",description="Blushes.")
    async def blush(self, ctx, m: discord.Member = None):
        if m == None:
            m = ctx.author
        emb = discord.Embed(description=f"{ctx.author.mention} blushes at {m.mention} ~ >.<", color=0x2e69f2)
        req = requests.get('https://shiro.gg/api/images/blush')
        rjson = json.loads(req.content)
        emb.set_image(url=rjson['url'])
        await ctx.send(embed=emb)

    @commands.command(aliases=["hold"],name=f"",usage="@user",description="Handholds a User.")
    async def handhold(self, ctx, m: discord.Member = None):
        if m == None:
            m = ctx.author
        emb = discord.Embed(description=f"{ctx.author.mention} holds {m.mention}'s hands ~ cutee", color=0x2e69f2)
        emb.set_image(url=return_gif("handhold"))
        await ctx.send(embed=emb)

    @commands.command(name=f"feed",aliases=[],usage="@user",description="Feeds a User.")
    async def feed(self, ctx, m: discord.Member = None):
        if m == None:
            m = ctx.author
        emb = discord.Embed(description=f"{ctx.author.mention} feeds {m.mention} ~ uwu", color=0x2e69f2)
        emb.set_image(url=return_gif("feed"))
        await ctx.send(embed=emb)


def setup(bot):
    bot.add_cog(Actions(bot))