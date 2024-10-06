from flask import Flask, request
import requests,json
import os
from pymessenger import Bot

from utils import fetch_reply, match_det, HELP_MSG,cur_match, data
from config import FB_ACCESS_TOKEN, VERIFICATION_TOKEN

app=Flask("Cricbot")
bot=Bot(FB_ACCESS_TOKEN)

@app.route('/',methods=['GET'])
def verify():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == VERIFICATION_TOKEN:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return "Hello world! This is Cricbot.", 200


@app.route('/', methods=['POST'])
def webhook():
	data = request.get_json()
	#print(data)
	if data['object'] == "page":
		entries = data['entry']

		for entry in entries:
			messaging = entry['messaging']

			for messaging_event in messaging:

				sender_id = messaging_event['sender']['id']
				if sender_id=='803956049791378':
					return "ok",200
				recipient_id = messaging_event['recipient']['id']

				if messaging_event.get('message'):
					try:
						# HANDLE NORMAL MESSAGES HERE
						if messaging_event['message'].get('text'):
							# HANDLE TEXT MESSAGES
							query = messaging_event['message']['text']
							bot.send_action(sender_id,"mark_seen")
							bot.send_action(sender_id,"typing_on")

							if messaging_event['message'].get('quick_reply'):
								# HANDLE TEXT MESSAGE WITH QUICK REPLY
								payload = messaging_event['message']['quick_reply']['payload']
								li=cur_match()
								if li=="Error":
									bot.send_text_message(sender_id,"Unable to process your request due to some technical issues. Please try again later.")
									return "ok",200
								for i in li:
									if payload in i[1]:
										query = payload
										break
							try :
								#handle any error in utils.py
								reply=fetch_reply(query,sender_id)
							except Exception as e:
								print(e)
								print("here1\n")
								reply={}
								reply['type']="none"
								reply['data']="Sorry"

							if reply['type']=="match_detail":
								#to show details of all live messages
								#print(reply['data'])
								bot.send_generic_message(sender_id, reply['data'])

							elif reply['type']=="live_score":
								#to show detail of a particular match
								#print(reply['data'])
								if "button" in reply.keys():
									buttons = [{"type":"web_url",
									"url": reply['button'],
								    "title":"Scorecard"}]
									bot.send_button_message(sender_id,reply['data'],buttons)
								else:
									bot.send_text_message(sender_id,reply['data'])

							elif reply['type']=="match_info":
								#print(reply['data'])
								#to show info like venue, umpires, refree of a particular match
								bot.send_text_message(sender_id,reply['data'])

							elif reply['type']=='ranking_t':
								#to show team rankings of test, ODI, T20i and women
								s1=reply['data'][-1]+"\n\n"
								excepti=['Zimbabwe',"Hong Kong"]
								reply['data'].pop()
								for i in reply['data']:
									s=""
									s+=str(i.get("rank"))
									s+=" \t"
									s+=i.get("team")
									if len(i.get('team').rstrip(' Women'))<10 and i.get('team') not in excepti:
										if "India Women" in i.get('team') or i.get('team')=="UAE" or i.get("team")=="PNG":
											s+="\t"
										s+="\t\t"
									else:
										s+="\t"
									s+="  "
									s+=i.get("rating")+"\n"
									s1+=s
								s1+="\nP.S.: Ratings in brackets\n"
								bot.send_text_message(sender_id,s1)

							elif reply['type']=="ranking_p":
								# to show players ranking in odi, t20i and test in batting, bowling and all-rounder
								s1=reply['data'][-1]+"\n\n"
								reply['data'].pop()
								button_url=reply['data'][-1]['button_url']
								reply['data'].pop(-1)
								for i in reply['data']:
									s=""
									s+=i.get("rank")
									s+=" \t"
									s+=i.get("player")
									if len(i.get('player'))<10:
										s+='\t\t'
									else:
										s+='\t'
									s+=" "
									s+=i.get("country")+" \t"
									s+=i.get("rating")+"\n"
									s1+=s
								s1+="\nP.S.: Ratings in brackets\n"
								buttons = [{"type":"web_url",
									"url": button_url,
								    "title":"Complete list"}]
								bot.send_action(sender_id,"typing_off")
								bot.send_button_message(sender_id,s1,buttons)
							elif reply['type'] == 'none':
								#to handle anything that bot doesn't understand
								button=[{
								"type":"postback",
								"title":"Click here for help",
								"payload":"help"
								}]
								bot.send_button_message(sender_id, "Sorry, I didn't understand.",button)

							elif reply['type']=="offline":
								#Status code error
								bot.send_text_message(sender_id,reply['data'])

							else:
								#mainly to handle smalltalks
								print(reply['data'])
								bot.send_text_message(sender_id, reply['data'])
						elif messaging_event['message'].get('attachments'):
							#HANDLE ATTACHMENTS
							try:
								image_url=messaging_event['message']['attachments'][0]['payload']['url']
								bot.send_image_url(sender_id,image_url)
							except Exception as e:
								print(e)
								print("here2\n")
					except Exception as e:
						print(e)
						print("here3\n")
						bot.send_text_message(sender_id,"Unable to process your request due to some technical issues. Please try again later.")
				
				elif messaging_event.get("postback"):
					payload=messaging_event['postback']['payload']
					try:
						if payload=="match_detail":
							data=match_det()
							if data=="Error":
								bot.send_text_message(sender_id,"Unable to process your request due to some technical issues. Please try again later.")
							else:
								bot.send_generic_message(sender_id,data)
						elif payload=="live_score":
							quick_reply=cur_match()[:10]
							if quick_reply=="Error":
								bot.send_text_message(sender_id,"Unable to process your request due to some technical issues. Please try again later.")
							else:
								bot.send_quickreply(sender_id,HELP_MSG,cur_match()[:10])
						elif payload=='help':
							bot.send_text_message(sender_id,"Hello I am Cricbot. I can show you details like live scores and match info of all the ongoing cricket matches.:)")
							bot.send_text_message(sender_id,"For checking live scores, type 'team_name1 vs team_name2' and you will get live scores of that match.")
							bot.send_text_message(sender_id,"For match info, type 'team_name1 vs team_name2 match info'.\nAnd for ICC team and player ranking, type <format> ranking.\nFor example: for test cricket ranking, type test ranking. ")
							bot.send_text_message(sender_id,"If u still need any help, use persistent menu.")
							button=[{
							'type':'web_url',
							'title':"Meet the developer",
							'url':'https://www.facebook.com/MohitBansal97'
							}]
							bot.send_button_message(sender_id,"For any suggestion or query, contact my botmaster",button)
					except Exception as e:
						print(e)
						button=[{
						"type":"postback",
						"title":"Click here for help",
						"payload":"help"
						}]
						bot.send_button_message(sender_id, "Sorry, I didn't understand.",button)
						
	return "ok", 200
	

