from discord.ext import commands
import discord
import aiohttp
from io import BytesIO
from dotenv import load_dotenv
import os
import requests
import json

load_dotenv()
API_KEY = os.environ.get("WEEBY_API_KEY")

def check_img(user):
    if user.avatar.url is None:
        return 
    else:
        return user.avatar.url

def return_gif(arg):
    request = requests.get(f"https://weebyapi.xyz/gif/{arg}?token={str(API_KEY)}")
    rjson = json.loads(request.content)
    return rjson['url']



import json
import os
import random


current_directory = os.path.dirname(__file__)
file_path = os.path.join(current_directory,  'data')


def get_momma_jokes():
    with open(os.path.join(file_path, "jokes.json"), encoding="utf8") as joke_file:
        jokes = json.load(joke_file)
    random_category = random.choice(list(jokes.keys()))
    insult = random.choice(list(jokes[random_category]))
    return insult


def get_truth():
    with open(os.path.join(file_path, "tord.json"), encoding="utf8") as tord_file:
        ques = json.load(tord_file)
    truth = random.choice(list(ques["truth"]))
    return truth


def get_dare():
    with open(os.path.join(file_path, "tord.json"), encoding="utf8") as tord_file:
        ques = json.load(tord_file)
    dare = random.choice(list(ques["dare"]))
    return dare


def get_wyr():
    with open(os.path.join(file_path, "tord.json"), encoding="utf8") as tord_file:
        ques = json.load(tord_file)
    wyr = random.choice(list(ques["wyr"]))
    return wyr


def get_nhie():
    with open(os.path.join(file_path, "tord.json"), encoding="utf8") as tord_file:
        ques = json.load(tord_file)
    nhie = random.choice(list(ques["nhie"]))
    return nhie

def last_replace(s, old, new):
    li = s.rsplit(old, 1)
    return new.join(li)
vowels = ['a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U']

def text_to_owo(text):
    """ Converts your text to OwO """
    smileys = [';;w;;', '^w^', '>w<', 'UwU', '(・`ω\´・)', '(´・ω・\`)']

    text = text.replace('L', 'W').replace('l', 'w')
    text = text.replace('R', 'W').replace('r', 'w')

    text = last_replace(text, '!', '! {}'.format(random.choice(smileys)))
    text = last_replace(text, '?', '? owo')
    text = last_replace(text, '.', '. {}'.format(random.choice(smileys)))

    for v in vowels:
        if 'n{}'.format(v) in text:
            text = text.replace('n{}'.format(v), 'ny{}'.format(v))
        if 'N{}'.format(v) in text:
            text = text.replace('N{}'.format(v), 'N{}{}'.format(
                'Y' if v.isupper() else 'y', v))

    return text