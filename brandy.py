#Brandwatch Functions
#William Harding 1/21/2015
#billh@tahzoo.com
#http://tahzoo.com/

import requests
import json
import pandas as pd
import numpy as np
import time



def get_new_key(login_name, login_password):
	"""
	Brandwatch account required
	
	login_name {string: the email or username that you use to login to the dashboard}
	login_password {string: the password that you use with the dashboard}
	returns: access_token {string}
	
	access_token = get_new_key('email@email.com', 'password')
	
	"""
	login_request_URL = r"https://newapi.brandwatch.com/oauth/token"
	request_string = login_request_URL + "?username=" + login_name + "&password=" + login_password + r"&grant_type=api-password&client_id=brandwatch-api-client"
	response = requests.post(request_string)
	print (response.status_code)
	if response.status_code == 200:
		print ("Acquire key: success")
	else:
		print "Something went wrong"
		print response.status_code
		print response.text
	response_codes = json.loads(response.text)
	access_token = response_codes['access_token']
	return access_token
	
def store_key(access_token,file_path):
	"""
	store_key(access_token)
	
	no return value, requires 
	"""
	key_file = open(file_path + "\key.txt", "w")
	key_file.write(access_token)
	key_file.close()
	print access_token + " has been written to file"

def get_key_from_file(file_path):
	key_file = open(file_path + r"\key.txt", "r")
	access_token = key_file.read().replace('\n', '')
	return access_token

def list_projects(access_token):
	request_URL = "https://newapi.brandwatch.com/projects?access_token=" + str(access_token)
	response = requests.get(request_URL)
	if response.status_code == 200:
		print ("Request: success")
	project_json = json.loads(response.text)
	project_list = pd.DataFrame(project_json['results'])
	print project_list[['name','id']]
	return project_list
	
def get_project_id_from_name(project_list,project_name):
	print project_list[project_list['name']==project_name][['name','id']]
	name = project_list[project_list['name']==project_name][['id']].reset_index(drop=True)
	id = str(name['id'][0])
	return id
	
def get_query_id_from_name(query_list,query_name):
	print query_list[query_list['name']==query_name][['name','id']]
	name = query_list[query_list['name']==query_name][['id']].reset_index(drop=True)
	id = str(name['id'][0])
	return id

def get_query_id(project_id,access_token):
	request_URL = "https://newapi.brandwatch.com/projects/" + str(project_id) + "/queries/summary?access_token=" + access_token
	response = requests.get(request_URL)
	if response.status_code == 200:
		print ("Get query ID: success")
	project_json = json.loads(response.text)
	project_summary = pd.DataFrame(project_json['results'])
	print project_summary[['name','type','id']]
	return project_summary	

	
def get_rules(project_id,access_token):
	'''
	rules = get_rules(project_id,access_token)
	https://newapi.brandwatch.com/projects/{project_id}/rules?access_token={access_token}
	'''
	request_URL = r"https://newapi.brandwatch.com/projects/" + project_id + r"/" + r"rules?access_token=" + access_token
	response = requests.get(request_URL)
	print (response.status_code)
	if response.status_code == 200:
		print ("Acquire key: success")
	else:
		print "Something went wrong"
		print response.status_code
		print response.text
	content = json.loads(response.text)
	df = pd.DataFrame(content['results'])
	print df[['name','id']]
	return df
	#access_token = response_codes['access_token']
	
def get_categories(project_id,access_token):
	'''
	categories = get_categories(project_id,access_token)
	categories[categories['name']=='name'].values  #will give you a list of categories for that group. 

	https://newapi.brandwatch.com/projects/{project_id}/categories?access_token={access_token}
	'''
	request_URL = r"https://newapi.brandwatch.com/projects/" + project_id + r"/" + r"categories?access_token=" + access_token
	response = requests.get(request_URL)
	print (response.status_code)
	if response.status_code == 200:
		print ("Acquire key: success")
	else:
		print "Something went wrong"
		print response.status_code
		print response.text
	content = json.loads(response.text)
	df = pd.DataFrame(content.get('results'))
	print df[['name','id']]
	return df
	#access_token = response_codes['access_token']

def cat_tags(df,cat_name):
	'''
	tags = cat_tags(categories,cat_name)
	'''
	df1 = pd.DataFrame(df[df['name']==cat_name].children.reset_index(drop=True)[0])
	return df1


def get_query_group_ids(project_id,access_token):
	'''
	query_groups = get_query_group_id(project_id,access_token)
	'''
	request_URL = "https://newapi.brandwatch.com/projects/" + str(project_id) + "/querygroups?access_token=" + access_token
	response = requests.get(request_URL)
	if response.status_code == 200:
		print ("Get query ID: success")
	project_json = json.loads(response.text)
	project_summary = pd.DataFrame(project_json['results'])
	print project_summary
	return project_summary	

def get_query_children(query_groups, query_number):
	'''
	subqueries = get_query_children(query_groups, query_id)
	'''
	query_groups[query_groups['id']==query_number]
	df = pd.DataFrame(query_groups[query_groups['id']==query_number].reset_index(drop=True)['queries'].values[0])
	print df
	return df
	
def get_mentions_query_URL(start_date,end_date,project_id,query_id,access_token,fullText):
	'''
	start_date {string: "2013-10-30"}
	end_date {string: "2015-10-30"}
	project_id {int: number of your project}
	query_id {int: number of your query}
	access_token {string}
	
	fullText {boolian: true will retrun the full text of the mention in a much larger json file
	
	request_URL = get_mentions_query_URL(start_date,end_date,project_id,query_id,access_token,fullText)
	
	returns {string: http}
	'''
	query_def = "data/mentions" 
	end_date = "endDate=" + end_date + "T00:00:00.000Z"
	start_date = "startDate=" + start_date + "T00:00:00.000Z"
	request_URL = "https://newapi.brandwatch.com/projects/" + str(project_id) + "/" + query_def
	if fullText == True:
		request_URL = request_URL + "/fulltext"
	request_URL = request_URL + "?" + "queryId=" + str(query_id) + "&" + start_date + "&" + end_date + "&pageSize=5000" + "&access_token=" + access_token
	return request_URL

