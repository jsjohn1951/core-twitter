import tweety
import os
import csv
import tweety.types
from tweety import Twitter
from tweety.filters import SearchFilters
from time import sleep
from pathlib import Path
from dotenv import load_dotenv

# load the env file
load_dotenv();

# Retrive variables
USERNAME = os.getenv('USERNAME');
PASSWORD = os.getenv('PASSWORD');
TREND_STR = os.getenv('TRENDS');
FILENAME = os.getenv('CSV_FILENAME');

# Global Variables
app = Twitter("session");
app.sign_in(username=USERNAME, password=PASSWORD);
trends = [];
data = [];
fields = [
			'Found on Trend',
			'id',
			'name',
			'username',
			'profile_img',
			'verified',
			'description',
			'location',
			'entities',
			'public_metrics',
			'protected',
		];

# function to sleep for set number of minutes
def sleep_minutes(minutes):
    sleep(minutes * 60);

# loads the trends
def loadTrends():
	i = 0;
	print('\n\x1B[34mLoading Trends\x1B[0m:\n');
	trends_list = TREND_STR.split(',');
	for trend in trends_list:
		trends.append(trend.strip());
		print(i, ') \x1B[31m', trend.strip(), '\x1B[0m');
		i = i + 1;
	print('\n\x1B[35mStarting Lookup\x1B[0m:\n');

# extracts the data from userinfo 
def extract(writer, trend, userinfo):
	if userinfo.followers_count >= 5000:
		info = {
			'Found on Trend' : trend,
			'id' : userinfo.id,
			'name' : userinfo.name,
			'username' : userinfo.username,
			'profile_img' : userinfo.profile_image_url_https,
			'verified' : userinfo.verified,
			'description' : userinfo.description,
			'location' : userinfo.location,
			'entities' : userinfo.entities,
			'public_metrics' : 
			{
				'media_count' : userinfo.media_count,
				'status_count': userinfo.statuses_count,
				'listed_count' : userinfo.listed_count,
				'followers_count' : userinfo.followers_count,
			},
			'protected' : userinfo.protected,
			};
		if info not in data :
			print('\x1B[35mUser\x1B[0m:\t', userinfo.username, '✅');
			writer.writerow(info);
			data.append(info);
		else :
			print('User \'', userinfo.username, '\' \x1B[31malready logged!\x1B[0m ❌');
	elif not userinfo.followers_count >= 5000:
		print('User \'', userinfo.username, '\' \x1B[31mUser has less than 5000 followers!\x1B[0m ❌');
			

def iter(writer):
	i = 0;
	for trend in trends :
		print('\n\x1B[34mOn Trend:\t', trend, '\x1B[0m')
		tweets = app.search(trend, pages=3, filter_=SearchFilters.Latest(), wait_time=5);
		for tweet in tweets :
			username = '';
			username = tweet.author.username;
			userinfo: tweety.types.twDataTypes.User = tweet.author;
			extract(writer=writer, trend=trend, userinfo=userinfo);

def main():
	loadTrends();
	try :
		Path("./csv").mkdir(parents=True, exist_ok=True)
		with open("./csv/" + FILENAME, 'w') as csvfile:
			writer = csv.DictWriter(csvfile, fieldnames=fields);
			writer.writeheader();
			iter(writer=writer);
	except Exception as error:
		print('Exception occured: ', error);
	print('Ended\n');

if __name__=="__main__": 
    main() 
