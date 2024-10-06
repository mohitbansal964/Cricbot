import apiai
import json
from requests import *
from bs4 import BeautifulSoup
from datetime import date
from pymongo import MongoClient

from config import APIAI_ACCESS_TOKEN, MONGODB_URI, db_name

client = MongoClient(MONGODB_URI)
db = client.get_database(db_name)
data = db.data

# a help message
HELP_MSG = """
Hey! I am Cricbot.:).
Choose any one of the ongoing matches.:)
"""

cric_url="http://www.cricbuzz.com/cricket-match/live-scores"

def insertion():
	print("\n\nin insertion\n\n")
	r=get(cric_url)
	l="Error"
	if r.status_code==200:
		soup=BeautifulSoup(r.content,"html5lib")
		matches=soup.findAll(class_="cb-col cb-col-100 cb-lv-main")
		l=[]
		for i in range(len(matches)):
			a=matches[i].findAll("a")
			teams=a[0].text
			t1=teams.split(" vs ")[0]
			t2=teams.split(" vs ")[1].rstrip(",")
			l.append((t1.lower(),t2.lower()))
	else:
		url="http://www.espncricinfo.com/ci/engine/match/index.html?view=live"
		r=get(url)
		l=[]
		if r.status_code==200:
			soup=BeautifulSoup(r.content,"html5lib")
			matches=soup.findAll("section",class_="default-match-block")
			for match in matches:
				preview=match.find('div',class_='innings-info-1')
				ts1=preview.text.strip().replace("    "," ")
				ts2=match.find('div',class_='innings-info-2').text.strip().replace("    "," ")
				t1=ts1.strip(match.find('div',class_='innings-info-1').find('span').text)
				t2=ts2.strip(match.find('div',class_='innings-info-2').find('span').text)
				l.append((t1.lower(),t2.lower()))
	return l
def espn_scrape():
	# if cricbuzz scraping has any error, then scrape from espncricinfo
	url="http://www.espncricinfo.com/ci/engine/match/index.html?view=live"
	cric_url=url
	r=get(url)
	l=[]
	if r.status_code==200:
		soup=BeautifulSoup(r.content,"html5lib")
		matches=soup.findAll("section",class_="default-match-block")
		for match in matches:
			try:
				preview=match.find('div',class_='innings-info-1')
				if preview.find('span').text=="":
					continue
				d={}
				d['flag']=1
				d['team_score1']=preview.text.strip().replace("    "," ")
				d['team_score2']=match.find('div',class_='innings-info-2').text.strip().replace("    "," ")
				d['result']=match.find('div',class_="match-status").text.strip()
				d['team1']=d['team_score1'].strip(match.find('div',class_='innings-info-1').find('span').text)
				d['team2']=d['team_score2'].strip(match.find('div',class_='innings-info-2').find('span').text)
				d['scorecard_url']=match.find('a')['href'].replace('game','scorecard')
				d['commentary_url']=match.find('a')['href'].replace('game','commentary')
				d['match_facts_url']=match.find('a')['href']
				l.append(d)
			except:
				pass
	else:
		l="Error"
	return l

def scrape():
	"""
	function to get live scores from cricbuzz
	"""
	r=get(cric_url)
	if r.status_code==200:
		soup=BeautifulSoup(r.content,"html5lib")
		matches=soup.findAll(class_="cb-col cb-col-100 cb-lv-main")
		l=[]
		for i in range(len(matches)):
			try:
				a=matches[i].findAll("a")
				if "preview" in a[1]['class'][1]:
					continue
				s=matches[i].findAll("span")
				d={}
				d['flag']=0
				teams=a[0].text
				d['team1']=teams.split(" vs ")[0]
				d['team2']=teams.split(" vs ")[1].rstrip(",")
				score=a[1].text.split("\xa0•\xa0")
				d['team_score1']=score[0].strip()
				xyz=a[1].find(class_="cb-lv-scrs-col cb-text-live")
				if xyz:
					reslt=a[1].find(class_="cb-lv-scrs-col cb-text-live").text
					team_score2=score[1].replace(reslt," ").strip()
					d['team_score2']=team_score2
					d['result']=reslt
				else:
					reslt=a[1].find(class_="cb-lv-scrs-col cb-text-complete").text
					team_score2=score[1].replace(reslt," ").strip()
					d['team_score2']=team_score2
					d['result']=reslt
				if "opt" in d['result']:
					d['team_score1'],d['team_score2']=d['team_score2'],d['team_score1']
				d['scorecard_url']="http://www.cricbuzz.com"+a[3]['href']
				d['commentary_url']="http://www.cricbuzz.com"+a[4]['href']
				d['match_facts_url']=d['commentary_url'].replace("full-commentary","match-facts")
				l.append(d)
			except:
				pass
	else:
		l=espn_scrape()
	return l


