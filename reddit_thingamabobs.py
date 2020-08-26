import praw
from yaml import safe_load
from file_handler import getFile

reddit = None
subreddit = "starcraft2coop"

def getRedditInstance():
	global reddit

	if(reddit):
		return reddit

	with getFile("credentials.yml") as file:
		credentials = safe_load(file)["reddit"]

	reddit = praw.Reddit(**credentials)
	reddit.validate_on_submit = True

	return reddit

def getSubredditInstance():
	return getRedditInstance().subreddit(subreddit)

def getRedditLink(postID):
	return getRedditInstance().submission(id = postID)