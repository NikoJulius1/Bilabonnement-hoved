from flask import Flask, jsonify, request
import requests
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('user_database.db')
    conn.row_factory = sqlite3.Row
    return conn

# register a user
@app.route('/register', methods=['POST'])
def register():
    username = username.get('username')
    password = password.get('password')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO users ( username, password)
        VALUES (?, ?)''') (username, password)
    conn.commit()
    conn.close()



