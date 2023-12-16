import sqlite3

from app.infrastructure.password import encrypt_password

def authenticate_user(email: str, password: str):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute("SELECT password FROM users WHERE email=?", (email,))
    result = cursor.fetchone()

    if result is not None:
        stored_password = result[0]
        if encrypt_password(password) == stored_password:
            return True

    return False

def create_users_table():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS users (email TEXT, password TEXT)")
    conn.commit()