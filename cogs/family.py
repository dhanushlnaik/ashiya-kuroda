from datetime import datetime ,date
from os import set_inheritable
import discord
from discord.ext import commands
from database import guilddb, userdb
from discord.ui import Button, View
import asyncio

options = [
            discord.SelectOption(
                label="Partner", description="Check your Marital Status.", emoji=discord.PartialEmoji(name="amyChibiILY", id="863681666673147914")
            ),
            discord.SelectOption(
                label="Siblings", description="Check Your Siblings.", emoji=discord.PartialEmoji(name="amyBlush", id="898532188813950986")
            )
        ]

class FamilyOption(View):
    def __init__(self, bot, user):
        super().__init__()
        self.timeout = 180
        self.bot = bot
        self.user =user
        
    @discord.ui.select(placeholder="Choose an option.",min_values=1,max_values=1,options=options)
    async def callback(self,selection : discord.ui.Select , interaction: discord.Interaction):
        user1 = interaction.user.id
        if self.user.id:
            prefix = guilddb.check_prefix(interaction.guild.id)
            desc = f""
            if selection.values[0].lower() == "siblings":
                sib = userdb.getsiblings(self.user.id).split(",")
                rel = userdb.getsiblings(self.user.id)
                
                if str(rel) == "0":
                    desc = "You have no E-siblings!"
                    lensib = "0"
                elif len(sib) == 1:
                    ppl = discord.utils.get(self.bot.get_all_members(), id=int(rel))
                    desc= f"`[1] {ppl.name}`"
                    lensib=f"{len(sib)}"
                else:
                    for a in range(len(sib)):
                        lensib = len(sib)
                        try:
                            print(sib[a])
                            ppl = discord.utils.get(self.bot.get_all_members(), id=int(sib[a]))
                            desc = desc + f"`[{a+1}] {ppl.name}` | "
                        except Exception as e:
                            print(e)
                embed=discord.Embed(color=self.user.color,description=f"** Siblings[{lensib}] :**\n{desc}")
                embed.set_author(name=f"{self.user.name}'s Siblings", icon_url=self.user.avatar.url)
                embed.timestamp = datetime.utcnow()
                embed.set_footer(icon_url=self.bot.user.avatar.url,text="Team Tatsui ❤️")
                embed.set_image(url="https://giffiles.alphacoders.com/113/113317.gif")
                msg1 = await interaction.response.edit_message(embed=embed)
            else:
                partner = int(userdb.getpartnervar(self.user.id,"ID"))

                if partner == 0:
                    emb = discord.Embed(description=f"{self.user.name}, you are not married! Please Marry Someone First! \n Usage : `{prefix}marry @user`")
                    emb.set_author(name=f"You are not currently married.", icon_url=self.user.avatar.url)
                    msg1 = await interaction.response.edit_message(embed=emb)
                    return

                else:
                    some = userdb.getpartnervar(self.user.id, "DATE")
                    today = datetime.today()
                    dat = userdb.getpartnervar(self.user.id, "DAY")
                    someday = datetime.strptime(some ,'%Y-%m-%d')
                    diff = today - someday
                    prsn = discord.utils.get(self.bot.get_all_members(), id = partner)
                    emb = discord.Embed(description=f"Married since {dat} ({diff.days} days) ! The Perfect Cuple <3 UwU", color=discord.Color.random())
                    emb.set_author(name=f"{self.user.name}, you are happily married to {prsn.name}", icon_url=self.user.avatar.url)
                    emb.set_thumbnail(url=f"https://i.gifer.com/ZdPB.gif")
                    emb.set_footer(text="Team Tatsui ❤️")
            
                    emb.set_image(url="https://giffiles.alphacoders.com/113/113317.gif")
                    msg1 = await interaction.response.edit_message(embed=emb)
                    return
        else:
            return

