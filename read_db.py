import sqlite3

db_path = '/workspaces/stock_evaluator/article_titles/titles.db'

# initialize database before first retrieval
# session to connect to sqlite database
conn = sqlite3.connect(db_path)
# sql execution object
cursor = conn.cursor()