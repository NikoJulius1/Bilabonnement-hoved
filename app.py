from flask import Flask, jsonify, request, g
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from dotenv import load_dotenv # import fra .env fil
import os
import requests
import sqlite3


# Load environment variables fra .env filen
load_dotenv()
db_path=os.getenv("db_path", "user_database.db")

app = Flask(__name__)

# Gem secret key in env fil
app.config['JWT_SECRET_KEY'] = os.getenv('KEY')

# Sæt authorization header til 'token' istedet for 'bearer' for simpelhed
app.config['JWT_HEADER_TYPE'] = 'token'

# Gør så den ikke udløber
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False

jwt = JWTManager(app)

@app.route('/debug', methods=['GET'])
def debug():
    return jsonify({
        "JWT_SECRET_KEY": app.config['JWT_SECRET_KEY'],
        "Database_Path": db_path
    }), 200

def get_db_connection():
    if 'db' not in g:
        g.db = sqlite3.connect(db_path) 
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(error):
    if 'db' in g:
        g.db.close()

with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users(
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username VARCHAR(100),
        password VARCHAR(100))
    ''')
    conn.commit()

# Home så den viser den virker hvis man går på azure
@app.route('/')
def home():
    return "Welcome to the Login API. Use /register or /login for functionality."

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
    app.run(port=5002)
