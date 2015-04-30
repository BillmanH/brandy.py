#Calcualting Response Time
'''
Built for Brandwach by William Harding and Tahzoo
http://tahzoo.com/
www.linkedin.com/in/hardingwilliam

Feel free to use as-is and let me know if you have improvements/bug-fixes

<indicate user input>
'''
#Response Time:
from brandy import *
import math

#Starting Functions to get you logged in:
project_list, access_token = boot_api()
project_id = <your project id>
query_list = get_query_id(project_id,access_token)
#if this is your first time logging into BW, you might want to check out the brandy.py documentation


myWorkDirectory = r"C:\Users\Bill\Desktop\Reach out to us at Tahzoo.com"

request_URL = get_mentions_query_URL('2015-04-01','2015-04-29',project_id,query_id,access_token,True)
mentions = get_mentions_data(request_URL)
data = pd.DataFrame(mentions['results'])

owner = <the FB id of the company page you want to study>

#here is a list of the columns that are relevant to this study. I preffer to work with as few columns as possible.
data = data[['author', 'facebookAuthorId','threadId','threadCreated','date','avatarUrl','url','engagement',
	'facebookComments', 'facebookLikes', 'facebookRole',
	'facebookShares', 'facebookSubtype', 'forumPosts', 'forumViews','id','impact',
	'resourceId','sentiment','snippet','fullText']]


#DataCleaneing: 
#Marked one particular post that was confusing my dataset.
for i in range(len(data)):
	myUrl = data.loc[i,'url']
	if "<page id from URL that I want to exclude>" in myUrl:
		data.loc[i,'Not_part_of_this_study'] = 1
#Removed carriage returns, will be a problem later.
for i in range(len(data)):
	mytext = data.loc[i,'fullText'] 
	mytext = mytext.replace('\r'," ")
	mytext = mytext.replace('\n'," ")
	data.loc[i,'fullText'] = mytext

data = data.sort('date').reset_index(drop=True)
#End Data Cleaning Section, on with the analysis

#Getting the subset of data that I want to look at.
#in this case, I wanted to look at negative mentions that were popular. You can use the same logic to define your own query. 
negative_posts = data[data['sentiment']=="negative"]
#I'm looking at the audience posts, so for this subset I'm kicking out all of the owner mentions.
negative_posts = negative_posts[negative_posts["facebookRole"]!='owner'].reset_index(drop=True)
#negative posts that were liked at least once
popular_neg_posts = negative_posts[negative_posts['facebookLikes']!=0]
#in order to triage, I made the list to show the ones that have at least one like. 
popular_neg_posts = popular_neg_posts.sort('facebookLikes',ascending=False).reset_index(drop=True)


#Analyse bad conversations:
#this is just the quick way to measure those conversations on a 1:1 level.
threadID = <Thread ID that you want to look at>
	
def StudyConversation(threadID):
	badConvo = data[data['threadId']==str(threadID)]
	ownerResponse = badConvo[badConvo['facebookAuthorId']==owner]
	print "Total conversation length " + str(len(badConvo))
	print "number of owner mentions: " + str(len(badConvo[badConvo['facebookRole']=="owner"]))
	print "number of unique participants mentions: " + str(len(np.unique(badConvo['facebookAuthorId'])))
	print "positive mentions for every negative mention: " + str(float(len(badConvo[badConvo['sentiment']=="positive"]))/float(len(badConvo[badConvo['sentiment']=="negative"])))
	print "Owner mentions for every negative mention: " + str(float(len(badConvo[badConvo['facebookRole']=="owner"]))/float(len(badConvo[badConvo['sentiment']=="negative"])))
	print "Owner likes in this post:", ownerResponse.facebookLikes.sum()

StudyConversation(threadID)
	
#to create a dataframe of all of the threads in the study:
def owner_audience_interaction(DF):
	newDF = pd.DataFrame()
	for thread in np.unique(DF['threadId']):
		Convo = data[data['threadId']==str(thread)]
		ownerResponse = Convo[Convo['facebookAuthorId']==owner]
		newDF.loc[thread,'conversation_length'] = len(Convo)
		newDF.loc[thread,'owner_mentions'] = len(Convo[Convo['facebookRole']=="owner"])
		newDF.loc[thread,'unique_participants'] = len(np.unique(Convo['facebookAuthorId']))
		if len(Convo[Convo['sentiment']=="negative"]) != 0:
			newDF.loc[thread,'pos_to_neg_mentions'] = float(len(Convo[Convo['sentiment']=="positive"]))/float(len(Convo[Convo['sentiment']=="negative"]))
			newDF.loc[thread,'own_per_neg_mention'] = float(len(Convo[Convo['facebookRole']=="owner"]))/float(len(Convo[Convo['sentiment']=="negative"]))
		else:
			newDF.loc[thread,'pos_to_neg_mentions'] = 0
			newDF.loc[thread,'own_per_neg_mention'] = 0
		newDF.loc[thread,'owner_likes'] = ownerResponse.facebookLikes.sum()
	return newDF
	
