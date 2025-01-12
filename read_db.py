import sqlite3
# This python file is for testing and running one-time commands


db_path = '/workspaces/stock_evaluator/article_titles/titles.db'

# initialize database before first retrieval
# session to connect to sqlite database
conn = sqlite3.connect(db_path)
# sql execution object
cursor = conn.cursor()

#if SQLite returns 0 then it is false, boolean types exist outside of SQLite
# Must remove timestamp when doing date comparisons
cursor.execute("""SELECT DATE(MAX(pub_date)) FROM article_titles""")
print(cursor.fetchone()[0])

# first entry from 01/07
# cursor.execute('SELECT * from article_titles WHERE id < 2')
# print(cursor.fetchall())

#delete all entries from today
# cursor.execute('''SELECT COUNT(*) FROM article_titles''')
# print(cursor.fetchone()[0])

cursor.execute('''DELETE FROM article_titles WHERE DATE(pub_date) = DATE('now','utc')''')

# cursor.execute('''SELECT COUNT(*) FROM article_titles''')
# print(cursor.fetchone()[0])

# cursor.execute("SELECT * from article_titles WHERE topic != 'business' ")
# print(cursor.fetchall())

# topic = 'health'
# topic = 'business'

# cursor.execute("""SELECT COALESCE(DATE(MAX(pub_date)) = DATE('now','utc'),0) FROM article_titles
#                            WHERE topic = ?""",(topic,))
# print(cursor.fetchone()[0])

conn.commit()
conn.close()

# print(last_updated_today)