def set_greeting_text():
    headers = {
        'Content-Type':'application/json'
        }
    data = {
        "setting_type":"greeting",
        "greeting":{
            "text":"Hi {{user_first_name}}! I am Cricbot. I can show you details like live scores and match info of all the ongoing cricket matches.:)"
            }
        }
    ENDPOINT = "https://graph.facebook.com/v2.8/me/thread_settings?access_token=%s"%(FB_ACCESS_TOKEN)
    r = requests.post(ENDPOINT, headers = headers, data = json.dumps(data))
    #print(r.content)


def set_persistent_menu():
    headers = {
        'Content-Type':'application/json'
        }
    data = {
        "setting_type":"call_to_actions",
        "thread_state" : "existing_thread",
        "call_to_actions":[
            {
                "type":"web_url",
                "title":"Meet the developer",
                "url":"https://www.facebook.com/MohitBansal97" 
            },{
            "type":"postback",
            "title":"Live Matches",
            "payload":"match_detail"
            },{
            "type":"postback",
            "title":"Live Scores",
            "payload":"live_score"
            },{
            "type":"postback",
            "title":"Help",
            "payload":"help"
            }]
        }
    ENDPOINT = "https://graph.facebook.com/v2.8/me/thread_settings?access_token=%s"%(FB_ACCESS_TOKEN)
    r = requests.post(ENDPOINT, headers = headers, data = json.dumps(data))


def get_started():
    headers = {
        'Content-Type':'application/json'
        }
    data = {
        "setting_type":"call_to_actions",
        "thread_state" : "new_thread",
        "call_to_actions":[{
            "type":"postback",
            "payload":"help"
            }]
        }
    ENDPOINT = "https://graph.facebook.com/v2.8/me/thread_settings?access_token=%s"%(FB_ACCESS_TOKEN)
    r = requests.post(ENDPOINT, headers = headers, data = json.dumps(data))

set_persistent_menu()
set_greeting_text()
get_started()

if __name__=="__main__":
	app.run(port=8000,use_reloader=True)
