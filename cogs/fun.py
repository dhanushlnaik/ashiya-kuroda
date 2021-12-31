import discord
from discord.ext import commands
import datetime
import time
from random import choice , randint
from asyncio import TimeoutError
from aiohttp import ClientSession
from imgurpython import ImgurClient
import giphy_client
from giphy_client.rest import ApiException
import praw
from tools import *
import urbandict
from database import guilddb
from typing import List
from discord.ext import commands
import discord
from dotenv import load_dotenv
from tools import last_replace , text_to_owo
from akinator.async_aki import Akinator
import akinator
import asyncio

aki = Akinator()

class TicTacToeButton(discord.ui.Button["TicTacToe"]):
    def __init__(self, x: int, y: int):
        super().__init__(style=discord.ButtonStyle.secondary, label="\u200b", row=y)
        self.x = x
        self.y = y

    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: TicTacToe = self.view
        state = view.board[self.y][self.x]
        if state in (view.X, view.O):
            return

        if view.current_player == view.X:
            self.style = discord.ButtonStyle.danger
            self.label = "X"
            self.disabled = True
            view.board[self.y][self.x] = view.X
            view.current_player = view.O
            content = "It is now O's turn"
        else:
            self.style = discord.ButtonStyle.success
            self.label = "O"
            self.disabled = True
            view.board[self.y][self.x] = view.O
            view.current_player = view.X
            content = "It is now X's turn"

        winner = view.check_board_winner()
        if winner is not None:
            if winner == view.X:
                content = "X won!"
            elif winner == view.O:
                content = "O won!"
            else:
                content = "It's a tie!"

            for child in view.children:
                child.disabled = True

            view.stop()

        await interaction.response.edit_message(content=content, view=view)

class TicTacToe(discord.ui.View):
    children: List[TicTacToeButton]
    X = -1
    O = 1
    Tie = 2

    def __init__(self):
        super().__init__()
        self.current_player = self.X
        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]

        for x in range(3):
            for y in range(3):
                self.add_item(TicTacToeButton(x, y))

    def check_board_winner(self):
        for across in self.board:
            value = sum(across)
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        for line in range(3):
            value = self.board[0][line] + self.board[1][line] + self.board[2][line]
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        diag = self.board[0][2] + self.board[1][1] + self.board[2][0]
        if diag == 3:
            return self.O
        elif diag == -3:
            return self.X

        diag = self.board[0][0] + self.board[1][1] + self.board[2][2]
        if diag == 3:
            return self.O
        elif diag == -3:
            return self.X

        if all(i != 0 for row in self.board for i in row):
            return self.Tie

        return None
load_dotenv()
REDDIT_APP_ID = os.environ.get("REDDIT_APP_ID")
REDDIT_APP_SECRET = os.environ.get("REDDIT_APP_SECRET")
REDDIT_ENABLED_MEME_SUBREDDITS = [
    'funny',
    'memes'
]
REDDIT_ENABLED_NSFW_SUBREDDITS = [
    'wtf'
]

def user_is_me(ctx):
    return ctx.message.author.id == 624174437821972480

# __COLORS__
color1 = discord.Color.from_rgb(93,71,82)
color2 = discord.Color.from_rgb(248,238,229)
color3 = discord.Color.from_rgb(228,188,148)
color4 = discord.Color.from_rgb(129,110,112)

randcol = [color1, color2, color3, color4]
melon = choice(randcol)




async def notify_user(member, message):
    if member is not None:
        channel = member.dm_channel
        if channel is None:
            channel = await member.create_dm()
        await channel.send(message)

tenor_key = os.environ.get("TENOR_KEY")
api_key = os.environ.get("API_KEY")
imgur = ImgurClient(os.environ.get("IMGUR"),os.environ.get("IMGUR_KEY"))

async def get(session: object, url: object) -> object:
        async with session.get(url) as response:
            return await response.text()


