from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from dotenv import load_dotenv # import fra .env fil
import os
import requests
import sqlite3

# Load environment variables fra .env filen
load_dotenv()

app = Flask(__name__)

# Gem secret key in env fil
app.config['JWT_SECRET_KEY'] = os.getenv('KEY')

# Sæt authorization header til 'token' istedet for 'bearer' for simpelhed
app.config['JWT_HEADER_TYPE'] = 'token'

# Gør så den ikke udløber
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False

jwt = JWTManager(app)

def get_db_connection():
    conn = sqlite3.connect('user_database.db')
    conn.row_factory = sqlite3.Row
    return conn

# register a user
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # Hvis de IKKE har udfyldt username og password, giv error besked
    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO users ( username, password)
        VALUES (?, ?)''', (username, password))
    conn.commit()
    conn.close()
    return jsonify({'message': 'User registered successfully'}), 201

# Log en bruger ind
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
        
    # Hvis de IKKE har udfyldt username og password, giv error besked
    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400
    
    #Tjek om det er en bruger der eksisterer, så man ikke bare kan indsætte alt og komme ind
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    user = cursor.fetchone()
    conn.close()
    if not user:
        return jsonify({'message': 'Invalid username or password'}), 401
    
# Opret token
    token = create_access_token(identity=username)

    return jsonify({
        'access_token': token,
    }), 200

if __name__ == '__main__':
    app.run()
