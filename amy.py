import datetime
import os
import discord
from discord.ext import commands
import traceback
from database import userdb, guilddb
import random
import asyncio
from random import choice
from dotenv import load_dotenv
from tools import check_img

load_dotenv()
TOKEN = os.environ.get("TOKEN")
DEFAULT_PREFIX = "a!"
ownerID = ["624174437821972480", "710852927543050292"]

def user_is_me(ctx):
    if str(ctx.message.author.id) in ownerID:
        return True
    else:
        return False

async def prefix_get(bot, message):
    if not message.guild:
        return commands.when_mentioned_or(DEFAULT_PREFIX)(bot, message)
    prefix = guilddb.check_prefix(message.guild.id)
    return commands.when_mentioned_or(prefix,"a!")(bot, message)
                      
# Bot Variables
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix= prefix_get , case_insensitive=True, intents=intents, allowed_mentions=discord.AllowedMentions(everyone=False,users=True,roles=False,replied_user=True))
bot.remove_command("help")

# Load & Unload Cog Functions
def unload_cogs():
    for file in os.listdir("./cogs"):
        if file.endswith(".py") and not file.startswith("_"):
            try:
                bot.unload_extension(f"cogs.{file[:-3]}")
            except Exception as e:
                print(f"COG UNLOAD ERROR : {e}")


def load_cogs():
    print("Loading...")
    for file in os.listdir("./cogs"):
        if file.endswith(".py") and not file.startswith("_"):
             
            try:
                bot.load_extension(f"cogs.{file[:-3]}")
                print(f'> Loaded cog: {file[:-3]}'.title())
            except Exception as e:
                print(f"COG LOAD ERROR : {e}\n\n{traceback.format_exc()}\n\n")


@bot.command(aliases=["reload"], hidden=True)
@commands.check(user_is_me)
async def reloadcogs(ctx):

    unload_cogs()
    load_cogs()
    await ctx.reply("All Cogs Reloaded!")

async def switchpresence():
    await bot.wait_until_ready()
    statuses = ["Actually Stalking brr", "Tatsuya <3", f"{len(bot.guilds)} servers !", "Kakarot", "My Friends Suffer ! hehe", "K-Drama (Checkmate Weebs)"]
    while not bot.is_closed():
        status = random.choice(statuses)

        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=status))
        await asyncio.sleep(10)

@bot.event
async def on_ready():
    print(f"Logged in as : {bot.user.name}\nID : {bot.user.id}")
    print(f"Total Servers : {len(bot.guilds)}\n")

    load_cogs()
    print("Bot is ready to roll out\n")


@bot.command(hidden=True)                                                                                                                                            
@commands.check(user_is_me)
async def servername(ctx):
    activeservers = bot.guilds                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
    desc=""
    n=0
    for guild in activeservers:
        n +=1
        desc += f"[{n}] {guild.name}\n"
    await ctx.send(f"`{desc}`")
   
@bot.command(aliases=['pre', 'setprefix', 'change_prefix'], brief="Get or set the command prefix for this server.",usage="",name="Prefix",help="", extras={"emoji": "🔧"},description="Get or set the command prefix for this server.", cog_name=f"Misc")
@commands.cooldown(rate=1, per=5, type=commands.BucketType.default)
async def prefix(ctx, newpre:str=None):
    if newpre is None:
        await ctx.channel.send(f"My prefix is  `{guilddb.check_prefix(ctx.guild.id)}`")
        return
    else: 
        if ctx.message.author.guild_permissions.administrator:
            guilddb.add_prefix(ctx.guild.id, newpre)
            emb = discord.Embed(color=discord.Color.green())
            emb.set_author(name=f"Changed server prefix to `{guilddb.check_prefix(ctx.guild.id)}`", icon_url="https://firebasestorage.googleapis.com/v0/b/aiko-mizuki.appspot.com/o/PicsArt_11-25-04.04.58.png?alt=media&token=5898ba72-63bc-4f12-aeb4-ee9ff22a9526")
            await ctx.channel.send(embed=emb)
            return
        else:
            emb = discord.Embed(color=discord.Color.red())
            emb.set_author(name=f"❌ You don't have required Permissions to use this Command!")
            await ctx.channel.send(embed=emb)
            return


