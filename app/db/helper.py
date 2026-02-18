import sqlite3

def get_connection():
    conn = sqlite3.connect('bot.db') 
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            telegram_id INTEGER PRIMARY KEY
        )
    ''')
    conn.commit()
    conn.close()

def save_user(telegram_id, token):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO users (telegram_id)
        VALUES (?)
    ''', (telegram_id, token))
    conn.commit()
    conn.close()