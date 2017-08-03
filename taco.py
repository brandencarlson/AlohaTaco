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
            tacoLogic(uid, evt, num_tacos)
            

def tacoLogic(uid, evt, num_tacos):
    sender = evt["user"]
    reciever = uid
    if reciever in taco_dict and sender in taco_give_dict:
        if taco_give_dict[sender] >= num_tacos:
            taco_give_dict[sender] -= num_tacos
            taco_dict[reciever] += num_tacos
            dm = sc.api_call("im.open", user=sender)
            print dm
            reponse = sc.api_call("chat.postMessage", channel="#tacotest", text="<@" + reciever + "> now has: " + str(taco_dict[reciever]) + " tacos!")
            reponse = sc.api_call("chat.postMessage", channel=dm.get("id"), as_user=False, text= "You have given " + str(5 -taco_give_dict[sender]) + " tacos today. You have " + str(taco_give_dict[sender]) + " tacos remaining today.")
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
        taco_give_dict[user.get("id")] = 5
        taco_dict[user.get("id")] = 0
        print user.get("id")


if sc.rtm_connect():
    while True:
        events = sc.rtm_read()
        print events
        for evt in events:
            if(evt["type"] == "message"):
                isThisValid(evt)
        time.sleep(1)
else:
    print "Connection Failed, invalid token?"