def match_det():
	scores = scrape()
	if scores=="Error":
		return scores
	# create generic template
	diff_matches = []
	count=1
	for match in scores:
		if count>10:#max number of templates can only be 10
			break
		element = {}
		element["title"] = match['team1']+" vs "+match['team2']
		element['subtitle']=match['team_score2']+"\xa0•\xa0"+match['team_score1']+'\n'+match['result']
		element["item_url"]=cric_url
		element["buttons"] = [{
			"type":"web_url",
			"title":"Scorecard",
			"url":match["scorecard_url"]},
			{"type":"web_url",
            "title":"Full Commentary",
            "url":match['commentary_url']}]
		diff_matches.append(element)
		count+=1
	return diff_matches


def live_score(params):
	l=scrape()
	if l=="Error":
		return l
	#Check if match between given teams exists or not
	teams=params.get("teams")
	team1=teams[0].lower().strip()
	team2=teams[1].lower().strip()
	for i in l:
		if i.get("team1").lower()==team1 or i.get("team2").lower()==team1:
			if i.get("team1").lower()==team2 or i.get("team2").lower()==team2:
				return i
	return "error"


def match_facts(params):
	ls=live_score(params)
	if ls=="Error" or ls=="error":
		return ls
	s=""
	if ls["flag"]==0:
		url=ls['match_facts_url']
		r=get(url)
		soup=BeautifulSoup(r.content,"html5lib")
		info_h=soup.findAll(class_="cb-col cb-col-27 cb-mat-fct-itm text-bold")
		info_b=soup.findAll(class_="cb-col cb-col-73 cb-mat-fct-itm")
		for i in range(8):
			s+="{} {}\n\n".format(info_h[i].text,info_b[i].text)
	elif ls['flag']==1:
		url=ls['match_facts_url']
		r=get(url)
		soup=BeautifulSoup(r.content,"html5lib")
		info_h=soup.findAll("div",class_="match-detail--left")
		info_b=soup.findAll("div",class_="match-detail--right")
		s=""
		for i in range(len(info_b)):
		    s+=str(info_h[i].text)+" "
		    a=info_b[i].findAll("span")
		    for j in range(len(a)):
		        if len(a)>1 and j!=len(a)-1:
		            s+=str(a[j].text)+", "
		        else:
		            s+=str(a[j].text)
		    s+="\n\n"
	return s


def cur_match():
	l=scrape()
	if l=="Error":
		return l
	#Creating quick reply
	reply=[]
	if l[0]['flag']==0:
		for i in l:
			team1=i.get("team_score1").split()[0]
			team2=i.get("team_score2").split()[0]
			match=team1+" vs "+team2
			postback=i.get("team1") +" vs "+i.get("team2")+" live scores"
			reply.append((match,postback))
	elif l[0]['flag']==1:
		for i in l:
			team1=i.get("team1")
			team2=i.get("team2")
			match=team1+" vs "+team2
			postback=i.get("team1") +" vs "+i.get("team2")+" live scores"
			reply.append((match,postback))
	return reply


def ranking_t(params):
	#function to team ranking from espncricinfo
	match_type=["Test","ODI","T20i"]
	url="http://www.espncricinfo.com/rankings/content/page/211271.html"
	r=get(url)
	if r.status_code==200:

		soup=BeautifulSoup(r.content,"html5lib")
		table=soup.findAll('table')
		tables_t=[]
		for i in range(len(table)):
			tbody=table[i].find("tbody")
			team=tbody.findAll("tr")
			li=[]
			for j in range(1,len(team)):
				data=team[j].findAll("td")
				d={}
				d['rank']=j
				d['team']=data[0].text
				d['rating']="({})".format(data[3].text)
				li.append(d)
			tables_t.append(li)
		x=params.get('Type')
		if len(x)==0:
			x.append("Test")
		if "Women" in x:
			tables_t[3].append("Women's Rankings")
			l=tables_t[3]
			return l
		for i in range(3):
			if match_type[i] in x:
				tables_t[i].append(match_type[i]+" Ranking")
				l=tables_t[i]
				return l
	else:
		return "Error"