rpsC = ["Rock", "Paper", "Scissors"]
melon = discord.Color.from_rgb(248,131,121)
response_list = ["As I see it, yes", "Yes", "No", "Very likely", "Not even close", "Maybe", "Very unlikely", "Gino's mom told me yes", "Gino's mom told me no", "Ask again later", "Better not tell you now", "Concentrate and ask again", "Don't count on it", " It is certain", "My sources say no", "Outlook good", "You may rely on it", "Very Doubtful", "Without a doubt"]

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reddit = None
        if REDDIT_APP_ID and REDDIT_APP_SECRET:
            self.reddit = praw.Reddit(client_id=REDDIT_APP_ID, client_secret=REDDIT_APP_SECRET,
                                      user_agent="ULTIMATE_DISCORD_BOT:%s:1.0" % REDDIT_APP_ID)


    @commands.command(aliases=["aki"],name="akinator",help="Play Akinator.", extras={"emoji": "🍾"},description="Play Akinator.")
    async def akinator(self, ctx):
        await ctx.author.send(f"{ctx.author.mention} The game is about to begin!\n You will get 60 seconds to answer each question, answer in `yes/no` or `y/n`.")
        await asyncio.sleep(5)
        q = await aki.start_game()
        c = 0
        while aki.progression <= 80:
            await ctx.author.send(f"**{q}**")
            try:
                def check(m):
                    return m.author == ctx.author and m.channel.type is discord.ChannelType.private
                a = await self.client.wait_for('message', check=check, timeout=60)
                if a == "back":
                    try:
                        q = await aki.back()
                    except akinator.CantGoBackAnyFurther:
                        pass
                elif a == "stop":
                    await aki.close()
                    await ctx.author.send(f"{ctx.author.mention} Game stopped!")
                    c = c+1
                    break
                else:
                    try:
                        q = await aki.answer(a.content.lower())
                    except Exception:
                        await ctx.author.send("Invalid Response to question!\nAnswer in `yes/no` or `y/n`.")
            except asyncio.TimeoutError:
                await ctx.author.send(f"{ctx.author.mention} You took too long to answer the question, the game has been stopped!")
                await aki.close()
                c = c+1
                break
        await aki.win()

        if c == 0:
            desc=f"**It's {aki.first_guess['name']}**\n*{aki.first_guess['description']}*!\n**Was I correct? (yes/no)**"
            emb = discord.Embed(title="Here is my guess!", description=desc, color=0x2e69f2)
            emb.set_image(url=aki.first_guess['absolute_picture_path'])
            await ctx.author.send(embed=emb)
            def check(m):
                    return m.author == ctx.author
            correct = await self.client.wait_for('message', check=check, timeout=60)
            if correct.content.lower() == "yes" or correct.content.lower() == "y":
                await ctx.author.send("Yay :)")
            else:
                await ctx.author.send("Oof :(")
            await aki.close()
                                
    @commands.command(aliases=["drunk"], brief="Drunkify a series of text.",callback="<text>",name="drunkify",help="Drunkify a series of text.", extras={"emoji": "🍾"},description="Drunkify a series of text.")
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.default)
    async def drunkify(self, ctx, *, s):
        if guilddb.is_channel_blacklisted(ctx.guild.id, ctx.channel.id):
            return
        lst = [str.upper, str.lower]
        newText = await commands.clean_content().convert(ctx, ''.join(choice(lst)(c) for c in s))
        if len(newText) <= 380:
            await ctx.send(newText)
        else:
            try:
                await ctx.author.send(newText)
                await ctx.send(f"**{ctx.author.mention} The output too was too large, so I sent it to your DMs! :mailbox_with_mail:**")
            except Exception:
                await ctx.send(f"**{ctx.author.mention} There was a problem, and I could not send the output. It may be too large or malformed**")


    @commands.command(aliases=["shipping"], brief="Ship two users.",callback="<user1> <user2>",name="ship",help="Ship two users.", extras={"emoji": "💟"},description="Ship two users.")
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.default)
    async def ship(self, ctx, name1 : commands.clean_content, name2 : commands.clean_content):
        if guilddb.is_channel_blacklisted(ctx.guild.id, ctx.channel.id):
            return
        shipnumber = randint(0,100)
        if 0 <= shipnumber <= 10:
            status = "Really low! {}".format(choice(["Friendzone ;(", 
                                                            'Just "friends"', 
                                                            '"Friends"', 
                                                            "Little to no love ;(", 
                                                            "There's barely any love ;("]))
        elif 10 < shipnumber <= 20:
            status = "Low! {}".format(choice(["Still in the friendzone", 
                                                     "Still in that friendzone ;(", 
                                                     "There's not a lot of love there... ;("]))
        elif 20 < shipnumber <= 30:
            status = "Poor! {}".format(choice(["But there's a small sense of romance from one person!", 
                                                     "But there's a small bit of love somewhere", 
                                                     "I sense a small bit of love!", 
                                                     "But someone has a bit of love for someone..."]))
        elif 30 < shipnumber <= 40:
            status = "Fair! {}".format(choice(["There's a bit of love there!", 
                                                      "There is a bit of love there...", 
                                                      "A small bit of love is in the air..."]))
        elif 40 < shipnumber <= 60:
            status = "Moderate! {}".format(choice(["But it's very one-sided OwO", 
                                                          "It appears one sided!", 
                                                          "There's some potential!", 
                                                          "I sense a bit of potential!", 
                                                          "There's a bit of romance going on here!", 
                                                          "I feel like there's some romance progressing!", 
                                                          "The love is getting there..."]))
        elif 60 < shipnumber <= 70:
            status = "Good! {}".format(choice(["I feel the romance progressing!", 
                                                      "There's some love in the air!", 
                                                      "I'm starting to feel some love!"]))
        elif 70 < shipnumber <= 80:
            status = "Great! {}".format(choice(["There is definitely love somewhere!", 
                                                       "I can see the love is there! Somewhere...", 
                                                       "I definitely can see that love is in the air"]))
        elif 80 < shipnumber <= 90:
            status = "Over average! {}".format(choice(["Love is in the air!", 
                                                              "I can definitely feel the love", 
                                                              "I feel the love! There's a sign of a match!", 
                                                              "There's a sign of a match!", 
                                                              "I sense a match!", 
                                                              "A few things can be imporved to make this a match made in heaven!"]))
        elif 90 < shipnumber <= 100:
            status = "True love! {}".format(choice(["It's a match!", 
                                                           "There's a match made in heaven!", 
                                                           "It's definitely a match!", 
                                                           "Love is truely in the air!", 
                                                           "Love is most definitely in the air!"]))

        if shipnumber <= 33:
            shipColor = 0xE80303
        elif 33 < shipnumber < 66:
            shipColor = 0xff6600
        else:
            shipColor = 0x3be801

        emb = (discord.Embed(color=shipColor, \
                             title="Love test for:", \
                             description="**{0}** and **{1}** {2}".format(name1, name2, choice([
                                                                                                        ":sparkling_heart:", 
                                                                                                        ":heart_decoration:", 
                                                                                                        ":heart_exclamation:", 
                                                                                                        ":heartbeat:", 
                                                                                                        ":heartpulse:", 
                                                                                                        ":hearts:", 
                                                                                                        ":blue_heart:", 
                                                                                                        ":green_heart:", 
                                                                                                        ":purple_heart:", 
                                                                                                        ":revolving_hearts:", 
                                                                                                        ":yellow_heart:", 
                                                                                                        ":two_hearts:"]))))
        emb.add_field(name="Results:", value=f"{shipnumber}%", inline=True)
        emb.add_field(name="Status:", value=(status), inline=False)
        emb.set_author(name="Shipping", icon_url="http://moziru.com/images/kopel-clipart-heart-6.png")
        await ctx.send(embed=emb)
        
    @commands.command(aliases=["8ball", "tellme", "isittrue"], brief="Extra generic 8ball Game. ",callback="<text>",name="eightball",help="Extra generic 8ball Game. ", extras={"emoji": "🎱"},description="Extra generic 8ball Game. ")
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.default)
    async def eightball(self, ctx, *, _ballInput: commands.clean_content):
        if guilddb.is_channel_blacklisted(ctx.guild.id, ctx.channel.id):
            return
        choiceType = choice(["(Affirmative)", "(Non-committal)", "(Negative)"])
        if choiceType == "(Affirmative)":
            prediction = choice(["It is certain ", 
                                        "It is decidedly so ", 
                                        "Without a doubt ", 
                                        "Yes, definitely ", 
                                        "You may rely on it ", 
                                        "As I see it, yes ",
                                        "Most likely ", 
                                        "Outlook good ", 
                                        "Yes ", 
                                        "Signs point to yes "]) + ":8ball:"

            emb = (discord.Embed(title="Question: {}".format(_ballInput), colour=0x3be801, description=prediction))
        elif choiceType == "(Non-committal)":
            prediction = choice(["Reply hazy try again ", 
                                        "Ask again later ", 
                                        "Better not tell you now ", 
                                        "Cannot predict now ", 
                                        "Concentrate and ask again "]) + ":8ball:"
            emb = (discord.Embed(title="Question: {}".format(_ballInput), colour=0xff6600, description=prediction))
        elif choiceType == "(Negative)":
            prediction = choice(["Don't count on it ", 
                                        "My reply is no ", 
                                        "My sources say no ", 
                                        "Outlook not so good ", 
                                        "Very doubtful "]) + ":8ball:"
            emb = (discord.Embed(title="Question: {}".format(_ballInput), colour=0xE80303, description=prediction))
        emb.set_author(name='Magic 8 ball', icon_url='https://www.horoscope.com/images-US/games/game-magic-8-ball-no-text.png')
        await ctx.send(embed=emb)


    @commands.command(aliases=[ "gayscanner"], brief="A Gay Scanner.",callback="@user",name="gay",help="A Gay Scanner.", extras={"emoji": "🌈"},description="A Gay Scanner.")
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.default)
    async def gay_scanner(self, ctx,* ,user: commands.clean_content=None):
        if guilddb.is_channel_blacklisted(ctx.guild.id, ctx.channel.id):
            return
        if not user:
            user = ctx.author.name
        gayness = randint(0,100)
        if gayness <= 33:
            gayStatus = choice(["No homo", 
                                       "Wearing socks", 
                                       '"Only sometimes"', 
                                       "Straight-ish", 
                                       "No homo bro", 
                                       "Girl-kisser", 
                                       "Hella straight"])
            gayColor = 0xFFC0CB
        elif 33 < gayness < 66:
            gayStatus = choice(["Possible homo", 
                                       "My gay-sensor is picking something up", 
                                       "I can't tell if the socks are on or off", 
                                       "Gay-ish", 
                                       "Looking a bit homo", 
                                       "lol half  g a y", 
                                       "safely in between for now"])
            gayColor = 0xFF69B4
        else:
            gayStatus = choice(["LOL YOU GAY XDDD FUNNY", 
                                       "HOMO ALERT", 
                                       "MY GAY-SENSOR IS OFF THE CHARTS", 
                                       "STINKY GAY", 
                                       "BIG GEAY", 
                                       "THE SOCKS ARE OFF", 
                                       "HELLA GAY"])
            gayColor = 0xFF00FF
        emb = discord.Embed(description=f"Gayness for **{user}**", color=gayColor)
        emb.add_field(name="Gayness:", value=f"{gayness}% gay")
        emb.add_field(name="Comment:", value=f"{gayStatus} :kiss_mm:")
        emb.set_author(name="Gay-Scanner™", icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a4/ICA_flag.svg/2000px-ICA_flag.svg.png")
        await ctx.send(embed=emb)

    @commands.command(aliases=["reddit", "subrettit", "rslash", "r"], brief="Random Post from desired Subreddit.",callback="<redditname>",name="random",help="Random Post from desired Subreddit.", extras={"emoji": "😂"},description="Random Post from desired Subreddit.")
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.default)
    async def random(self, ctx, subreddit: str="cat"):
        if guilddb.is_channel_blacklisted(ctx.guild.id, ctx.channel.id):
            return
        async with ctx.channel.typing():
            if self.reddit:
                allsubs = []
                submissions = self.reddit.subreddit(subreddit)
                top = submissions.top(limit=50)
                for subm in top:
                    allsubs.append(subm)

                randomsub = choice(allsubs)

                while True:
                    name = randomsub.title
                    url = randomsub.url
                    if url.endswith("jpg") or url.endswith("png"):
                        break
                    else:
                        randomsub = choice(allsubs)
                em = discord.Embed(title=name, color=discord.Color.blurple())
                em.set_image(url=url)
                await ctx.send(embed=em)
            else:
                await ctx.send("This is not working. Contact Administrator.")

    @commands.command(aliases=["mommajokes"], brief="Insults a user via Momma Joke.",callback="@user",name="insult",help="Insults a user via Momma Joke.", extras={"emoji": "😹"},description="Insults a user via Momma Joke.")
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.default)
    async def insult(self, ctx, member: discord.Member = None):
        if guilddb.is_channel_blacklisted(ctx.guild.id, ctx.channel.id):
            return
        insult = get_momma_jokes()
        if member is not None:
            await ctx.send("%s eat this: %s " % (member.name, insult))
        else:
            await ctx.send("%s for yourself: %s " % (ctx.message.author.name, insult))

    @commands.command(aliases= ["copy"], brief="Make me say Something.",callback="<text>",name="say",help="Make me say Something.", extras={"emoji": "🗣"},description="Drunkify a series of text.")
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.default)
    async def say(self, ctx,*,msg):
        if guilddb.is_channel_blacklisted(ctx.guild.id, ctx.channel.id):
            return
        mes = await ctx.send(msg)



    @commands.command(aliases=["doggo", "doggies", "🐕", "doggie"], brief="Random Dog Picture and Fact.",callback="",name="dog",help="Random Dog Picture and Fact.", extras={"emoji": "🐕"},description="Random Dog Picture and Fact.")
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.default)
    async def dog(self, ctx):
        if guilddb.is_channel_blacklisted(ctx.guild.id, ctx.channel.id):
            return
        async with ClientSession() as session:
            request = await session.get('https://some-random-api.ml/img/dog')
            dogjson = await request.json()
            # This time we'll get the fact request as well!
            request2 = await session.get('https://some-random-api.ml/facts/dog')
            factjson = await request2.json()

        embed = discord.Embed(title="Doggo!", color=discord.Color.purple(), description=factjson['fact'])
        embed.set_image(url=dogjson['link'])
        await ctx.send(embed=embed)

    @commands.command(aliases=["catto", "cattie", "🐈"], brief="Random Cat Picture and Fact.",callback="",name="cat",help="Random Cat Picture and Fact.", extras={"emoji": "😾"},description="Random Cat Picture and Fact.")
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.default)
    async def cat(self, ctx):
        if guilddb.is_channel_blacklisted(ctx.guild.id, ctx.channel.id):
            return
        async with ClientSession() as session:
            request = await session.get('https://some-random-api.ml/img/cat')
            dogjson = await request.json()
            # This time we'll get the fact request as well!
            request2 = await session.get('https://some-random-api.ml/facts/cat')
            factjson = await request2.json()

        embed = discord.Embed(title="Cat", color=discord.Color.purple(), description=factjson['fact'])
        embed.set_image(url=dogjson['link'])
        await ctx.send(embed=embed)


    @commands.command(aliases=["img", "image","picture"], brief="Search for an Image from ImageUr.",callback="< search result >",name="imgur",help="Search for an Image from ImageUr.", extras={"emoji": "🖼"},description="Search for an Image from ImageUr.")
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.default)
    async def imgur(self, ctx, *text: str):
        if guilddb.is_channel_blacklisted(ctx.guild.id, ctx.channel.id):
            return
        rand = randint(0, 29)
        if text == ():
            await ctx.send('**Please enter a search term**')
        elif text[0] != ():
            items = imgur.gallery_search(" ".join(text[0:len(text)]), advanced=None, sort='viral', window='all',page=0)
            await ctx.send(items[rand].link)

    @commands.command(aliases=[], brief="Search for a Gif from Giphy.",callback="< search result >",name="giphy",help="Search for a Gif from Giphy.", extras={"emoji": "📹"},description="Search for a Gif from Giphy.")
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.default)    
    async def gif(self, ctx,*,q="Anime"):
        if guilddb.is_channel_blacklisted(ctx.guild.id, ctx.channel.id):
            return
        api_instance = giphy_client.DefaultApi()

        try:
            api_response = api_instance.gifs_search_get(api_key, q, limit=5, rating='g')
            lst = list(api_response.data)
            rgiff = choice(lst)
            emb = discord.Embed(color=ctx.author.color)
            emb.set_author(name=q.title(),icon_url=ctx.author.avatar.url)
            emb.set_image(url=f"https://media.giphy.com/media/{rgiff.id}/giphy.gif")
            await ctx.channel.send(embed=emb)
        except ApiException as e:
            print("Exception when calling Api as "+e)

    @commands.command(aliases=[], brief="Poke a User.",callback="@user",name="poke",help="Poke a User.", extras={"emoji": "💢"},description="Poke a User.")
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.default)
    async def poke(self, ctx, member: discord.Member = None):
        if guilddb.is_channel_blacklisted(ctx.guild.id, ctx.channel.id):
            return
        try:
            if member is not None:
                message = "%s poked you!!!!" % ctx.author.name
                await notify_user(member, message)
                await ctx.message.delete()
            else:
                await ctx.send("Please use @mention to poke someone.")
        except:
            message = "%s poked you!!!!" % ctx.author.name
            await ctx.send(f"{member.mention},{message}/n ||Cant Dm them||")
            
    @commands.command(aliases=[], brief="Owoify Text.",callback="<text>",name="owo",help="Owoify Text.", extras={"emoji": "😳"},description="Owoify Text.")
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.default)
    async def owo(self, ctx):
        if guilddb.is_channel_blacklisted(ctx.guild.id, ctx.channel.id):
            return
        await ctx.send(text_to_owo(ctx.message.content))

    @commands.command(aliases=["d", "dre"], brief="Get a random Dare.",callback="@user",name="dare",help="Get a random Dare.", extras={"emoji": "🎯"},description="Drunkify a series of text.")
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.default)
    async def dare(self,ctx,*,msg=None):
        if guilddb.is_channel_blacklisted(ctx.guild.id, ctx.channel.id):
            return
        dareRand = get_dare()
        emb = discord.Embed(color = melon)
        emb.set_author(name=f"DARE : {dareRand}", icon_url=ctx.author.avatar.url)
        await ctx.send(embed=emb)

    @commands.command(aliases=["t", "true", "tru"], brief="Get a random Truth Question.",callback="@user",name="truth",help="Get a random Truth Question.", extras={"emoji": "😬"},description="Get a random Truth Question.")
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.default)
    async def truth(self,ctx,*,msg=None):
        if guilddb.is_channel_blacklisted(ctx.guild.id, ctx.channel.id):
            return
        truthRand = get_truth()
        emb = discord.Embed(color = melon)
        emb.set_author(name=f"TRUTH : {truthRand}", icon_url=ctx.author.avatar.url)
        await ctx.send(embed=emb)

    @commands.command(aliases=["wouldyou", "wouldyourather"],  brief="Get a random Would You Rather Question.",callback="@user",name="wyr",help="Get a random Would You Rather Question.", extras={"emoji": "🙄"},description="Get a random Truth Question.")
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.default)
    async def wyr(self,ctx,*,msg=None):
        if guilddb.is_channel_blacklisted(ctx.guild.id, ctx.channel.id):
            return
        wyrRand = get_wyr()
        emb = discord.Embed(color = melon)
        emb.set_author(name=f"{wyrRand}", icon_url=ctx.author.avatar.url)
        await ctx.send(embed=emb)

    @commands.command(aliases=["neverhaveiever"], brief="Get a random Never Have I Ever Question.",callback="@user",name="nhie",help="Get a random Never Have I Ever Question.", extras={"emoji": "😏"},description="Get a random Never Have I Ever Question.")
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.default)
    async def nhie(self,ctx,*,msg=None):
        if guilddb.is_channel_blacklisted(ctx.guild.id, ctx.channel.id):
            return
        nhieRand = get_nhie()
        emb = discord.Embed(color = melon)
        emb.set_author(name=f"{nhieRand}", icon_url=ctx.author.avatar.url)
        await ctx.send(embed=emb)

    @commands.command(aliases=["urbandict", "dict"], brief="Check Something in Urban Dictionary.",callback="<text>",name="df",help="Check Something in Urban Dictionary.", extras={"emoji": "📚"},description="Check Something in Urban Dictionary.")
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.default)
    async def urban(self,ctx,*,define):
        if guilddb.is_channel_blacklisted(ctx.guild.id, ctx.channel.id):
            return
        term = urbandict.define(define)
        print(term)
        ex = term[0]['example']
        meaning = term[0]['def']
        embed = discord.Embed(title=f"{define.title()}",description=f"Meaning : {meaning}\n {term[1]['def']}",color=melon)
        embed.add_field(name="Example:", value=f"{ex}\n{term[1]['example']}")
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)

    # @commands.command(aliases=["tac", "toe", "ttt"], brief="Starts a tic-tac-toe game with yourself.",callback="<text>",name="tic",help="Starts a tic-tac-toe game with yourself.", extras={"emoji": "📚"},description="Starts a tic-tac-toe game with yourself.")
    # @commands.cooldown(rate=1, per=5, type=commands.BucketType.default)
    # async def tic(self,ctx: commands.Context):
    #     await ctx.send("Tic Tac Toe: X goes first", view=TicTacToe())


def setup(bot):
    bot.add_cog(Fun(bot))