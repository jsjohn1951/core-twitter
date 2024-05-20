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
USERNAME = os.getenv('TWITTER_USERNAME');
PASSWORD = os.getenv('TWITTER_PASSWORD');
FILENAME = os.getenv('TWITTER_CSV_FILENAME');
FOLLOWER_COUNT = int(os.getenv('FOLLOWER_COUNT'));
TREND_STR = os.getenv('TRENDS');
MAX_COUNT = int(os.getenv('MAX'));

# Global Variables
app = Twitter("session");
app.sign_in(username=USERNAME, password=PASSWORD);
trends = [];
data = [];
fields = [
			'trend',
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
 
def exists_on_db(info):
	for entry in data:
		if info['username'] == entry['username']:
			return True;
	return False;

# extracts the data from userinfo 
def extract(trend, userinfo):
    i = 1;
    if userinfo.followers_count >= FOLLOWER_COUNT:
        info = {
			'trend' : trend,
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
        if not exists_on_db(info) :
            print('\x1B[35mUser\x1B[0m:\t', userinfo.username, '✅');
            if len(data) < MAX_COUNT:
                data.append(info);
            else:
                print('\x1B[36mOverwriting\x1B[0m:\t', data[i]['username'], '\t\x1B[33m⸜(｡˃ ᵕ ˂ )⸝♡\x1B[0m');
                data[i] = info;
                if i >= MAX_COUNT:
                    i = 1;
                i = i + 1;
        else :
            print('User \'', userinfo.username, '\' \x1B[31malready logged!\x1B[0m ❌');
    else :
        print('User \'', userinfo.username, '\' \x1B[31mUser has less than',FOLLOWER_COUNT,'followers!\x1B[0m ❌');
			

def iter():
	i = 0;
	for trend in trends :
		print('\n\x1B[34mOn Trend:\t', trend, '\x1B[0m')
		tweets = app.search(trend, pages=3, filter_=SearchFilters.Latest(), wait_time=5);
		for tweet in tweets :
			userinfo: tweety.types.twDataTypes.User = tweet.author;
			extract(trend=trend, userinfo=userinfo);

def main():
    flag = False;
    loadTrends();
    try :
        Path("./csv").mkdir(parents=True, exist_ok=True);
        try :
            print('\n\x1B[35mImporting Previous\x1B[0m:\n');
            with open("./csv/" + FILENAME, 'r') as csvfile:
                reader = csv.DictReader(csvfile, fieldnames=fields);
                for row in reader:
                    info = {
						'trend' : row['trend'],
						'id' : row['id'],
						'name' : row['name'],
						'username' : row['username'],
						'profile_img' : row['profile_img'],
						'verified' : row['verified'],
						'description' : row['description'],
						'location' : row['location'],
						'entities' : row['entities'],
						'public_metrics' : row['public_metrics'],
						'protected' : row['protected'],
						};
                    data.append(info);
                csvfile.close();
                for item in data[1:]:
                    print('importing:\x1B[35m', item['username'], '\x1B[0m');
        except OSError as error:
            print('Exception occured: ', error);
            if error.errno == 2:
                flag = True;
                print('We Will Create the File!');
            else :
                raise error;

        try :
            print('\n\x1B[35mStarting Lookup\x1B[0m:');
            iter();
        except Exception as error:
            print('Exception occured: ', error);
        
        with open("./csv/" + FILENAME, 'w+') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fields);
            if flag :
                writer.writeheader();
            for item in data:
                writer.writerow(item);
            csvfile.close();
    except Exception as error:
        print('Exception occured: ', error);
    print('Ended\n');

if __name__=="__main__": 
    main() 
