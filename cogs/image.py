import discord
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont, ImageSequence
from io import BytesIO
import random
import imageio
import datetime
import numpy as np
import requests
from typing import Union, Optional
from petpetgif import petpet as petpetgif
import aiohttp
from dotenv import load_dotenv
import os
import json


load_dotenv()
API_KEY = os.environ.get("WEEBY_API_KEY")

def resize(image):
    size = 200, 200
    im = Image.open(image)
    global frames
    frames = ImageSequence.Iterator(im)
    def thumbnails(frames):
        for frame in frames:
            thumbnail = frame.copy()
            thumbnail.thumbnail(size, Image.ANTIALIAS)
            yield thumbnail
    frames = thumbnails(frames)
    om = next(frames)
    om.info = im.info
    return om


class Cards(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(usage="@user")
    async def pet(self,ctx, image: Optional[Union[discord.PartialEmoji, discord.member.Member]]):
        '''Give Pets!'''
        if type(image) == discord.PartialEmoji:
            return
        elif type(image) == discord.member.Member:
            image = await image.avatar.with_format("png").url.read() # retrieve the image bytes
        else:
            await ctx.reply('Please tag a member to petpet their avatar.')
            return

        source = BytesIO(image) # file-like container to hold the emoji in memory
        dest = BytesIO() # container to store the petpet gif in memory
        petpetgif.make(source, dest)
        dest.seek(0) # set the file pointer back to the beginning so it doesn't upload a blank file.
        await ctx.send(file=discord.File(dest, filename=f"{image[0]}-petpet.gif"))

    
    @commands.command(usage="@user")
    async def triggered(self, ctx, member: discord.Member=None):
        '''AWW! U ARE TRIGGERED?'''
        member = member or ctx.author
        await ctx.trigger_typing()
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://some-random-api.ml/canvas/triggered?avatar={member.avatar.with_format("png").url}') as af:
                if 300 > af.status >= 200:
                    fp = BytesIO(await af.read())
                    file = discord.File(fp, "triggered.gif")
                    em = discord.Embed(
                        color=0xf1f1f1,
                    )
                    em.set_image(url="attachment://triggered.gif")
                    await ctx.send(embed=em, file=file)
                else:
                    return
                await session.close()

    @commands.command(usage="@user")
    async def horny(self,ctx, member: discord.Member = None):
        '''Horny license just for u!'''
        member = member or ctx.author
        await ctx.trigger_typing()
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://some-random-api.ml/canvas/horny?avatar={member.avatar.with_format("png").url}') as af:
                if 300 > af.status >= 200:
                    fp = BytesIO(await af.read())
                    file = discord.File(fp, "horny.png")
                    em = discord.Embed(
                        color=0xf1f1f1,
                    )
                    em.set_image(url="attachment://horny.png")
                    await ctx.send(embed=em, file=file)
                else:
                    await ctx.send('No horny :(')
                await session.close()

    @commands.command(usage="@user")
    async def gaycard(self, ctx, member: discord.Member=None):
        '''You are Gae Bro!'''
        member = member or ctx.author
        await ctx.trigger_typing()
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://some-random-api.ml/canvas/gay?avatar={member.avatar.with_format("png").url}') as af:
                if 300 > af.status >= 200:
                    fp = BytesIO(await af.read())
                    file = discord.File(fp, "gay.gif")
                    em = discord.Embed(
                        color=0xf1f1f1,
                    )
                    em.set_image(url="attachment://gay.gif")
                    await ctx.send(embed=em, file=file)
                else:
                    return
                await session.close()
        
    @commands.command(usage="@user")
    async def glass(self, ctx, member: discord.Member=None):
        '''Glass Overlay!'''
        member = member or ctx.author
        await ctx.trigger_typing()
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://some-random-api.ml/canvas/glass?avatar={member.avatar.with_format("png").url}') as af:
                if 300 > af.status >= 200:
                    fp = BytesIO(await af.read())
                    file = discord.File(fp, "glass.gif")
                    em = discord.Embed(
                        color=0xf1f1f1,
                    )
                    em.set_image(url="attachment://glass.gif")
                    await ctx.send(embed=em, file=file)
                else:
                    return
                await session.close()

    @commands.command(usage="@user")
    async def wasted(self, ctx, member: discord.Member=None):
        '''Hands Up!'''
        member = member or ctx.author
        await ctx.trigger_typing()
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://some-random-api.ml/canvas/wasted?avatar={member.avatar.with_format("png").url}') as af:
                if 300 > af.status >= 200:
                    fp = BytesIO(await af.read())
                    file = discord.File(fp, "wasted.gif")
                    em = discord.Embed(
                        title="bonk",
                        color=0xf1f1f1,
                    )
                    em.set_image(url="attachment://wasted.gif")
                    await ctx.send(embed=em, file=file)
                else:
                    return
                await session.close()

    @commands.command(usage="@user")
    async def mission(self, ctx, member: discord.Member=None):
        '''Mission Passed'''
        member = member or ctx.author
        await ctx.trigger_typing()
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://some-random-api.ml/canvas/mission?avatar={member.avatar.with_format("png").url}') as af:
                if 300 > af.status >= 200:
                    fp = BytesIO(await af.read())
                    file = discord.File(fp, "mission.gif")
                    em = discord.Embed(
                        title="bonk",
                        color=0xf1f1f1,
                    )
                    em.set_image(url="attachment://mission.gif")
                    await ctx.send(embed=em, file=file)
                else:
                    return
                await session.close()

    @commands.command(usage="@user")
    async def jail(self, ctx, member: discord.Member=None):
        '''Take me to Jail.'''
        member = member or ctx.author
        await ctx.trigger_typing()
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://some-random-api.ml/canvas/jail?avatar={member.avatar.with_format("png").url}') as af:
                if 300 > af.status >= 200:
                    fp = BytesIO(await af.read())
                    file = discord.File(fp, "jail.gif")
                    em = discord.Embed(
                        title="bonk",
                        color=0xf1f1f1,
                    )
                    em.set_image(url="attachment://jail.gif")
                    await ctx.send(embed=em, file=file)
                else:
                    return
                await session.close()

    @commands.command(aliases=["communist"],usage="@user")
    async def comrade(self, ctx, member: discord.Member=None):
        '''OUR COMMAND!'''
        member = member or ctx.author
        await ctx.trigger_typing()
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://some-random-api.ml/canvas/comrade?avatar={member.avatar.with_format("png").url}') as af:
                if 300 > af.status >= 200:
                    fp = BytesIO(await af.read())
                    file = discord.File(fp, "comrade.gif")
                    em = discord.Embed(
                        title="bonk",
                        color=0xf1f1f1,
                    )
                    em.set_image(url="attachment://comrade.gif")
                    await ctx.send(embed=em, file=file)
                else:
                    return
                await session.close()
        
    @commands.command(usage="@user")
    async def simpcard(self,ctx, member: discord.Member = None):
        '''Simpcard just for u'''
        member = member or ctx.author
        await ctx.trigger_typing()
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://some-random-api.ml/canvas/simpcard?avatar={member.avatar.with_format("png").url}') as af:
                if 300 > af.status >= 200:
                    fp = BytesIO(await af.read())
                    file = discord.File(fp, "simpcard.png")
                    em = discord.Embed(
                        title="bonk",
                        color=0xf1f1f1,
                    )
                    em.set_image(url="attachment://simpcard.png")
                    await ctx.send(embed=em, file=file)
                else:
                    print(af.status)
                    await ctx.send('No simping :(')
                await session.close()

    @commands.command(usage="@user")
    async def lolice(self,ctx, member: discord.Member = None):
        '''TRY THIS.'''
        member = member or ctx.author
        await ctx.trigger_typing()
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://some-random-api.ml/canvas/lolice?avatar={member.avatar.with_format("png").url}') as af:
                if 300 > af.status >= 200:
                    fp = BytesIO(await af.read())
                    file = discord.File(fp, "lolice.png")
                    em = discord.Embed(
                        title="bonk",
                        color=0xf1f1f1,
                    )
                    em.set_image(url="attachment://lolice.png")
                    await ctx.send(embed=em, file=file)
                else:
                    await ctx.send('No simping :(')
                await session.close()

    @commands.command(aliases=['avatar', 'av'], brief="Get a user's Avatar or Merge Pfps.",usage="@user",name="pfp",help="", extras={"emoji": "🖼"},description="Get a user's Avatar!")
    async def pfp(self, ctx):
        members = ctx.message.mentions
        if members == []:
            members = [ctx.author]
        if len(members) == 1:
            emb = discord.Embed(title="", description=f"", color=0x2e69f2)
            emb.set_image(url=members[0].avatar.url)
            await ctx.send(embed=emb)
            return

        animated = []
        for m in members:
            animated.append(m.avatar.is_animated())

        imgs = []
        for mem in members:
            url = requests.get(mem.avatar.url)
            im = Image.open(BytesIO(url.content))
            imgs.append(im)

        s = len(imgs)
        all_animated = all(animated)
        all_not_animated = not any(animated)
        if all_animated: 
            frames = []

            s = len(imgs)
            print("S", s)
            d = 250
            bg = Image.new(mode="RGBA", size=(d * s, d))

            for gif in imgs:
                f = []
                while True:
                    try:
                        gif.seek(gif.tell() + 1)
                        f.append(gif.copy().resize((d, d)))
                    except Exception as e:
                        frames.append(f)
                        break

            frames_imgs = []
            s = len(frames)
            f_no = 0
            while True:
                i = 0
                brk = False
                bg = Image.new(mode="RGBA", size=(d * s, d))
                for x in range(0, s):
                    try:
                        bg.paste(frames[i][f_no], (d * x, 0))
                        i += 1
                        frames_imgs.append(bg)
                    except Exception as e:
                        print(e, i)
                        brk = True
                f_no += 1
                if brk:
                    break
            # print(frames_imgs)
            if frames_imgs == []:
                frames_imgs = imgs

            # print(frames_imgs)
            frames_imgs[0].save(
                # f"images/generated/{ctx.author.id}.gif",
                # learn to put your generated stuff in a seperated folder and delete them later BRUH! :<
                f"{ctx.author.id}.gif",
                save_all=True,
                append_images=frames_imgs[:],
                loop=0,
                quality=1,
            )
            file = discord.File(
                # f"images/generated/{ctx.author.id}.gif", filename="pic.gif"
                f"{ctx.author.id}.gif", filename="pic.gif"
            )
            emb = discord.Embed(title="", description=f"", color=0x2e69f2)
            emb.set_image(url="attachment://pic.gif")
        else:
            s = len(imgs)
            bg = Image.new(mode="RGBA", size=(500 * s, 500))
            i = 0
            for x in range(0, s):
                try:
                    bg.paste(imgs[i].resize((500, 500)), (500 * x, 0))
                    i += 1
                except Exception as e:
                    print(e, i)
                    pass
            # bg.save(f"images/generated/{ctx.author.id}.png", quality=10)
            bg.save(f"{ctx.author.id}.png", quality=10)
            file = discord.File(
                # f"images/generated/{ctx.author.id}.png", filename="pic.jpg"
                f"{ctx.author.id}.png", filename="pic.jpg"
            )
            emb = discord.Embed(title="", description=f"", color=0x2e69f2)
            emb.set_image(url="attachment://pic.jpg")

        await ctx.send(file=file, embed=emb)

    # @commands.command(aliases=['bn', 'bnr'])
    # async def banner(self, ctx, mem: discord.User = None):
    #     if mem == None:
    #         mem = ctx.author
    #     if mem.banner is None:
    #         return
    #     emb = discord.Embed(color=0x2e69f2)
    #     emb.set_image(url=mem.banner.url)
    #     await ctx.send(embed=emb)

    # @commands.command()
    # async def serverav(self, ctx, mem: discord.User = None):
    #     if mem == None:
    #         mem = ctx.author
    #     if mem.display_avatar is None:
    #         return
    #     emb = discord.Embed(color=0x2e69f2)
    #     emb.set_image(url=mem.display_avatar.url)
    #     await ctx.send(embed=emb)


def setup(bot):
    bot.add_cog(Cards(bot))