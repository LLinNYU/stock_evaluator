import feedparser
import sys

from bs4 import BeautifulSoup

# The Google RSS feed URL
feed_url = sys.argv[1]

feed = feedparser.parse(feed_url)

