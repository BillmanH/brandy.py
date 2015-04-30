#Getting things from brandwatch
#note: I ran this in Rstudio and had no problems, but when I ran it in regular R the rjson
#note: these are just some of the basic parts of brandy.py translated in R. I know there is a lot missing but it should be enough to get you started.
#feel free to fork these and make improvements and I will merge them into the master version.

#Built for Brandwach by William Harding and Tahzoo
#http://tahzoo.com/
#www.linkedin.com/in/hardingwilliam

#Feel free to use as-is and let me know if you have improvements/bug-fixes


library(httr)
library(rjson)

#POST request example:
get_new_key <- function(login_name, login_password){
	#access_token <- get_new_key("me@tahzoo.com","myPassword")
	htpargs <- paste("?username=",login_name,
		"&password=",login_password,
		"&grant_type=api-password&client_id=brandwatch-api-client",
		sep = '')
	r <- POST(paste("https://newapi.brandwatch.com",
		"/oauth/token",htpargs, sep = ''))
	print(r$status_code)
	if (r$status_code!=200){
		print ("Something went wrong")
		print (content(r))
	} 
	x <- content(r)$access_token
	return(x)
}

#GET request example:
list_projects <- function(access_token){
	#project_list <- list_projects(access_token)
	#
	#query table to get id:
	#project_id <- project_list$id[which(grepl("My Project Name", project_list$name))][[1]]
	#project_id <- project_list[project_list$name == "Money Mindstates",]$id[[1]]
	htpargs <- paste("access_token=",access_token, sep = '')
	request_URL <- paste("https://newapi.brandwatch.com",
		"/projects/", "?",
		htpargs, sep = '')
	x <- fromJSON(file=request_URL, method='C')$results
	x.df = data.frame(do.call(rbind,x))
	return(x.df)
}

get_query_list <- function(project_id,access_token){
	#query_list <- get_query_list(project_id,access_token)
	#
	#
	#query table to get id:
	#query_id <- query_list[query_list$name == "foo",]$id[[1]]
	htpargs <- paste("access_token=",access_token, sep = '')
	request_URL <- paste("https://newapi.brandwatch.com",
		"/projects/", project_id,
		"/queries/summary" ,
		"?", htpargs, sep = '')
	x <- fromJSON(file=request_URL, method='C')$results
	x.df = data.frame(do.call(rbind,x))
	return(x.df)
}

get_query_group_list <- function(project_id,access_token){
	#query_groups <- get_query_group_list(project_id,access_token)
	#
	#
	#query table to get id:
	#group_id <- query_groups[query_groups$name == "foo",]$id[[1]]
	htpargs <- paste("access_token=",access_token, sep = '')
	request_URL <- paste("https://newapi.brandwatch.com",
		"/projects/", project_id,
		"/querygroups",
		"?", htpargs, sep = '')
	x <- fromJSON(file=request_URL, method='C')$results
	x.df = data.frame(do.call(rbind,x))
	return(x.df)
}


get_rules <- function(project_id,access_token){
	#rules <- get_rules(project_id,access_token)
	#
	#
	#query table to get id:
	#rule_id <- rules[rules$name == "rule",]$id[[1]]
	htpargs <- paste("access_token=",access_token, sep = '')
	request_URL <- paste("https://newapi.brandwatch.com",
		"/projects/", project_id,
		"/rules",
		"?", htpargs, sep = '')
	x <- fromJSON(file=request_URL, method='C')$results
	x.df = data.frame(do.call(rbind,x))
	return(x.df)
}

get_categories <- function(project_id,access_token){
	#category_groups <- get_categories(project_id,access_token)
	#
	#
	#query table to get id:
	#category <- category_groups[category_groups$name == "category",]$id[[1]]
	htpargs <- paste("access_token=",access_token, sep = '')
	request_URL <- paste("https://newapi.brandwatch.com",
		"/projects/", project_id,
		"/categories",
		"?", htpargs, sep = '')
	x <- fromJSON(file=request_URL, method='C')$results
	x.df = data.frame(do.call(rbind,x))
	return(x.df)
}


access_token <- get_new_key("me@tahzoo.com","1234")
project_list <- list_projects(access_token)

project_id <- project_list[project_list$name == "Money Mindstates",]$id[[1]]

