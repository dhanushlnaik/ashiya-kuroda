import discord
from discord.ext import commands
import requests
import json
from dotenv import load_dotenv
import os
from database import guilddb
from os import name
import asyncio
from disputils import BotEmbedPaginator
import time


load_dotenv()
API_KEY = os.environ.get("WEEBY_API_KEY")


class Basic(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot


    @commands.command()
    async def afk(self, ctx, *, message=None):
        """Set an AFK status to display when you are mentioned."""
        if message == None:
            message = "AFK"
        nick = ctx.author.display_name
        new_nick = "[AFK] " + nick
        try:
            await ctx.author.edit(nick = new_nick)
            await asyncio.sleep(2)
            guilddb.afcreate(ctx.author.id, ctx.guild.id, message)
            await ctx.reply(f"`{ctx.author.name}` your AFK has been set: {message}")
        except Exception:
            guilddb.afcreate(ctx.author.id, ctx.guild.id, message)
            await ctx.reply(f"`{ctx.author.name}` your AFK has been set: {message}")
        
        
    @commands.Cog.listener()
    async def on_message(self, message):
        if guilddb.checkafk(message.author.id, message.guild.id):
            ping = guilddb.get_ping(message.author.id, message.guild.id)
            await message.reply(f"Welcome back! your AFK has been removed\nYou were pinged {ping} times! ", delete_after=15)
            guilddb.remove_afk(message.author.id, message.guild.id)
            new_nick = message.author.display_name.strip("[AFK]")
            await message.author.edit(nick=new_nick)
        for mention in message.mentions:
            if guilddb.checkafk(mention.id, message.guild.id):
                if message.author.bot:
                    return
                else:
                    note = guilddb.get_afk_message(mention.id, message.guild.id)
                    await message.reply(
                    f"`{mention}` is AFK: **{note}**", delete_after=15)
                    guilddb.add_ping(mention.id, message.guild.id)

    @commands.command(name=f"enlarge",aliases=["jumbo"], brief="Enlarge an emoji!",usage=" <emoji>",description="Enlarge an emoji!")
    async def enlarge(self, ctx, *, content):
        cont = content.split()
        embeds = []
        for word in cont:
            if word.startswith("<") and word.endswith(">"):
                lst = word.strip("<:a>").split(":")
                if word.startswith("<a:"):
                    emoj = discord.PartialEmoji(name=lst[0], id=lst[1], animated=True)
                else:
                    emoj = discord.PartialEmoji(name=lst[0], id=lst[1])
                asset = emoj.url
                emb = discord.Embed(description=f"`{lst[1]}`\n`{lst[0]}`", color=0x2e69f2)
                emb.set_author(
                    name="Enlarged Emotes!",
                    icon_url=ctx.author.avatar.url
                )
                emb.set_image(url=str(asset))
                embeds.append(emb)
        paginator = BotEmbedPaginator(ctx, embeds, control_emojis=("⏮", "◀", "▶", "⏭"))
        await paginator.run()

    # @commands.command()
    # async def blacklist(self, ctx, channel=None):
    #     if channel is None:
    #         channel = ctx.channel
    #     emb = discord.Embed



def setup(bot):
    bot.add_cog(Basic(bot))
    