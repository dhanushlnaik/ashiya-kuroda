import discord
from discord.ext import commands
import datetime
import time
from random import choice , randint

from database import guilddb

class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name=f"serverinfo",usage="",description="Get Server Info", aliases=["guildinfo"], extras={"emoji": "🤼"})
    async def serverinfo(self, ctx):
        if guilddb.is_channel_blacklisted(ctx.guild.id, ctx.channel.id):
            return
        userSize = len([m for m in ctx.guild.members if not m.bot])
        botSize = len([m for m in ctx.guild.members if m.bot])
        createdAt = ctx.guild.created_at
        emb = discord.Embed(title=f"{ctx.guild.name}", color=discord.Color.random(), description=f"\`👤\` \`Owner\` **- <@{ctx.guild.owner_id}>**\n\`🙂\` \`Members\` **- \`${ctx.guild.member_count}\`**\n\n\`🤖\` \`Bots\` **- \`${botSize}\`**\n\`👋\` \`Users\` **- \`${userSize}\`**\n\n\`🎉\` \`Roles\` **- \`{len(ctx.guild.roles)}\`**\n\`📆\` \`Created\` **- \`${createdAt}\`**")
        emb.set_footer(f"Team Tatsui ❤️")
        emb.set_thumbnail(ctx.guild.icon.url)
        emb.timestamp()
        await ctx.channel.send(embed=emb)

    @commands.command(name=f"botstats",usage="",description="See Bot Stats!", aliases=[], extras={"emoji": "🤖"})
    async def botstats(self, ctx):
        if guilddb.is_channel_blacklisted(ctx.guild.id, ctx.channel.id):
            return
        emb = discord.Embed(title="__Amy Stats__")
        emb.add_field(
            name="Total Servers", value=str(len(self.bot.guilds)), inline=False
        )
        emb.add_field(
            name="Latency(s)", value=str(round(self.bot.latency, 3)), inline=False
        )
        emb.add_field(
            name=f"{ctx.guild} members", value=f"{ctx.guild.member_count}", inline=False
        )
        await ctx.send(embed=emb)
    
    @commands.command(name=f"server",usage="",description="Gives Support Server Link.", aliases=["support", "supportserver"], extras={"emoji": "💫"})
    async def server(self, ctx):
        if guilddb.is_channel_blacklisted(ctx.guild.id, ctx.channel.id):
            return
        await ctx.send(f"__Support Server__:\n https://discord.gg/eZFKMmS6vz ")

    @commands.command(name=f"ping",usage="",description="Check Ping.", aliases=["lag", "pong"], extras={"emoji": "🏓"})
    async def ping(self,ctx):
        if round(self.bot.latency * 1000) <= 50:
            embed=discord.Embed(title="PING", description=f":ping_pong: Pingpingpingpingping! The ping is **{round(self.bot.latency *1000)}** milliseconds!", color=0x44ff44)
        elif round(self.bot.latency * 1000) <= 100:
            embed=discord.Embed(title="PING", description=f":ping_pong: Pingpingpingpingping! The ping is **{round(self.bot.latency *1000)}** milliseconds!", color=0xffd000)
        elif round(self.bot.latency * 1000) <= 200:
            embed=discord.Embed(title="PING", description=f":ping_pong: Pingpingpingpingping! The ping is **{round(self.bot.latency *1000)}** milliseconds!", color=0xff6600)
        else:
            embed=discord.Embed(title="PING", description=f":ping_pong: Pingpingpingpingping! The ping is **{round(self.bot.latency *1000)}** milliseconds!", color=0x990000)
        await ctx.send(embed=embed)
    

    @commands.command(name=f"github",usage="",description="Gives Github Repo Link.", aliases=[], extras={"emoji": "👩‍💻"})
    async def github(self, ctx):
        if guilddb.is_channel_blacklisted(ctx.guild.id, ctx.channel.id):
            return
        await ctx.reply(f"Repo Link :-https://github.com/dhanushlnaik/Amy-Sensei ")


    @commands.command(name=f"invite",usage="",description="Invite the Bot.", aliases=[], extras={"emoji": "💌"})
    async def invite(self,ctx):
        emb = discord.Embed( description=f" [Click here](https://discord.com/api/oauth2/authorize?client_id=850243448724127754&permissions=939838544&scope=bot) to invite me :))")
        await ctx.send(embed=emb)

    @commands.command(name=f"upvote",usage="",description="Upvote the Bot.", aliases=[], extras={"emoji": "👆"})
    async def upvote(self,ctx):
        emb = discord.Embed( description=f" [Click here](https://top.gg/bot/850243448724127754/vote) to upvote me :))")
        emb.set_footer(icon_url=self.bot.user.avatar.url, text=f"UwU")
        await ctx.send(embed=emb)

    @commands.command(name="userinfo",usage="",description="Get a User's Info.", aliases=["whois"], extras={"emoji": "❓"})
    async def userinfo(self, ctx, member: discord.Member=None):
        if guilddb.is_channel_blacklisted(ctx.guild.id, ctx.channel.id):
            return
        if member is None:
            member = ctx.author
        created_at = member.created_at.strftime("%b %d, %Y")
        joined_at = member.joined_at.strftime("%b %d, %Y")
        rolesMention = [role.mention for role in member.roles]
        rolesMention.pop(0)
        rolesMention.reverse()
        noPermList =  ['Create Instant Invite',  'Add Reactions',  'Priority Speaker', 'Stream', 'Read Messages', 'Send Messages', 'Send TTS Messages', 'Embed Links', 'Attach Files', 'Read Message History', 'Connect', 'Speak',  'Use Voice Activation',  'Use Slash Commands', 'Request To Speak']
        permList = [p[0].replace('_',' ').replace('guild', 'server').title().replace('Tts','TTS') for p in member.guild_permissions if p[1]]
        
        for perm in noPermList:
            if perm in permList:
                permList.remove(perm)
        admin = False
        mod = False
        manager = False
        memberA=False
        if  "Administrator" in permList:
            admin = True
        elif "Manage Server" in permList:
            manager = True
        elif "Mute Members" in permList:
            mod = True
        else:
            memberA = True
        text=', '.join(permList)
        
        embed = discord.Embed(description=f"{member.mention} `[{member.id}]`", color=ctx.author.color)
        embed.add_field(name="\`📆\` \`Created\`", value=f"**- \`{created_at}\`**\n\n\`")
        embed.add_field(name="\`📅\` \`Joined\`", value=f"**- \`{joined_at}\`**\n\n\`")
        if member.avatar.is_animated():
            embed.add_field(name="\`📱\` \`Avatar\`", value=f"[Animated]({member.avatar.url})", inline=False)
        if not member.avatar.is_animated():
            embed.add_field(name="\`📱\` \`Avatar\`", value=f"[Non-Animated]({member.avatar.url})", inline=False)
        embed.add_field(name=f"\`ℹ\` \`Roles [{len(rolesMention)}]\`", value=" ".join(rolesMention), inline=False)
        if not memberA:
            embed.add_field(name="\`📱\` \`Key Permissions\`", value=text, inline=False)
        if admin:
            embed.add_field(name="\`📱\` \`Acknowledgements\`", value="**- \`Server Admin\`**\n\n\`", inline=False)
        if manager:
            embed.add_field(name="\`📱\` \`Acknowledgements\`", value="**- \`Server Manager\`**\n\n\`", inline=False)
        if mod:
            embed.add_field(name="\`📱\` \`Acknowledgements\`", value="**- \`Server Moderator\`**\n\n\`", inline=False)
        embed.set_author(icon_url=ctx.author.avatar.url, name=ctx.author)
        embed.set_thumbnail(url=member.avatar.url)
        embed.set_footer("Team Tatsui ❤️")
        embed.timestamp =  datetime.datetime.utcnow()
        await ctx.send(embed=embed)
        

def setup(bot):
    bot.add_cog(Misc(bot))