import requests
import bs4
import re
import hashlib
import json
import pickle
import tqdm
#https://blog.scrapinghub.com/2017/07/07/scraping-the-steam-game-store-with-scrapy
#https://stackoverflow.com/questions/56359915/how-to-scrape-dynamic-review-content-from-steam-using-beautifulsoup-and-python

getIDs = True

class review:
	def __init__(self, body, label, score):
		self.corpus = body
		self.label = label
		self.score = score #tuple of (good, funny)
		self.hash = hashlib.md5(bytes(body, 'utf-8')).hexdigest()
	def __str__(self):
		return (self.label + '\n' + "'good' ratings: "+self.score[0] +'\n'+"'funny' ratings: "+self.score[1] + '\n' + self.corpus + '\n'+ "md5: " + self.hash +'\n'+'#'*50)
		
if getIDs:
	req = requests.get('http://api.steampowered.com/ISteamApps/GetAppList/v2')
	jason = json.loads(req.text)
	ids = []
	for i in jason['applist']['apps']:
		ids.append(str(i['appid']))
	print("there are", len(ids),"appids")
	with open ('IDs.txt','w') as outfile:
		json.dump(ids,outfile)
else:
	with open ('IDs.txt','r') as infile:
		ids = json.load(infile)
reviews = []
hashlist = []#a list of md5 hashses of reviews that have been collected
IDsWithData=[]
outfile = open('Reviews.p','wb')
newIDs = open('IDs2.txt','w')
count = 0
numreviews = 0
for gameID in tqdm.tqdm(ids):
	if count % 100 == 0 and count != 0:
		print('we have',numreviews,'reviews')
	count += 1
	for review_type in ['positive','negative']:
		url = 'https://store.steampowered.com/appreviews/'+str(gameID)+'?json=1&num_per_page=50&start_offset=0&day_range=9223372036854776000&language=english&filter=all&review_type='+review_type
		regex = re.compile('apphub_CardContentAuthorName')
		response = requests.get(url,headers={'User-Agent': 'Mozilla/5.0'})
		if response.status_code == 200:
			myjson = json.loads(response.text)
		else:
			break

		if myjson.get('success') == 1 and myjson['query_summary']['num_reviews'] > 0:
			if str(gameID) not in IDsWithData:
				IDsWithData.append(str(gameID))
			for reviewBox in myjson['reviews']:
				content = reviewBox['review']
				if reviewBox['voted_up']:
					label = "Recommended"
				else:
					label = "Not Recommended"
				good = str(reviewBox['votes_up'])
				funny = str(reviewBox['votes_funny'])
				myReview = review(content,label,(good,funny))
				if myReview.hash in hashlist:
					pass
				else:
					#reviews.append(myReview)
					numreviews +=1
					hashlist.append(myReview.hash)
					pickle.dump(myReview,outfile)
		else:
			break
			
json.dump(IDsWithData,newIDs)
print(len(reviews))

