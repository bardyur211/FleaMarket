import sqlite3

con = sqlite3.connect('blacklist.db')
cur = con.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS Words(
            Word TEXT
)""")

con.commit()