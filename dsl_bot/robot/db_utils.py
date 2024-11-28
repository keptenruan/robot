# db_utils.py
import mysql.connector
from config import Config
from models import User, Account
from passlib.hash import pbkdf2_sha256

def get_db_connection():
    conn = mysql.connector.connect(
        host=Config.DATABASE_HOST,
        user=Config.DATABASE_USER,
        password=Config.DATABASE_PASSWORD,
        database=Config.DATABASE_NAME
    )
    return conn

def init_db():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) NOT NULL UNIQUE,
                password_hash VARCHAR(255) NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Accounts (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                account_number VARCHAR(50) NOT NULL,
                balance DECIMAL(10, 2) DEFAULT 0.00,
                FOREIGN KEY (user_id) REFERENCES Users(id)
            )
        ''')
        conn.commit()

def register(username, password):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            hashed_password = pbkdf2_sha256.hash(password)
            cursor.execute('INSERT INTO Users (username, password_hash) VALUES (%s, %s)', (username, hashed_password))
            conn.commit()
            print("User registered successfully.")
        except mysql.connector.IntegrityError:
            print("Username already exists.")

def login(username, password):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, password_hash FROM Users WHERE username = %s', (username,))
        user = cursor.fetchone()
        if user and pbkdf2_sha256.verify(password, user[1]):
            return User(user[0], username, user[1])
        else:
            print("Invalid credentials.")
            return None

def logout(user):
    # 这里可以添加注销逻辑，例如清除会话或令牌
    print(f"User {user.username} logged out successfully.")