# Stock Evaluation Project
This is my personal project of stock analysis via Google RSS feeds.

The goal is to understand and navigate the stock market with a relatively small amount of resources by using google news RSS feeds once a day and incorporating a basic understanding of changes in stock. 

# Breakdown
## Part 1: Title Readers
1) Data Storage: `Daily RSS Feeds`
    - Check if the folder for today's folder exists
        - If True:
            - Skip 
        - If False:
            - Create new folder named the current date 
            - Run title_reader.py on the relevant RSS feeds
                - SPACE OUT THE URL REQUESTS SO YOU DON'T GET KICKED BY GOOGLE
                - topics: "stock market", "world", "business", "technology", "entertainment", "sports", "science", "health"
                - News from current day only
            - Storage via SQLite because I'd like querying abilities 
2) Interpret the news for today
    - Evaluate whether this is relevant to stocks - if so, suggest relevant topics
    - Requires LLMs/NLP
3) Stock history/metrics
    - Fetch stock history from Yahoo