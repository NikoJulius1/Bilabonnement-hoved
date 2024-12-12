import sqlite3

# Opret forbindelse til database
conn = sqlite3.connect("user_database.db")
cursor = conn.cursor()

# make the tables 
cursor.execute('''
CREATE TABLE IF NOT EXISTS users(
               user_id INTEGER PRIMARY KEY AUTOINCREMENT,
               username VARCHAR(100),
               password VARCHAR(100))
               ''')