import discord
from discord.ext import commands
import pyrebase
from json import loads , load 
import time

with open("firebase.json", "r") as read_file:
    firebase = pyrebase.initialize_app(load(read_file))
db = firebase.database()

Guild_Variable ={
    "prefix" : "a!",
    "blacklisted": "0",
    "command": "0"
}

def new_guild(guild):
    db.child("Guild_Variable").child(guild).set(Guild_Variable)

def add_prefix(guild_id: int, prefix: str):
    guild_prefix = db.child("Guild_Variable").child(guild_id).get().val()
    if guild_prefix == None:
        new_guild(guild_id)
    guild_prefix["prefix"] = prefix
    db.child("Guild_Variable").child(guild_id).set(guild_prefix)

def check_prefix(guild_id: int):
    guild_prefix = db.child("Guild_Variable").child(guild_id).get().val()
    if guild_prefix == None:
        new_guild(guild_id)
        guild_prefix = db.child("Guild_Variable").child(guild_id).get().val()
    prefix = str(guild_prefix["prefix"])
    return prefix

def add_blacklist(guild_id: int, channelId: str):
    guild_data = db.child("Guild_Variable").child(guild_id).get().val()
    if guild_data == None:
        new_guild(guild_id)
    if guild_data["blacklist"] == "0":
        guild_data["blacklist"] = str(channelId)
    else:
        guild_data["blacklist"] = str(guild_data["blacklist"])+ "," + str(channelId)
    db.child("Guild_Variable").child(guild_id).set(guild_data)
    return

def add_command(guild_id: int, command: str):
    guild_data = db.child("Guild_Variable").child(guild_id).get().val()
    if guild_data == None:
        new_guild(guild_id)
    if guild_data["command"] == "0":
        guild_data["command"] = str(command)
    else:
        guild_data["command"] = str(guild_data["command"])+ "," + str(command)
    db.child("Guild_Variable").child(guild_id).set(guild_data)
    return

def check_channel(guild_id: int ):
    guild_data = db.child("Guild_Variable").child(guild_id).get().val()
    if guild_data == None:
        new_guild(guild_id)
        guild_data = db.child("Guild_Variable").child(guild_id).get().val()
    relation = guild_data["blacklist"]
    return relation

def is_channel_blacklisted(guild_id: int, channel_id):
    guild_data = str(check_channel(int(guild_id)))
    q= guild_data.split(",")
    if str(channel_id) in q:
        return True
    else:
        return False

def remv_blacklist(guild, channel):
    guild_data = db.child("Guild_Variable").child(guild).get().val()
    li = guild_data["blacklist"].split(",")
    if guild_data["blacklist"] == "0":
        return 0
    if channel in li:
        li.remove(channel)
        guild_data["blacklist"] = ",".join(li)
        db.child("Guild_Variable").child(guild).set(guild_data)
    elif not channel in li:
        return 1
    else:
        return None

def remv_cmd(guild, cmd):
    guild_data = db.child("Guild_Variable").child(guild).get().val()
    li = guild_data["command"].split(",")
    if guild_data["command"] == "0":
        return 0
    if cmd in li:
        li.remove(cmd)
        guild_data["command"] = ",".join(li)
        db.child("Guild_Variable").child(guild).set(guild_data)
    elif not cmd in li:
        return 1
    else:
        return None

def afcreate(id, guild,  message):
   db.child("AFKUTIL").child(id).child(guild).set({"AFK" : True, "MESSAGE": message, "PING": 0, "TIME": f"{time.time()}"})

def checkafk(id, guild):
    check = db.child("AFKUTIL").child(id).child(guild).child("AFK").get().val()
    if check == None or check == False:
        return False
    elif check == True:
        return True

def get_afk_message(id, guild):
    message = db.child("AFKUTIL").child(id).child(guild).child("MESSAGE").get().val()
    return message

def get_time(id, guild):
    time = db.child("AFKUTIL").child(id).child(guild).child("TIME").get().val()
    return time

def get_ping(id, guild):
    ping = db.child("AFKUTIL").child(id).child(guild).child("PING").get().val()
    return ping

def remove_afk(id, guild):
    db.child("AFKUTIL").child(id).child(guild).remove()

def add_ping(id, guild):
    ping = db.child("AFKUTIL").child(id).child(guild).child("PING").get().val()
    if ping == None:
        return 0
    ping += 1
    ping = db.child("AFKUTIL").child(id).child(guild).child("PING").set(ping)