studyDF = owner_audience_interaction(negative_posts)


#the owner will usually mention the author in a mention by name.
#you can use the mention of the name and the author name to determine which person the author is responding.
def add_response_time(DF):	
	newDF = DF.copy()
	for i in range(len(DF)):
		thread = DF.threadId[i]
		authorName = DF.author[i].split(" ")
		subset = data[data['threadId']==str(thread)].sort('date').reset_index(drop=True)
		subset = subset[['threadId','author','threadCreated','date','snippet','fullText','facebookAuthorId','sentiment']].reset_index(drop=True)
		mentionTime = iso_to_epoch(DF.date[i])
		subset = add_epoch_date(subset)
		subset = subset[subset['epoch']>=mentionTime]
		OwnerMentioned = mentionTime
		#print np.array(subset.author)
		if owner not in subset['facebookAuthorId'].values:
			newDF.loc[i,"ResponseTime"] = np.nan
			newDF.loc[i,"Responded"] = False
		else: 
			companyMentions = subset[subset['facebookAuthorId']==owner].date.values
			mentions = subset[subset['facebookAuthorId']==owner].reset_index(drop=True)
			for j in range(len(mentions)):
				mention=mentions.fullText[j]
				respondedAT=mentions.fullText[j]
				for word in authorName:
					if word in mention.replace(","," ").replace("."," ").replace(u"\u2019","\'").split(" "):
						OwnerMentioned = iso_to_epoch(subset[subset['facebookAuthorId']==owner].reset_index(drop=True).date[0])
			Lapse_time = OwnerMentioned - mentionTime
			seconds = int(math.floor((Lapse_time%3600)%60))
			minutes = int(math.floor((Lapse_time%3600)/60))
			hours = int(math.floor((Lapse_time/3600)/60))
			Response_time = str(hours) + ":" + str(minutes) + ":" + str(seconds) 
			if Response_time == "0:0:0":
				newDF.loc[i,"ResponseTime"] = np.nan
				newDF.loc[i,"Responded"] = False
			else:
				newDF.loc[i,"ResponseTime"] = Response_time
				newDF.loc[i,"Responded"] = True
	return newDF

studyDF2 = add_response_time(negative_posts)
mentioned_by_name = studyDF2[studyDF2['Responded']]
specific_convo = subset[subset['author'].values=='<specific_name_to_study>']

studyDF2 = studyDF2[['author', 'facebookAuthorId','threadId','threadCreated','date','avatarUrl','url','engagement',
	'facebookComments', 'facebookLikes', 'facebookRole',
	'facebookShares', 'facebookSubtype', 'forumPosts', 'forumViews','id','impact',
	'resourceId','sentiment','snippet','fullText','ResponseTime','Responded']]

mentioned_by_name = mentioned_by_name[['author', 'facebookAuthorId','threadId','threadCreated','date','avatarUrl','url','engagement',
	'facebookComments', 'facebookLikes', 'facebookRole',
	'facebookShares', 'facebookSubtype', 'forumPosts', 'forumViews','id','impact',
	'resourceId','sentiment','snippet','fullText','ResponseTime','Responded']]

#Output to excel
data = data.astype(object)
studyDF2 = studyDF2.astype(object)
mentioned_by_name = mentioned_by_name.astype(object)
studyDF = studyDF.astype(object)
Rachels_convo = Rachels_convo.astype(object)


writer = pd.ExcelWriter(myWorkDirectory + '\\' + 'My_report.xlsx')
data.to_excel(writer,'data',index =False,encoding='utf-8', na_rep='NA')
studyDF2.to_excel(writer,'Negative_mentions',index =False,encoding='utf-8', na_rep='NA')
mentioned_by_name.to_excel(writer,'Owner_responses',index =False,encoding='utf-8', na_rep='NA')
studyDF.to_excel(writer,'conversation_overview',encoding='utf-8', na_rep='NA')
Rachels_convo.to_excel(writer,'Example_Rachel',index =False,encoding='utf-8', na_rep='NA')
writer.save()

