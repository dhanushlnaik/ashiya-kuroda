
from os import name
import discord
from discord import Color , Embed
from discord.ext import commands
from random import *
from discord.types.embed import EmbedAuthor
from database import guilddb
from discord.ui import Button, View

def checkcom(bot, command):
    for commands in bot.walk_commands():
        if commands.name.lower() == command.lower():
            return True
        else:
            return False
options = [
            discord.SelectOption(
                label="Basic", description="Basic Commands.", emoji=discord.PartialEmoji(name="amyShy3", id="864133590178070559")
            ),
            discord.SelectOption(
                label="Anime", description="Anime Related Commands.", emoji=discord.PartialEmoji(name="amyitsok", id="863680733201170432")
            ),
            discord.SelectOption(
                label="Actions", description="Action/Roleplay Related Commands.", emoji=discord.PartialEmoji(name="amyStare", id="864133208961581106")
            ),
            discord.SelectOption(
                label="Family", description="Family Commands.", emoji=discord.PartialEmoji(name="amyBed", id="863681197577601024")
            ),
            discord.SelectOption(
                label="Fun", description="Fun/Game Commands", emoji=discord.PartialEmoji(name="amyBunny", id="864133407499092028")
            ),
            discord.SelectOption(
                label="Image", description="Image Manipulation.", emoji=discord.PartialEmoji(name="amyChibiOk", id="863681774550515722")
            ),
            discord.SelectOption(
                label="Misc", description="Miscellaneous Commands,", emoji=discord.PartialEmoji(name="amyBlush", id="898532188813950986")
            ),
        ]

class HelpD(View):
    def __init__(self, bot, user):
        super().__init__()
        self.timeout = 180
        self.bot = bot
        self.user =user
        


    @discord.ui.select(placeholder="Choose an option.",min_values=1,max_values=1,options=options)
    async def callback(self,selection : discord.ui.Select , interaction: discord.Interaction):
        user1 = interaction.user.id
        if self.user.id == user1:
            
            emb = discord.Embed(color=self.user.color,title=f"Help - {selection.values[0]}")
            emb.set_thumbnail(url=self.bot.user.avatar.url)
            emb.set_author(name=f"{self.bot.user.name} - Help", icon_url=self.bot.user.avatar.url)
            prefix = guilddb.check_prefix(interaction.guild.id)
            desc = f""
            n = 1
            for command in self.bot.walk_commands():

                if command.cog_name is None:
                    pass
                elif command.cog_name.lower() == selection.values[0].lower():
                    desc += f"`[{n}] {prefix}{command.name}` - {command.description}\n"
                    n += 1
            emb.add_field(name=f"Command:", value=desc)
            emb.set_footer(text="Team Tatsui ❤️")
            msg1 = await interaction.response.edit_message(embed=emb)
            
        else:
            return

class Help(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(name=f"help",aliases=[], brief="Get Bot's Command.",usage="<command/cog_name>",description="Get Bot's Command.")
    async def help(self, ctx: commands.Context, input=None):
        prefix = guilddb.check_prefix(ctx.guild.id)
        version = "2.0.1"
        owner = 624174437821972480

        if input is None:
            try:
                owner = ctx.guild.get_member(owner).mention

            except AttributeError as e:
                owner = owner
            emb = discord.Embed(color=ctx.author.color,description=f"These Are the Available Commands For Amy-San\nBot's Global Prefix Is - `amy`\n Server Prefix Is - `{prefix}`\nUse `{prefix}help <module>` to gain more information about that module.\n")
            emb.set_thumbnail(url=ctx.author.avatar.url)
            emb.set_author(name=f"{self.bot.user.name} - Help", icon_url=self.bot.user.avatar.url)
            family_desc =''
            fun_desc=''
            misc_desc=''
            anime_desc=''
            imagM_desc=''
            action_desc=''
            basic_desc=''
            

            for command in self.bot.walk_commands():
                if command.cog_name is None:
                    pass

                if command.cog_name == "Basic" and not command.hidden:
                    basic_desc += f'`{command.name}` | '

                elif command.cog_name == "Anime" and not command.hidden:
                    anime_desc += f'`{command.name}` | '

                elif command.cog_name == "Actions" and not command.hidden:
                    action_desc += f'`{command.name}` | '

                elif command.cog_name == "Family" and not command.hidden:
                    family_desc += f'`{command.name}` | '

                elif command.cog_name == "Fun" and not command.hidden:
                    fun_desc += f'`{command.name}` | '

                elif command.cog_name == "ImageM" and not command.hidden:
                    imagM_desc += f'`{command.name}` | '

                elif command.cog_name == "Misc" and not command.hidden:
                    misc_desc += f'`{command.name}` | '

                else : pass
            if basic_desc:
                emb.add_field(name=f"__Basic__", value=f"{basic_desc}", inline=False)
            if anime_desc:
                emb.add_field(name=f"__Anime__", value=f"{anime_desc}", inline=False)
            if action_desc:
                emb.add_field(name=f"__Action__", value=f"{action_desc}", inline=False)
            if family_desc:
                emb.add_field(name=f"__Family__", value=f"{family_desc}", inline=False)
            if imagM_desc:
                emb.add_field(name=f"__Fun__", value=f"{imagM_desc}", inline=False)
            if fun_desc:
                emb.add_field(name=f"__Image__", value=f"{fun_desc}", inline=False)
            if misc_desc:
                emb.add_field(name=f"__Misc__", value=f"{misc_desc}", inline=False)

            emb.add_field(name="__About__", value=f"The Bots is developed by Dhanush#6875.\nPlease visit https://github.com/dhanushlnaik/Amy-Sensei to submit ideas or bugs.")
            emb.set_footer(text=f"Bot is running {version}")
        
        elif input.lower() in self.bot.cogs:
            for cog in self.bot.cogs:
                if cog.lower() == input.lower():
                    emb = discord.Embed(title=f'{cog} - Commands', description=self.bot.cogs[cog].__doc__,
                                        color=discord.Color.green())

                    for command in self.bot.get_cog(cog).get_commands():
                        if not command.hidden:
                            emb.add_field(name=f"`{prefix}{command.name}`", value=f"{command.description or command.help or command.brief}", inline=False)
                            
                    break
        
        elif checkcom(self.bot, input):
            for command in self.bot.walk_commands():
                if command.name.lower() == input.lower():
                    emb = discord.Embed(description=f"{command.description}",color=discord.Color.blurple())
                    emb.add_field(name=f"Usage", value=f"{command.usage}")
                    emb.add_field(name=f"Aliases", value=f"{prefix}{command.aliases}{command.callback}")
        
        else:
            print(self.bot.commands)
            emb = discord.Embed(title="What's that?!",description=f"I've never heard from a module called `{input}` before :scream:",color=discord.Color.orange())

        view = HelpD(self.bot, ctx.author)
        msg = await ctx.channel.send(embed=emb, view=view)
        try:
            await view.wait()        
            a = await view.on_timeout()
            await msg.edit(view=None)

        except Exception as err:
            print(err)


def setup(bot):
    bot.add_cog(Help(bot))