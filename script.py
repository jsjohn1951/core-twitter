from tweety import Twitter
import os
from dotenv import load_dotenv

load_dotenv();
USERNAME = os.getenv('USERNAME');
PASSWORD = os.getenv('PASSWORD');
  
app = Twitter("session")
app.sign_in(username=USERNAME, password=PASSWORD)

trends = app.get_trends()

i = 0

print('Starting\n')

try :
	for trend in trends :
		tweets = app.search(trend.name)
		print(tweets)
		if ( i > 5 ):
			break ;
		i = i + 1;
except Exception as error:
	print('Exception occured: ', error)
# for tweet in tweets:
#     username = ''
#     username = tweet.author.username
#     userInfo = app.get_user_info(username=username)
    # app.get_user
    # userInfo.followers_count
    # userInfo.description
    # userInfo.location
    # print(username, ' ---- ')
    # print( userInfo.profile_image_url_https)
    # userInfo._raw
    # print(userInfo._raw)
    # userInfo.profile_url
    # userInfo.profile_image_url_https
    # userInfo.fast_followers_count
    # print('checking: ', username, '\n\n')
    # followers = app.get_user_followers(username=username)
    # print('followers: ', followers);
    # time.sleep(3)
    # scraper = Nitter(log_level=1, skip_instance_check=False)
    # profile = scraper.get_profile_info(username)
    # print(profile)
    # print('type: ', type(username))
    
# scraper = Nitter(log_level=1, skip_instance_check=False)
# profile = scraper.get_profile_info('WildernessWypt')
# print(profile)