def ranking_p(params):
	#Function to scrape player ranking from espncricinfo
	url="http://www.espncricinfo.com/rankings/content/page/211270.html"
	r=get(url)
	if r.status_code==200:
		soup=BeautifulSoup(r.content,"html5lib")
		frames=soup.findAll('iframe')
		tables_p=[]
		button_url="https://www.icc-cricket.com/rankings/mens/player-rankings/test/batting"
		li=[("mens","test","batting"),("mens","test","bowling"),("mens","test","all-rounder"),("mens","odi","batting"),("mens","odi","bowling"),
		("mens","odi","all-rounder"),("mens","t20i","batting"),("mens","t20i","bowling"),("mens","t20i","all-rounder"),("womens","odi","batting"),
		("womens","odi","bowling"),("womens","odi","all-rounder"),("womens","t20i","batting"),("womens","odi","bowling"),
		("womens","t20i","all-rounder")]
		x=params.get("Type")
		i=0
		heading=""
		if "Women" in x:
			if "ODI" not in x and "T20i" not in x:
				x.append("ODI")
			if "Batting" not in x and "Bowling" not in x and "All-rounder" not in x:
				x.append("Batting")
			if "Test" in x:
				x.replace("Test","ODI")
			x=list(map(lambda x:x.lower(),x))
			for i in range(9,15):
				if li[i][1] in x and li[i][2] in x :
					break
			heading="Women's "+li[i][1].capitalize()+" "+li[i][2].capitalize()+" Ranking"
		else:
			if "ODI" not in x and "T20i" not in x and "Test" not in x:
				x.append("Test")
			if "Batting" not in x and "Bowling" not in x and "All-rounder" not in x:
				x.append("Batting")
			x=list(map(lambda x:x.lower(),x))
			for i in range(0,9):
				if li[i][1] in x and li[i][2] in x :
					break
			heading=li[i][1].capitalize()+" "+li[i][2].capitalize()+" Ranking"
		r1=get(frames[i]['src'])
		if r1.status_code==200:
			sp=BeautifulSoup(r1.content,"html5lib")
			tb=sp.findAll('tr')
			l=[]
			for j in range(2,len(tb)-1):
				d={}
				td=tb[j].findAll('td')
				d['rank']=td[0].text
				d['player']=td[1].text
				d['country']=td[2].text
				d['rating']="({})".format(td[3].text)
				l.append(d)
			req_url=button_url.replace("mens",li[i][0])
			req_url=req_url.replace("test",li[i][1])
			req_url=req_url.replace("batting",li[i][2])
			d={}
			d['button_url']=req_url
			l.append(d)
			heading=heading.replace("Odi","ODI")
			l.append(heading)
			return l
		else:
			return "Error"
	else:
		return "Error"

def apiai_response(query, session_id):
	"""
	function to fetch api.ai response
	"""
	
	ai = apiai.ApiAI(APIAI_ACCESS_TOKEN)
	request = ai.text_request()
	request.lang='en'
	request.session_id=session_id
	request.query = query
	response = request.getresponse()
	return json.loads(response.read().decode('utf8'))


def parse_response(response):
	"""
	function to parse response and
	return intent and its parameters
	"""
	result = response['result']
	params = result.get('parameters')
	intent = result['metadata'].get('intentName')
	return intent, params


def fetch_reply(query, session_id):
	"""
	main function to fetch reply for chatbot and
	return a reply dict with reply 'type' and 'data'
	"""
	response = apiai_response(query, session_id)
	intent, params = parse_response(response)
	print(intent,params)
	if params.get('teams'):
		l_team=[]
		for i in params['teams']:
			l_team.append(i.strip())
		params['teams']=l_team
	reply = {}
	d=data.find_one({'date':str(date.today())})
	if d is None:
		d1={}
		d1['date']=str(date.today())
		l=insertion()
		d1['data']=l
		if l!="Error":
			data.insert_one(d1)
		d=d1

	if response['result']['action'].startswith('smalltalk') or intent=="Default Welcome Intent":
		reply['type'] = 'smalltalk'
		reply['data'] = response['result']['fulfillment']['speech']

	elif intent == "match_detail":
		reply['type'] = 'match_detail'
		templates=match_det()
		if templates=="Error":
			reply['type']="offline"
			reply['data']="Unable to process your request due to some technical issues. Please try again later."
		else:
			reply["data"] = templates

	elif intent=="live_score":
		reply['type']="live_score"
		teams=params.get('teams')
		if len(teams)==2:
			team1=teams[0].lower()
			team2=teams[1].lower()
			if d['data']=="Error":
				score="Error"
			else:
				for match in d['data']:
					if (team1 in match[0] or team2 in match[0]) and (team2 in match[1] or team1 in match[1]):
						score=live_score(params)
						break
				else:
					score="error"
		else:
			score='Error'
		if score=="Error":
			reply['type']="offline"
			reply['data']="Unable to process your request due to some technical issues. Please try again later."
		elif score=="error":
			teams=params.get("teams")
			reply['data']="Sorry, there is no match between {} and {}".format(teams[0],teams[1])
		else:
			reply['data']="{} vs {}\n\n{}\n{}\n\n{}".format(score['team1'],score['team2'],score['team_score2'],score['team_score1'],score['result'])
			reply['button']=score['scorecard_url']

	elif intent=="match_info":
		s=match_facts(params)
		reply['type']="match_info"
		if info_b=="Error":
			reply['type']="offline"
			reply['data']="Unable to process your request due to some technical issues. Please try again later."
		if info_h=="error":
			teams=params.get("teams")
			reply['data']="Sorry, no match between {} and {}".format(teams[0],teams[1])
		else:
			reply['data']=s

	elif intent=="ranking":
		reply['type']="ranking_t"
		x=params.get('Type')
		if "Player" in params.get('Type') or "Batting" in x or "Bowling" in x or "All-rounder" in x :
			if "Player" not in x:
				params['Type']+=["Player"]
			reply['type']="ranking_p"
			rank=ranking_p(params)
			if rank=="Error":
				reply['type']="offline"
				reply['data']="Unable to process your request due to some technical issues. Please try again later."
			else:
				reply['data']=rank
		else:
			rank=ranking_t(params)
			if rank=="Error":
				reply['type']="offline"
				reply['data']="Unable to process your request due to some technical issues. Please try again later."
			else:
				reply['data']=rank
	else:
		reply["type"] = 'none'
		reply["data"] = ""

	return reply