@bot.event
async def on_command_error(ctx, error): 
        

    if isinstance(error, commands.MissingPermissions): 
        err = f"You are missing the required permissions to run this command!"
        emb = discord.Embed(title=f"", color=discord.Color.red(),description=f"```{err}```")
        emb.set_author(name=f"Uh Oh!", icon_url=check_img(bot.user))
        emb.timestamp = datetime.datetime.utcnow()
        emb.set_footer(text="Amy Devs 🌺", icon_url=check_img(bot.user))
        await ctx.channel.send(embed=emb)
        print(error)

    elif isinstance(error, commands.MissingRequiredArgument): 
        err = f"Missing a required argument: {error.param}"
        emb = discord.Embed(title=f"", color=discord.Color.red(),description=f"```{err}```")
        emb.set_author(name=f"Uh Oh!", icon_url=check_img(bot.user))
        emb.timestamp = datetime.datetime.utcnow()
        emb.set_footer(text="Amy Devs 🌺", icon_url=check_img(bot.user))
        await ctx.channel.send(embed=emb)
        print(error)
        
    elif isinstance(error, commands.CommandOnCooldown):
        err = f"This command is on cooldown. Please try again after {round(error.retry_after, 1)} seconds."
        emb = discord.Embed(title=f"", color=discord.Color.red(),description=f"```{err}```")
        emb.set_author(name=f"Uh Oh!", icon_url=check_img(bot.user))
        emb.timestamp = datetime.datetime.utcnow()
        emb.set_footer(text="Amy Devs 🌺", icon_url=check_img(bot.user))
        await ctx.channel.send(embed=emb)
        print(error)

    elif isinstance(error, commands.MissingRequiredArgument):
        err = f"Missing a required argument: {error.param}"
        emb = discord.Embed(title=f"", color=discord.Color.red(),description=f"```{err}```")
        emb.set_author(name=f"Uh Oh!", icon_url=check_img(bot.user))
        emb.timestamp = datetime.datetime.utcnow()
        emb.set_footer(text="Amy Devs 🌺", icon_url=check_img(bot.user))
        await ctx.channel.send(embed=emb)
        print(error)

    elif isinstance(error, commands.ConversionError):
        err = (str(error))
        emb = discord.Embed(title=f"", color=discord.Color.red(),description=f"```{err}```")
        emb.set_author(name=f"Uh Oh!", icon_url=check_img(bot.user))
        emb.timestamp = datetime.datetime.utcnow()
        emb.set_footer(text="Amy Devs 🌺", icon_url=check_img(bot.user))
        await ctx.channel.send(embed=emb)
        print(error)

    elif isinstance(error, commands.CommandNotFound):
        err = (str(error))
        emb = discord.Embed(title=f"", color=discord.Color.red(),description=f"```{err}```")
        emb.set_author(name=f"Uh Oh!", icon_url=check_img(bot.user))
        emb.timestamp = datetime.datetime.utcnow()
        emb.set_footer(text="Amy Devs 🌺", icon_url=check_img(bot.user))
        await ctx.channel.send(embed=emb)
        print(error)

    else:
        print(error)
        # emb = discord.Embed(title=f"", color=discord.Color.red(),description="An issue has occured while running the command. If this error keeps occuring please contact our development team.")
        # emb.set_author(name=f"Uh Oh!", icon_url=check_img(bot.user))
        # emb.timestamp = datetime.datetime.utcnow()
        # emb.set_footer(text="Amy Devs 🌺", icon_url=check_img(bot.user))
        # await ctx.channel.send(embed=emb)

bot.loop.create_task(switchpresence())
bot.run(TOKEN)


