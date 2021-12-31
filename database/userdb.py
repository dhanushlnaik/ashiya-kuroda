import pyrebase
from json import loads , load 
import datetime
import time

with open("firebase.json", "r") as read_file:
    firebase = pyrebase.initialize_app(load(read_file))
db = firebase.database()

User_Variable = {
    "PROFILE" : True,
    "CURRENCY" : "0",
    "SIBLINGS" : "0",
    "PARTNER" : {"ID" : "0", "DATE": "0", "DAY": "0", "RING": "0"},
}

def new_user(user):
    db.child("User_Variable").child(user).set(User_Variable)

def checkprofile(id):
    check = db.child("User_Variable").child(id).child("PROFILE").get().val()
    if check == None or check == False:
        return False
    elif check == True:
        return True

def changeprofile(id):
    check = db.child("User_Variable").child(id).child("PROFILE").get().val()
    if check == None or check == False:
        db.child("User_Variable").child(id).child("PROFILE").set(True)
        return
    elif check == True:
        db.child("User_Variable").child(id).child("PROFILE").set(False)
        return

def getsiblings(id):
    if db.child("User_Variable").child(id).get().val() is None:
        new_user(id)
    sib = db.child("User_Variable").child(id).child("SIBLINGS").get().val()
    return sib

def getpartnervar(id, var):
    if db.child("User_Variable").child(id).get().val() is None:
        new_user(id)
    part = db.child("User_Variable").child(id).child("PARTNER").child(var).get().val()
    return part


def is_sibling(rel1:str, rel2: str):
    rel = getsiblings(rel1)
    q= rel.split(",")
    if str(rel2) in q:
        return True
    else:
        return False

def is_partner(rel1: str, rel2:str):
    partner = getpartnervar(rel1, "ID")
    if partner == None:
        new_user(rel1)
        partner = getpartnervar(rel1, "ID")
    if str(rel2) == str(partner):
        return True
    else:
        return False

def add_sibling(user, user2):
    sib = db.child("User_Variable").child(user).child("SIBLINGS").get().val()
    if sib == "0":
        sib = user2
    else:
        sib = str(sib)+ "," + str(user2)
    db.child("User_Variable").child(user).child("SIBLINGS").set(sib)

def add_partnervar(user, ctx, val:str):
    db.child("User_Variable").child(user).child("PARTNER").child(ctx).set(val)

def remv_partner(user, ctx):
    db.child("User_Variable").child(user).child("PARTNER").child(ctx).set("0")

def remv_sibling(user, user2):
    sib = db.child("User_Variable").child(user).child("SIBLINGS").get().val().split(',') 
    if sib == "0":
        return
    if user2 in sib:
        sib.remove(user2)
        sib = ','.join(sib)
        db.child("User_Variable").child(user).child("SIBLINGS").set(sib)
    else:
        return

def add_time(id):
    db.child("User_Variable").child(id).child("PARTNER").child("DAY").set(str(datetime.datetime.now().strftime("%a, %B %d,%Y")))
    db.child("User_Variable").child(id).child("PARTNER").child("DATE").set(str(datetime.date.today()))
