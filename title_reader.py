# import feedparser
import sys
import os 
from bs4 import BeautifulSoup
from datetime import date

# Check if today's date exists in titles_data - create it if it doesn't 
today = date.today()
today_day = today.day
today_month = today.month
today_year = today.year

today_directory = str(today_day) + "_" + str(today_month) + "_" + str(today_year)
current_directory = os.getcwd()
target_path = os.path.join(current_directory,today_directory)

if not os.path.exists(target_path):
    os.makedirs(target_path)
else:
    print(f"'{target_path}' already exists!")

# print(today_day,today_month,today_year)




# current_directory = os.path.dirname(__file__)
# print(current_directory)

# The Google RSS feed URLs
# feed_url = sys.argv[1]
# feed = feedparser.parse(feed_url)

