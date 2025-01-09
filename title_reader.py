import feedparser
import sys
import os 
import sqlite3
import requests
from datetime import datetime,timezone

from bs4 import BeautifulSoup

# NEED TO:
# Ensure that at least one entry has been run first

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

# rss_feeds_mini = {
#     'business': 'https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx6TVdZU0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US%3Aen'}

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

# test: get first entry from the db to see if pub_date exists
# cursor.execute("""SELECT id,topic,title,pub_date,source FROM article_titles WHERE id = 1""")
# print(cursor.fetchone())

# What happened here???
# cursor.execute("""PRAGMA table_info(article_titles)""")
# print(cursor.fetchone())
# Conclusion: the table indeed exists 



# first check if there are entries:
# if no entries:
    # go straight to adding entries and COMMIT()
# if yes entries:
    # check if it has today
    # if has today: print 'hey you did this already'
    # else: go straight adding entries 
def read_items(items):
    for item in items: 
        # only care about today's news for consistency - everything in GMT time
        pub_date = item.find('pubDate').text
        original_date = datetime.strptime(pub_date, "%a, %d %b %Y %H:%M:%S %Z")
        title = item.find('title').text
        print('Record this entry!: ', title)
        source_name = item.find('source').text
        sql_date = original_date.strftime("%Y-%m-%d %H:%M:%S")

        # execute sanitized user inputs
        cursor.execute("""INSERT INTO article_titles (topic,title,pub_date,source)
                    values (?,?,?,?)""",(topic,title,sql_date,source_name))

for topic, topic_url in rss_feeds.items():
    response = requests.get(topic_url)
    if response.status_code == 200:
        # parse content soup
        soup = BeautifulSoup(response.content, 'xml')

        # item extraction
        items = soup.find_all('item')
        gmt_now = datetime.now(timezone.utc).strftime("%Y-%m-%d")

        #count the amount of entries
        cursor.execute("""SELECT COUNT(*) FROM article_titles""")

        # if no entries added previously, thus 0 rows
        if cursor.fetchone()[0] == 0:
            print('no entries previously, let\'s read')
            read_items(items)
        else:
            # table has already been written in before
            # print('previous entries exist')

            # Query: Did a specific topic for today get logged? 
            cursor.execute("""SELECT COALESCE(DATE(MAX(pub_date)) = DATE('now','utc'),0) FROM article_titles
                           WHERE topic = ?""",(topic,))
            already_parsed_today = False if cursor.fetchone()[0] == 0 else True
            
            cursor.execute("""SELECT DATE('now','utc')""")
            print('today\'s date in UTC:',cursor.fetchone()[0], )

            #if it hasn't been parsed today, add all the entries in
            if not already_parsed_today:
                print('hasn\'t been parsed today')
                read_items(items)
            else:
                print('You\'ve already saved the article titles today!')

    else: 
        print('Error :/ Status code:', response.status_code)
conn.commit()
conn.close()

        