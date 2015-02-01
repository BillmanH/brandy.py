# brandy.py

brandy.py: A Python Library for Brandwatch
Brandwatch has a very powerful API that can get you a lot more data than you can usually scrape from social media’s open APIs such as Facebook and Twitter. The API and Brandwatch’s dashboard tool really work well together to allow my team to collect and synthesize huge volumes of data. Because I use the API a lot, I made a series of time saving functions to get me where I am going more quickly. These libraries should give you a good head start on your Brandwatch data projects. 
In Python, I use Pandas and Numpy every day. These two together replace almost everything that I enjoy about R’s vector system. 
brandy.py has the following dependencies:
import requests
import json
import pandas as pd
import numpy as np
import time

Loading the Libraries:
Although you can copy and paste them into you interpreter, I made the codes so that you can import them directly into your libraries for easy use. Because Python doesn’t compile, you can just save the brandy.py file into your Python library and it will import. For the examples here I have loaded them into ipython using:
from brandy import *
Logging In:
The first time logging in you will need to log in the same way you would with the dashboard in your browser.  This function has been written out to return the access_token that you will need for all of your queries. The code below will call Brandwatch to get the key and then store it in a local file for later use. 
file_path = r” C:\Users\Python \files\for\Brandwatch”
access_token = get_new_key('email@email.com', 'password')
store_key(access_token)

After you have the key you can fetch it using a simple logon command:

file_path = r” C:\Users\Python \files\for\Brandwatch”
project_list, access_token = boot_brandy(file_path)

From there the world is your oyster.  I put a lot of docstrings into each function so you can get a full description of each function by entering help(function). To get a full list of functions just type: help(brandwatch).

Using dates:
Because Brandwatch only uses ISO dates, I added some functions that move smoothly between epoch time and ISO. These allow other functionality such as measuring latency between posts, or integration with other timing functions in your application. For example, if you have a dataframe using ISO dates you can quickly add an epoch column by using:

df = add_epoch_date(df, 'column')

You can also change a string ISO time into a float epoch and vice versa using:

epochTime = iso_to_epoch(isoTime)
isoTime = epoch_to_iso(epochTime)

This is most useful when calculating dates for http requests. The ‘startDate’ and ‘endDate’ are a major part of the query. While this can help with adding and subtracting time, be careful of errors caused by rounding epoch time. Check your work.

Getting queries, channels, rules and tags: 

Because most of my processing is in pandas.DataFrame objects, I set the output of these function to also return DataFrames. They are pretty self-explanatory. 

query_list = get_query_id(project_id,access_token)
query_id = get_query_id_from_name(query_list,'TMobileB2B')
query_groups = get_query_group_ids(project_id,access_token)
subqueries = get_query_children(query_groups, query_id)

You will see that ‘queries’ in query_groups is a dict of queries by id. You can pull out the individual queries using get_query_children(query_groups, query_id) in order to pull out a specific query. Note that, in the context of the API, Brandwatch considers a ‘channel’ and a ‘query’ as pretty much the same thing. 

