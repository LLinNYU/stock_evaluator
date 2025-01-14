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

cursor.execute('''SELECT COUNT(*) FROM article_titles''')
print(cursor.fetchone()[0])

# cursor.execute('''DELETE FROM article_titles WHERE DATE(pub_date) = DATE('now','utc')''')

# cursor.execute('''SELECT COUNT(*) FROM article_titles''')
# print(cursor.fetchone()[0])

# cursor.execute("SELECT * from article_titles WHERE topic != 'business' ")
# print(cursor.fetchall())

# topic = 'health'
# topic = 'business'

# cursor.execute("""SELECT COALESCE(DATE(MAX(pub_date)) = DATE('now','utc'),0) FROM article_titles
#                            WHERE topic = ?""",(topic,))
# print(cursor.fetchone()[0])

# cursor.execute('SELECT * FROM article_titles ORDER BY id DESC LIMIT 5')
# print(cursor.fetchall())

# cursor.execute('''CREATE TABLE new_table (
#                id INTEGER PRIMARY KEY AUTOINCREMENT,
#                topic TEXT NOT NULL,
#                title TEXT NOT NULL,
#                pub_date DATETIME NOT NULL,
#                source TEXT NOT NULL)''')
# cursor.execute('''INSERT INTO new_table (topic,title,pub_date,source)
#                SELECT DISTINCT topic,title,pub_date,source FROM article_titles''')
# cursor.execute('''DROP TABLE article_titles''')
# cursor.execute('''ALTER TABLE new_table RENAME TO article_titles''')

# cursor.execute('''SELECT COUNT(*) FROM article_titles''')
# print(cursor.fetchone()[0])

conn.commit()
conn.close()

# print(last_updated_today)