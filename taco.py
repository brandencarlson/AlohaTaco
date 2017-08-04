from slackclient import SlackClient
import os
import time
import re
import operator

aloha_taco_id = "<@U6HC2N4AD>"
token = os.environ["SLACK_API_TOKEN"]
sc = SlackClient(token)

taco_dict = {}
taco_give_dict = {}
taco_lifetime = {}
id_to_handle = {}

def parseMessage(evt):
    text = evt["text"]
    num_tacos = len(re.findall(":taco:", text))
    users = re.findall("<@.........>", text)
    if num_tacos > 0:
        for uid in users:
            uid = uid.replace("<@", "").replace(">", "")
            tacoLogic(uid, evt, num_tacos)
    elif aloha_taco_id in text and "leaderboard" in text:
        sc.api_call("chat.postMessage", channel=evt["channel"], text = get_leaderboard(4))
    elif aloha_taco_id in text and "stats <@" in text:
        for uid in users:
            if uid == aloha_taco_id:
                continue
            uid_fix = uid.replace("<@", "").replace(">", "")
            # username = sc.api_call("users.profile.get", user=uid, include_labels=False)
            sc.api_call("chat.postMessage", channel=evt["channel"], text=get_stats(uid_fix))

def tacoLogic(uid, evt, num_tacos):
    sender = evt["user"]
    reciever = uid
    if sender == reciever:
        return
    if reciever in taco_dict and sender in taco_give_dict:
        if taco_give_dict[sender] >= num_tacos:
            taco_give_dict[sender] -= num_tacos
            taco_lifetime[sender] += num_tacos
            taco_dict[reciever] += num_tacos
            dm_sender = sc.api_call("im.open", user=sender)
            dm_reciever = sc.api_call("im.open", user=reciever)
            reponse = sc.api_call("chat.postMessage", channel=dm_reciever.get("channel").get("id"), text="You have recieved " + str(num_tacos) + " tacos from <@" + sender + ">! You have: " + str(taco_dict[reciever]) + " tacos!")
            reponse = sc.api_call("chat.postMessage", channel=dm_sender.get("channel").get("id"), as_user=False, text= "You have given " + str(5 -taco_give_dict[sender]) + " tacos today. You have " + str(taco_give_dict[sender]) + " tacos remaining today.")
        else:
            reponse = sc.api_call("chat.postMessage", channel="#tacotest", text="Not enough tacos to give today, try again tomorrow")



def init_map():
    api_call = sc.api_call("users.list")
    if api_call.get('ok'):
        users = api_call.get("members")
        for user in users:
            uid = user["id"]

            taco_give_dict[uid] = 5
            taco_dict[uid] = 0
            taco_lifetime[uid] = 0

            id_to_handle[uid] = user["name"]
            print uid + " " + user["name"]

def reset_daily_tacos():
    api_call = sc.api_call("users.list")
    if api_call.get('ok'):
        users = api_call.get("members")
        for user in users:
            uid = user["id"]
            taco_give_dict[uid] = 5
            if user["name"] != id_to_handle[uid]:
                id_to_handle[uid] = user["name"]

def start_listening():
    if sc.rtm_connect():
        while True:
            events = sc.rtm_read()
            print events
            for evt in events:
                if(evt["type"] == "message"):
                    parseMessage(evt)
            time.sleep(1)
    else:
        print "Connection Failed, invalid token?"

def get_leaderboard(n):
    top_n = sorted(taco_dict.items(), key=operator.itemgetter(1), reverse = True)[:n]
    print(top_n)
    s = "*salesforceIQ Leaderboard*\n"
    for i in range(n):
        user = top_n[i]
        print user
        if user[1] > 0:
            s += str(i+1) + "). " + id_to_handle[user[0]] + "  *" + str(user[1]) + "*\n"
    return s

def get_stats(uid):
    s = str(uid) + " has recieved " + str(taco_dict[uid_fix]) + " tacos and given " + str(taco_lifetime[uid_fix]) + " tacos!"
    return s

init_map()
start_listening()