class MarryButton(View):
    def __init__(self, user:discord.User):
        super().__init__()
        self.value = None
        self.user= user

    @discord.ui.button(style=discord.ButtonStyle.success, emoji="<:amyYes:913690556452974592>", label="Yes !!")
    async def yesButton(
        self, button: Button, interaction: discord.Interaction
    ):
        user1 = interaction.user.id
        if self.user.id == user1:
            # await interaction.response.send_message("Confirming", ephemeral=True)
            self.value = True
            self.stop()
        else:
            return


    # This one is similar to the confirmation button except sets the inner value to `False`
    @discord.ui.button(style=discord.ButtonStyle.danger, emoji="<:pepe_no:848275072435224586>", label="No ;-;")
    async def cancel(self, button: Button, interaction: discord.Interaction):
        user1 = interaction.user.id
        if self.user.id == user1:
            # await interaction.response.send_message("Confirming", ephemeral=True)
            self.value = False
            self.stop()
        else:
            return


class Family(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(usage="@user",description="Marry another user !", aliases=["propose", "marrriage", "waifu", "wife", "husbando", "husband"], extras={"emoji": "💒"}, brief="Marry another user !")
    async def marry(self, ctx, user: discord.Member=None):

        
        prefix = guilddb.check_prefix(ctx.guild.id)

        if user is None:
            partner = int(userdb.getpartnervar(ctx.author.id,"ID"))

            if partner == 0:
                emb = discord.Embed(description=f"{ctx.author.name}, you are not married! Please Marry Someone First! \n Usage : `{prefix}marry @user`")
                emb.set_author(name=f"You are not currently married.", icon_url=ctx.author.avatar.url)
                await ctx.channel.send(embed=emb)
                return

            else:
                some = userdb.getpartnervar(ctx.author.id, "DATE")
                today = datetime.today()
                dat = userdb.getpartnervar(ctx.author.id, "DAY")
                someday = datetime.strptime(some ,'%Y-%m-%d')
                diff = today - someday
                prsn = discord.utils.get(self.bot.get_all_members(), id = partner)
                emb = discord.Embed(description=f"Married since {dat} ({diff.days} days) ! The Perfect Cuple <3 UwU", color=discord.Color.random())
                emb.set_author(name=f"{ctx.author.name}, you are happily married to {prsn.name}", icon_url=ctx.author.avatar.url)
                emb.set_thumbnail(url=f"https://i.gifer.com/ZdPB.gif")
                emb.set_footer(text="Team Tatsui ❤️")
                await ctx.channel.send(embed=emb)
                return
        
        elif not user.bot:
            if ctx.author.id == user.id:
                emb = discord.Embed(title=f"", color=discord.Color.red(), description=f"> You Can't Marry Yourself Dumbo!\n**__Usage__:**\n`{prefix}marry @user`")
                emb.set_author(name=f"Sheesh!", icon_url=ctx.author.avatar.url)
                emb.set_image(url="https://firebasestorage.googleapis.com/v0/b/amy-sensei-37a68.appspot.com/o/self.gif?alt=media&token=418caded-3a40-463b-a294-9ba5ff939587")
                emb.timestamp = datetime.utcnow()
                emb.set_footer(text="Team Tatsui ❤️")
                await ctx.channel.send(embed=emb)
                return
            
            if userdb.is_sibling(ctx.author.id, user.id):
                emb = discord.Embed(title=f"", color=discord.Color.red(), description=f"> You Can't Marry Your Sibling !!\nI mean u can- But my dev won't allow it.\n**__Usage__:**\n`{prefix}marry @user`")
                emb.set_author(name=f"Wha-! You Wanna Marry Your Sibling?", icon_url=ctx.author.avatar.url)
                emb.timestamp = datetime.utcnow()
                emb.set_footer(text="Team Tatsui ❤️")
                emb.set_image(url="https://firebasestorage.googleapis.com/v0/b/amy-sensei-37a68.appspot.com/o/mom.png?alt=media&token=61eb7d6d-92e3-48a0-a5a1-40e74ca00cad")
                await ctx.channel.send(embed=emb)
                return
                
            prsn1 = int(userdb.getpartnervar(ctx.author.id, "ID"))
            prsn2 = int(userdb.getpartnervar(user.id, "ID"))
            if prsn1 == 0 and prsn2 == 0:
                emb = discord.Embed(description=f"Hey, {user.mention}, it would make {ctx.author.mention} really happy if you would marry them. What do you say?\n", color=discord.Color.random())
                emb.set_author(name=f"{ctx.author.name} has proposed to {user.name}! <3 ")
                emb.timestamp = datetime.utcnow()

                btn1 = Button(style=discord.ButtonStyle.success, emoji="<:amyYes:913690556452974592>", label="Yes !!")
                btn2 = Button(style=discord.ButtonStyle.danger, emoji="<:pepe_no:848275072435224586>", label="No ;-;")

                btn3= Button(style=discord.ButtonStyle.blurple, emoji="<:amySad1:913697522474704916>", label="timeup", disabled=True)

                view = MarryButton(user)


                msg = await ctx.channel.send(embed=emb, view=view)
                try:
                    await view.wait()
                    if view.value is None:

                        view2= View()
                        view2.add_item(btn3)
                        await msg.edit(view=view2)
                        await ctx.send(f"😠 || Sorry, {ctx.author.mention}, {user.name} didn't reply on time!! Maybe They are confused, lets give them some time!")

                    elif view.value:
                        view2= View()
                        view2.add_item(btn3)
                        await msg.edit(view2)
                        await ctx.send(f"💒 || {ctx.author.mention} and {user.mention} are now married! Congrats!!|")
                        userdb.add_partnervar(user.id, "ID",str(ctx.author.id))
                        userdb.add_partnervar(ctx.author.id, "ID",str(user.id))
                        userdb.add_time(int(user.id))
                        userdb.add_time(int(ctx.author.id))
                        return
                    else:
                        view2= View()
                        view2.add_item(btn3)
                        view2= View()
                        await msg.edit(view=view2)
                        await ctx.send(f"💔 || {user.mention}, you have decline a marriage request to {ctx.author.mention}")
                        return

                except Exception as err:
                    view2= View()
                    view2.add_item(btn3)
                    await msg.edit(view=view2)
                    await ctx.send(f"😠 || Sorry, {ctx.author.mention}, {user.name} didn't reply on time!! Maybe They are confused, lets give them some time!")
                    return err
            elif prsn1 != 0 and prsn2==0 or  prsn1 == 0 and prsn2!=0 or prsn1 != 0 and prsn2 !=0:
                await ctx.reply(f":no_entry_sign: | **{ctx.author.name}** , you or your friend is already married!")
                return
            else:
                return

    @commands.command(usage="",description="Take a Divorce!", aliases=["divorce", "unmarry", "unwaifu", "unwife", "unhusbando", "unhusband"], extras={"emoji": "❌"}, brief="Take a Divorce!")
    async def div(self,ctx):

        
        prefix = guilddb.check_prefix(ctx.guild.id)
        partner = int(userdb.getpartnervar(ctx.author.id,"ID"))

        if partner == 0:
            await ctx.reply(f":no_entry_sign: | {ctx.author.mention}, you can't divorce if you aren't married!")
            return
        else:
            try:
                ppl = discord.utils.get(self.bot.get_all_members(), id=partner)
                some = userdb.getpartnervar(ctx.author.id, "DATE")
                today = datetime.today()
                dat = userdb.getpartnervar(ctx.author.id, "DAY")
                someday = datetime.strptime(some ,'%Y-%m-%d')
                diff = today - someday
                
                emb=discord.Embed(description=f"You married on {dat} and have been married for {diff.days} days... Once you divorce, the ring will break and disappear.")
                emb.set_author(name=f"{ctx.author.name}, are you sure you want to divorce {ppl.name}?", icon_url=ctx.author.avatar.url)
                emb.set_thumbnail(url="https://i.gifer.com/ZdPB.gif")
                view = MarryButton(ctx.author)


                msg = await ctx.channel.send(embed=emb, view=view)
                try:
                    await view.wait()
                    if view.value is None:

                        view2= View()
                        btn3= Button(style=discord.ButtonStyle.blurple, emoji="<:amySad1:913697522474704916>", label="timeup", disabled=True)
                        view2.add_item(btn3)
                        await msg.edit(view=view2)
                        await ctx.send(f"😠 || Sorry, {ctx.author.mention} you didn't reply on time!!")

                    elif view.value:
                        view2= View()
                        btn3= Button(style=discord.ButtonStyle.blurple, emoji="<:amySad1:913697522474704916>", label="timeup", disabled=True)
                        view2.add_item(btn3)
                        await msg.edit(view2)
                        await ctx.send(f":broken_heart:  || {ctx.author.mention}, You have decided to divorce.")
                        userdb.remv_partner(int(ctx.author.id), "ID")
                        userdb.remv_partner(int(ctx.author.id), "DAY")
                        userdb.remv_partner(int(ctx.author.id), "DATE")
                        userdb.remv_partner(int(ppl.id), "ID")
                        userdb.remv_partner(int(ppl.id), "DAY")
                        userdb.remv_partner(int(ppl.id), "DATE")
                        
                        return
                    else:
                        view2= View()
                        btn3= Button(style=discord.ButtonStyle.blurple, emoji="<:amySad1:913697522474704916>", label="timeup", disabled=True)
                        await msg.edit(view=view2)
                        await ctx.send(f"👍 || {ctx.author.mention},You have declined to divorce.")
                        return

                except asyncio.TimeoutError:
                    view2= View()
                    btn3= Button(style=discord.ButtonStyle.blurple, emoji="<:amySad1:913697522474704916>", label="timeup", disabled=True)
                    await msg.edit(view=view2)
                    await ctx.send(f"😠 || Sorry, {ctx.author.mention} you didn't reply on time!!")
                    return
            except:
                return

    @commands.command(usage="@user",description="Make someone your Sibling", aliases=["rakhi", "sib", "bro", "sis"], extras={"emoji": "❌"}, brief="Take a Divorce!")
    async def sibling(self, ctx, user: discord.Member=None):

        prefix = guilddb.check_prefix(ctx.guild.id)
        if user == None:
            rel = userdb.getsiblings(ctx.author.id)
            sib = rel.split(",")
            desc = ""
            if rel == "0":
                emb=discord.Embed(description=f"{ctx.author.name}, You have no E-siblings right now! Please make Someone First! ex. `{prefix}sib @user` ", color=discord.Color.random())
                emb.set_author(name="Lonely Soul", icon_url=ctx.author.avatar.url)
                emb.set_thumbnail(url="https://i.pinimg.com/originals/b3/8e/27/b38e27402bc8accd4e9b313a1b567fa6.gif")
                await ctx.send(embed=emb)
                return
            if len(sib) == 1:
                ppl = discord.utils.get(self.bot.get_all_members(), id=int(rel))
                emb=discord.Embed(description=f"▪️ {ppl.name} `({ppl.id})`", color=discord.Color.random())
                emb.set_author(name=f"{ctx.author.name}, you have {len(sib)} Siblings : ", icon_url=ctx.author.avatar.url)
                emb.set_thumbnail(url="https://4.bp.blogspot.com/-T2bVs6xiUks/XHeLMCZlvOI/AAAAAAAUQDU/k-8YrZmX5j4S9VOaOULzqtExdduBcfPtQCLcBGAs/s1600/AW3567431_10.gif")
                emb.timestamp = datetime.utcnow()
                emb.set_footer(icon_url=self.bot.user.avatar.url)
                await ctx.send(embed=emb)
                return
            else:
                for a in range(len(sib)):
                    try:
                        ppl = discord.utils.get(self.bot.get_all_members(), id=int(sib[a]))
                        desc = desc + f"`[{a+1}] {ppl.name}` | "
                    except Exception as e:
                        print(e)

                emb=discord.Embed(description=f"{desc}\n >>> `Foolo ka Taaron Ka Sabka Kehna hai!`", color=discord.Color.random())
                emb.set_author(name=f"{ctx.author.name}, you have {len(sib)} siblings : ", icon_url=ctx.author.avatar.url)
                emb.timestamp = datetime.utcnow()
                emb.set_footer(icon_url=self.bot.user.avatar.url)
                emb.set_thumbnail(url="https://4.bp.blogspot.com/-T2bVs6xiUks/XHeLMCZlvOI/AAAAAAAUQDU/k-8YrZmX5j4S9VOaOULzqtExdduBcfPtQCLcBGAs/s1600/AW3567431_10.gif")
                await ctx.send(embed=emb)
                return
        if ctx.author.id ==user.id:
            await ctx.reply("Sad Soul!!")
            return
        elif not user.bot:
            rel = str(userdb.getsiblings(ctx.author.id))
            rel2 = str(userdb.getsiblings(user.id))

            if userdb.is_partner(ctx.author.id, user.id):
                emb = discord.Embed(title=f"", color=discord.Color.red(), description=f"> If You wanna make your partner your sibling, First take a divorce!\n**__Usage__:**\n`{prefix}div @user`")
                emb.set_author(name=f"Wha-! You Wanna Make Your Partner Sibling?", icon_url=ctx.author.avatar.url)
                emb.timestamp = datetime.utcnow()
                emb.set_footer(text="Team Tatsui ❤️")
                await ctx.channel.send(embed=emb)
                return

            sib = rel.split(",")
            sib2 = rel2.split(",")
            if rel == "0" and rel2=="0" or str(user.id) not in sib and str(ctx.author.id) not in sib2 :
                emb = discord.Embed(description=f"Hey {user.mention},  I feel glad too say that {ctx.author.mention} wants to make you their sibling ! It would make them  really happy if you accept this proposal. What do you say?\n")
                emb.set_author(name=f"{ctx.author.name} wants to make {user.name} their Sibling! <3 ")
                emb.timestamp = datetime.utcnow()
                emb.set_thumbnail(url="https://cdn.discordapp.com/attachments/865570883170861077/865875381537734686/output-onlinegiftools.gif")
                emb.set_footer(icon_url=self.bot.user.avatar.url)
                
                view = MarryButton(ctx.author)


                msg = await ctx.channel.send(embed=emb, view=view)
                try:
                    await view.wait()
                    if view.value is None:

                        view2= View()
                        btn3= Button(style=discord.ButtonStyle.blurple, emoji="<:amySad1:913697522474704916>", label="timeup", disabled=True)
                        view2.add_item(btn3)
                        await msg.edit(view=view2)
                        await ctx.send(f"😠 || Sorry, {ctx.author.mention}, {user.name} didn't reply on time!! Maybe They are confused, lets give them some time!")

                    elif view.value:
                        view2= View()
                        btn3= Button(style=discord.ButtonStyle.blurple, emoji="<:amySad1:913697522474704916>", label="timeup", disabled=True)
                        view2.add_item(btn3)
                        await msg.edit(view2)
                        userdb.add_sibling(ctx.author.id, user.id)
                        userdb.add_sibling(user.id, ctx.author.id)
                        await ctx.send(f"🏡 || {user.mention}, Yay! {ctx.author.mention} is now your Sibling. Congrats!!")
                        return
                
                    else:
                        view2= View()
                        btn3= Button(style=discord.ButtonStyle.blurple, emoji="<:amySad1:913697522474704916>", label="timeup", disabled=True)
                        await msg.edit(view=view2)
                        await ctx.send(f"💔 || {ctx.author.mention} Sorry ! But {user.mention} declined your request :((")
                        return

                except asyncio.TimeoutError:
                    view2= View()
                    btn3= Button(style=discord.ButtonStyle.blurple, emoji="<:amySad1:913697522474704916>", label="timeup", disabled=True)
                    await msg.edit(view=view2)
                    await ctx.send(f"😠 || Sorry, {ctx.author.mention} you didn't reply on time!!")
                    return
            else:
                await ctx.send(f"You Guys are Already Siblings !")
        else:
            await ctx.reply("BRUH!! You can't make a bot your Sibling!!")

    @commands.command(aliases=["nosib"], brief="Disown Your Sister.",callback="@user",name="disown",enabled="",help="Disown Your Sister.", extras={"emoji": "😭"},description="Disown Your Sister.")
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.default)
    async def remvsib(self,ctx, user: discord.Member=None):

        prefix = guilddb.check_prefix(ctx.guild.id)
        rel = userdb.getsiblings(ctx.author.id).split(',')
        if len(rel) == 0:
            await ctx.reply(f"{ctx.author.name}, You have no E-siblings right now! Please make Someone First! ex. `{prefix}sib @user`")
            return
        if user == None:
            await ctx.send("Please use @mention  someone.")
            return
        else:
            try:
                if str(user.id) in rel:
                    emb=discord.Embed(description=f"{ctx.author.mention}, Are you sure? ", color=discord.Color.nitro_pink())
                    emb.set_author(name=f"{ctx.author.name}, are you sure you want to disown {user.name} as your Sibling?", icon_url=ctx.author.avatar.url)
                    view = MarryButton(ctx.author)


                    msg = await ctx.channel.send(embed=emb, view=view)
                    try:
                        await view.wait()
                        if view.value is None:

                            view2= View()
                            btn3= Button(style=discord.ButtonStyle.blurple, emoji="<:amySad1:913697522474704916>", label="timeup", disabled=True)
                            view2.add_item(btn3)
                            await msg.edit(view=view2)
                            await ctx.send(f"😠 || Sorry, {ctx.author.mention}, {user.name} didn't reply on time!! Maybe They are confused, lets give them some time!")
                            return

                        elif view.value:
                            view2= View()
                            btn3= Button(style=discord.ButtonStyle.blurple, emoji="<:amySad1:913697522474704916>", label="timeup", disabled=True)
                            view2.add_item(btn3)
                            await msg.edit(view2)
                            await msg.edit( components=[])
                            await ctx.send(f":broken_heart:  || {ctx.author.mention}, You have decided to disown them as sibling.")
                            userdb.remv_sibling(ctx.author.id, str(user.id))
                            userdb.remv_sibling(user.id, str(ctx.author.id))

                            return
                    
                        else:
                            view2= View()
                            btn3= Button(style=discord.ButtonStyle.blurple, emoji="<:amySad1:913697522474704916>", label="timeup", disabled=True)
                            await msg.edit(view=view2)
                            await ctx.send(f"👍 || {ctx.author.mention},You have declined")
                            return

                    except asyncio.TimeoutError:
                        view2= View()
                        btn3= Button(style=discord.ButtonStyle.blurple, emoji="<:amySad1:913697522474704916>", label="timeup", disabled=True)
                        await msg.edit(view=view2)
                        await ctx.send(f"😠 || Sorry, {ctx.author.mention} you didn't reply on time!!")
                        return
                else:
                    await ctx.send(f"You Guys are Already Siblings !")
            except:
                return


    @commands.command(aliases=[], brief="Check your Family.",callback="@user",name="family",help="Check your Family.", extras={"emoji": "👪"},description="Check your Family.")
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.default)
    async def family(self,ctx, user: discord.Member=None):

        prefix = guilddb.check_prefix(ctx.guild.id)
        if user == None:
            view = FamilyOption(self.bot, ctx.author)
            emb = discord.Embed(color=ctx.author.color,description=f"Nickname: `{ctx.author.name}`\nID: `{ctx.author.id}`")
            emb.set_thumbnail(url=ctx.author.avatar.url)
            emb.set_author(name=f"{ctx.author.name}'s Family", icon_url=ctx.author.avatar.url)
            emb.add_field(name=f"Check Family - ", value=f"Select Desired Family option from DropDown.")
            msg = await ctx.channel.send(embed=emb, view=view)
            try:
                await view.wait()        
                a = await view.on_timeout()
                await msg.edit(view=None)
            except Exception as err:
                print(err)
        else:
            view = FamilyOption(self.bot, user)
            emb = discord.Embed(color=user.color,description=f"Nickname: `{user.name}`\nID: `{user.id}`")
            emb.set_thumbnail(url=user.avatar.url)
            emb.set_author(name=f"{user.name}'s Family", icon_url=user.avatar.url)
            emb.add_field(name=f"Check Family - ", value=f"Select Desired Family option from DropDown.")
            msg = await ctx.channel.send(embed=emb, view=view)
            try:
                await view.wait()        
                a = await view.on_timeout()
                await msg.edit(view=None)
            except Exception as err:
                print(err)

def setup(bot):
    bot.add_cog(Family(bot))