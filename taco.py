from slackclient import SlackClient
import os
import time
import re


def parseMessagess(evt):
    num_tacos = len(re.findall(":taco:", evt["text"]))
    users = re.findall("<@.........>", evt["text"])
    if num_tacos > 0:
        for uid in users:
            uid = uid.replace("<@", "")
            uid =uid.replace(">", "")
            tacoLogic(uid, evt, num_tacos)
    elif "<@U6HC2N4AD>" in evt["text"] and "leaderboard" in evt["text"]:
        sc.api_call("chat.postMessage", channel=evt["channel"], text= "um... not ready yet")
    elif "<@U6HC2N4AD>" in evt["text"] and "stats <@" in evt["text"]:
        for uid in users:
            if uid == "<@U6HC2N4AD>":
                continue
            uid_fix = uid.replace("<@", "")
            uid_fix =uid_fix.replace(">", "")
            # username = sc.api_call("users.profile.get", user=uid, include_labels=False)
            sc.api_call("chat.postMessage", channel=evt["channel"], text= str(uid) + " has recieved " + str(taco_dict[uid_fix]) + " tacos and given " + str(taco_lifetime[uid_fix]) + " tacos!")

def tacoLogic(uid, evt, num_tacos):
    sender = evt["user"]
    reciever = uid
    if sender == reciever:
        return
    if reciever in taco_dict and sender in taco_give_dict:
        if taco_give_dict[sender] >= num_tacos:
            taco_give_dict[sender]-= num_tacos
            taco_lifetime[sender] += num_tacos
            taco_dict[reciever] += num_tacos
            dm_sender = sc.api_call("im.open", user=sender)
            dm_reciever = sc.api_call("im.open", user=reciever)
            reponse = sc.api_call("chat.postMessage", channel=dm_reciever.get("channel").get("id"), text="You have recieved " + str(num_tacos) + " tacos from <@" + sender + ">! You have: " + str(taco_dict[reciever]) + " tacos!")
            reponse = sc.api_call("chat.postMessage", channel=dm_sender.get("channel").get("id"), as_user=False, text= "You have given " + str(5 -taco_give_dict[sender]) + " tacos today. You have " + str(taco_give_dict[sender]) + " tacos remaining today.")
        else:
            reponse = sc.api_call("chat.postMessage", channel="#tacotest", text="Not enough tacos to give today, try again tomorrow")




token = os.environ["SLACK_API_TOKEN"]
sc = SlackClient(token)

taco_dict = {}
taco_give_dict = {}
taco_lifetime = {}

def init_map():
    api_call = sc.api_call("users.list")
    if api_call.get('ok'):
        users = api_call.get("members")
        for user in users:
            uid = user["id"]
            taco_give_dict[uid] = 5
            taco_dict[uid] = 0
            taco_lifetime[uid] = 0
            print uid

def start_listening():
    if sc.rtm_connect():
        while True:
            events = sc.rtm_read()
            print events
            for evt in events:
                if(evt["type"] == "message"):
                    parseMessagess(evt)
            time.sleep(1)
    else:
        print "Connection Failed, invalid token?"

init_map()
start_listening()





