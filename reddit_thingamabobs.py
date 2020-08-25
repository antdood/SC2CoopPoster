import praw
from yaml import safe_load

reddit = None

def getRedditInstance():
	global reddit

	if(reddit):
		return reddit

	with open("credentials.yml") as file:
		credentials = safe_load(file)["reddit"]

	reddit = praw.Reddit(**credentials)
	reddit.validate_on_submit = True

	return reddit.subreddit("sircmpwn")