from slackclient import SlackClient
import os
import time
import re


def isThisValid(evt):
    num_tacos = len(re.findall(":taco:", evt["text"]))
    if num_tacos > 0:
        users = re.findall("<@.........>", evt["text"])
        for uid in users:
            uid = uid.replace("<@", "")
            uid =uid.replace(">", "")
            print uid
            tacoLogic(uid, evt, num_tacos)
            

def tacoLogic(uid, evt, num_tacos):
    sender = evt["user"]
    reciever = uid
    if reciever in taco_dict and sender in taco_give_dict:
        if taco_give_dict[sender] >= num_tacos:
            taco_give_dict[sender] -= num_tacos
            taco_dict[reciever] += num_tacos
            reponse = sc.api_call("chat.postMessage", channel="#tacotest", text="<@" + reciever + "> now has: " + str(taco_dict[reciever]) + " tacos!")
            reponse = sc.api_call("chat.postMessage", channel="#tacotest", text="<@" + sender + "> has given " + str(5 -taco_give_dict[sender]) + " tacos today")
            print reponse
        else:
            reponse = sc.api_call("chat.postMessage", channel="#tacotest", text="Not enough tacos to give today, try again tomorrow")




token = os.environ["SLACK_API_TOKEN"]
sc = SlackClient(token)

taco_dict = {}
taco_give_dict = {}

api_call = sc.api_call("users.list")
if api_call.get('ok'):
    users = api_call.get("members")
    for user in users:
        uid = user["id"]
        taco_give_dict[uid] = 5
        taco_dict[uid] = 0
        print uid


if sc.rtm_connect():
    while True:
        events = sc.rtm_read()
        print events
        for evt in events:
            if(evt["type"] == "message"):
                print evt["text"]
                isThisValid(evt)
        time.sleep(1)
else:
    print "Connection Failed, invalid token?"







