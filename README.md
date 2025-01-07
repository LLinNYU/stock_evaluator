# Stock Evaluation Project
This is my personal project of stock analysis via Google RSS feeds.

The goal is to understand and navigate the stock market with a relatively small amount of resources by using google news RSS feeds once a day and incorporating a basic understanding of changes in stock. 

# Breakdown
## Part 1: Title Readers
1) Data Storage: `Daily RSS Feeds`
    - Run title_reader.py on the relevant RSS feeds
        - SPACE OUT THE URL REQUESTS (so you don't get kicked by Google)
        - topics: "stock market", "world", "business", "technology", "entertainment", "sports", "science", "health"
        - News from current day only
    - Storage via SQLite because for querying abilities 
2) Interpret the news for today
    - Evaluate whether this is relevant to stocks - if so, suggest relevant topics
    - Requires LLMs/NLP
3) Stock history/metrics
    - Fetch stock history from Yahoo

# Dependencies:
(Assuming sqlite3 and requests are installed)
- feedparser: `pip install feedparser`
- lmxl: `pip install lmxl`

