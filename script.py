from tweety import Twitter
import os
from dotenv import load_dotenv
import csv
from time import sleep

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
fields = [
			'Found on Trend',
			'id',
			'name',
			'username',
			'profile_img',
			'created_at',
			'verified',
			'description',
			'location',
			'entities',
			'public_metrics',
			'protected',
		];

def sleep_minutes(minutes):
    sleep(minutes * 60);

def loadTrends():
	i = 0;
	print('\n\x1B[34mLoading Trends\x1B[0m:\n');
	trends_list = TREND_STR.split(',');
	for trend in trends_list:
		trends.append(trend.strip());
		print(i, ') \x1B[31m', trend.strip(), '\x1B[0m');
		i = i + 1;
	print('\n\x1B[35mStarting Lookup\x1B[0m:\n');

def extract(writer):
	i = 0;
	for trend in trends :
		tweets = app.search(trend);
		for tweet in tweets :
			username = '';
			username = tweet.author.username;
			userinfo = app.get_user_info(username=username);
			if userinfo.verified and userinfo.followers_count >= 5000:
				print('\x1B[35mTrend\x1B[0m: ', trend, ' \x1B[35mUser\x1B[0m: ', userinfo.username, '\n');
				writer.writerow({
					'Found on Trend' : trend,
					'id' : userinfo.id,
					'name' : userinfo.name,
					'username' : userinfo.username,
					'profile_img' : userinfo.profile_image_url_https,
					'created_at' : userinfo.created_at,
					'verified' : userinfo.verified,
					'description' : userinfo.description,
					'location' : userinfo.location,
					'entities' : userinfo.entities,
					'public_metrics' : 
					{
						'tweet_count' : userinfo.media_count,
						'listed_count' : userinfo.listed_count,
						'followers_count' : userinfo.followers_count
					},
					'protected' : userinfo.protected,
					});
		if i > 2 :
			sleep_minutes(15);
			i = 0;
		i = i + 1;

def main():
	loadTrends();
	try :
		with open(FILENAME, 'w') as csvfile:
			writer = csv.DictWriter(csvfile, fieldnames=fields);
			writer.writeheader();
			extract(writer=writer);
	except Exception as error:
		print('Exception occured: ', error);
	print('Ended\n');

if __name__=="__main__": 
    main() 
