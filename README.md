# Tweety-Concept

Hi! In this project I've created a program to retrieve certain user information from **Twitter / X** by using a dummy account and a python library '**tweety**.'

The program will target specific trends and note the top *tweets* before extracting usernames and searching for the user profile.

The Following information is extracted from user information and added to a csv file.
``` python
{
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
} 
``` 

# Use:
Make sure to install the following dependencies

## Install Dependencies
``` bash
sudo apt-get update && upgrade
sudo apt-get install python3 python3-pip ipython3
python3 -m pip install --upgrade pip
python3 -m pip install --upgrade tweety-ns
pip3 install dotenv
```
##
Use the following .env example and place your .env within the root directory of the program.

## .env requirements:

>USERNAME='user'

>PASSWORD='pass'

>CSV_FILENAME='tweety_scraper.csv'

>TRENDS='Fashion and Beauty, Fitness and Wellness, Travel, Celebrity News and Gossip, Social Causes and Activism, Entertainment, Technology and Gaming'

Copy the above into your .env, replace *user* and *pass* with your Dummy Twitter account's *Username* and *Password*. You can edit the trends you would like to search for with the **TRENDS** variable. Make sure to separate trends with a ',' as shown in the example above.

# Tweety Documentation

>https://mahrtayyab.github.io/tweety_docs/basic/installation.html