def get_volume_data(start_date,end_date,query_type1,query_type2,project_id,query_id,access_token):
	'''
	start_date {string: "2013-10-30"}
	end_date {string: "2015-10-30"}
	project_id {int: number of your project}
	query_id {int: number of your query}
	access_token {string}
	
	myJson = get_volume_data(start_date,end_date,demension_1,demension_2,project_id,query_id,access_token)
	
	returns {string: http}
	'''
	query_def = "data/volume/" + query_type1 + "/" + query_type2 + "/"
	end_date = "?endDate=" + end_date
	start_date = "&startDate=" + start_date
	query_input = "&queryId=" + str(query_id)
	request_URL = "https://newapi.brandwatch.com/projects/" + project_id + "/" + query_def + end_date + query_input + start_date + "&access_token=" + access_token
	print request_URL
	response = requests.get(request_URL)
	print (response.status_code)
	if response.status_code == 200:
		print ("Acquire key: success")
	else:
		print response.text
		print request_URL
	project_json = json.loads(response.text)
	#query_volume = project_json['results']
	#data_time_volume = pd.DataFrame(query_volume[0]['values'])
	return project_json

		
def channel_query(query_def,start_date,end_date,project_id,query_id,access_token):
	'''
	project_json = channel_query(query_def,start_date,end_date,project_id,query_id,access_token)
	'''
	end_date = "?endDate=" + end_date
	start_date = "&startDate=" + start_date
	query_input = "&queryId=" + str(query_id)
	request_URL = "https://newapi.brandwatch.com/projects/" + project_id + "/" + query_def + end_date + query_input + start_date + "&access_token=" + access_token
	print request_URL
	response = requests.get(request_URL)
	print (response.status_code)
	if response.status_code == 200:
		print ("Acquire key: success")
	else:
		print response.text
	project_json = json.loads(response.text)
	return project_json
	
def get_mentions_data(request_URL):	
	"""
	myJson = get_mentions_data(request_URL)
	
	returns JSON
	"""
	response = requests.get(request_URL)
	print (response.status_code)
	if response.status_code != 200:
		print ("Query: failure")
		print request_URL
		print response.text
	project_json = json.loads(response.text)
	return project_json
	

def iso_to_epoch(isoTime):
	"""
	pattern = "%Y-%m-%dT%H:%M:%S"
	epochTime = time.mktime(time.strptime(isoTime, '%Y-%m-%dT%H:%M:%SZ'))
	
	epochTime = iso_to_epoch(isoTime)
	"""
	epochTime = time.mktime(time.strptime(isoTime, '%Y-%m-%dT%H:%M:%SZ'))
	return epochTime
	
def epoch_to_iso(epochTime):
	"""
	isoTime = epoch_to_iso(epochTime)
	isoTime = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(epochTime))
	"""
	isoTime = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(epochTime))
	return isoTime
	
def add_epoch_date(data, column):
	"""
	data {the pandas dataframe that contains an ISO datestamp}
	column {string: the column name that contains your ISO datestamp}
	returns: {pandas dataframe with appended epoch timestamp}
	
	data = add_epoch_date(data, 'column')
	"""
	for row in range(len(data)):
		data.loc[row, 'epoch'] = iso_to_epoch(data.loc[row, column])
	data = data.sort('epoch').reset_index()
	return data
	
def boot_brandy(file_path):
	"""
	call: project_list, access_token = boot_api()
	
	returns:
	project_list {pandas file contain}
	"""
	access_token=get_key_from_file(file_path)
	project_list = list_projects(access_token)
	return project_list, access_token

def brandwatch():
	"""
	brandwatch()
	project_list, access_token = boot_brandy(file_path)
	get_new_key(login_name, login_password)
	store_key(access_token)
	
	project_list = list_projects(access_token)
	project_id = get_project_id_from_name(project_list,project_name)
	
	df = add_epoch_date(df, 'column')
	epochTime = iso_to_epoch(isoTime)
	isoTime = epoch_to_iso(epochTime)
		 
	query_list = get_query_id(project_id,access_token)
	query_id = get_query_id_from_name(query_list,'name')
	query_groups = get_query_group_ids(project_id,access_token)
	subqueries = get_query_children(query_groups, query_id)
	query_ids = query_list['id'].values
	
	rules = get_rules(project_id,access_token)
	categories = get_categories(project_id,access_token)
	tags = cat_tags(categories,cat_name)

	request_URL = get_mentions_query_URL(start_date,end_date,project_id,query_id,access_token,fullText)
	project_json = get_volume_data(start_date,end_date,query_type1,query_type2,project_id,query_id,access_token)
	project_json = channel_query(query_def,start_date,end_date,project_id,query_id,access_token)
	myJson = get_mentions_data(request_URL) 
	"""
	print "project_id = get_project_id_from_name(project_list,'project_name')"
	print "query_list = get_query_id(project_id,access_token)"
	print "subqueries = get_query_children(query_groups, query_number)"

	print "today_date = time.strftime('%Y-%m-%dT%H:%M:%S')"
	print ""
	print "query_groups = get_query_group_id(project_id,access_token)"
	print "project_list, access_token = boot_api()"
	
	
