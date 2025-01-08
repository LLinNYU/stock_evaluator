import feedparser
import sys
import os 
import sqlite3
import requests
from datetime import datetime,timezone

from bs4 import BeautifulSoup

# PLEASE ADD##############
# NEED TO:
# (1) CLOSE CONN
# (2) NEED TO IGNORE IF THE DATE IS ALREADY FOUND IN THE DATABASE!!!!

# dictionary of RSS feeds to read each day
rss_feeds = {
    'business': 'https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx6TVdZU0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US%3Aen',
    'technology': 'https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGRqTVhZU0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US%3Aen',
    'world': 'https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx1YlY4U0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US%3Aen',
    'finance': 'https://news.google.com/rss/topics/CAAqIQgKIhtDQkFTRGdvSUwyMHZNREpmTjNRU0FtVnVLQUFQAQ?hl=en-US&gl=US&ceid=US%3Aen',
    'science': 'https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFp0Y1RjU0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US%3Aen',
    'health': 'https://news.google.com/rss/topics/CAAqIQgKIhtDQkFTRGdvSUwyMHZNR3QwTlRFU0FtVnVLQUFQAQ?hl=en-US&gl=US&ceid=US%3Aen',
    'sports': 'https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFp1ZEdvU0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US%3Aen',
    'entertainment': 'https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNREpxYW5RU0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US%3Aen'
    }

# db file path
db_path = '/workspaces/stock_evaluator/article_titles/titles.db'

# initialize database before first retrieval
# session to connect to sqlite database
conn = sqlite3.connect(db_path)
# sql execution object
cursor = conn.cursor()

rss_feeds_mini = {
    'business': 'https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx6TVdZU0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US%3Aen'}

# DB ALREADY EXISTS, SAVE SOME COMPUTE RESOURCES by commenting the below
# need id, topic, title, publication date, source
# cursor.execute("""CREATE TABLE IF NOT EXISTS 
# article_titles (
#                id INTEGER PRIMARY KEY AUTOINCREMENT,
#                topic TEXT NOT NULL,
#                title TEXT NOT NULL,
#                pub_date DATETIME NOT NULL,
#                source TEXT NOT NULL
#                )""")

for topic, topic_url in rss_feeds_mini.items():
    response = requests.get(topic_url)
    if response.status_code == 200:
        # parse content soup
        soup = BeautifulSoup(response.content, 'xml')

        # item extraction
        items = soup.find_all('item')
        gmt_now = datetime.now(timezone.utc).strftime("%Y-%m-%d")

        # did I already run this script today and grab all the articles?
        # if so, then don't add more
        cursor.execute("""SELECT MAX(pub_date) latest_update FROM article_titles
                       WHERE DATE(latest_update) = DATE('now','utc')""")
        already_parsed_today = cursor.fetchone()


        if not already_parsed_today[0]:
            for item in items: 
                # only care about today's news for consistency - everything in GMT time
                pub_date = item.find('pubDate').text
                original_date = datetime.strptime(pub_date, "%a, %d %b %Y %H:%M:%S %Z")

                if (gmt_now == original_date.strftime("%Y-%m-%d")):
                    title = item.find('title').text
                    print('Record this entry!: ', title)
                    source_name = item.find('source').text
                    sql_date = original_date.strftime("%Y-%m-%d %H:%M:%S")

                # execute sanitized user inputs
                cursor.execute("""INSERT INTO article_titles (topic,title,pub_date,source)
                            values (?,?,?,?)""",(topic,title,sql_date,source_name))
        else:
            print('You\'ve already saved the article titles today')   
        # good practice
        conn.close()
    else: 
        print('Error :/ Status code:', response.status_code)

    