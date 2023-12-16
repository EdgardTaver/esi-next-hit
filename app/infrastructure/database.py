import sqlite3

from app.infrastructure.password import encrypt_password
from app.config import USERS_DATABASE_FILE

def authenticate_user(email: str, password: str):
    conn = sqlite3.connect(USERS_DATABASE_FILE)
    cursor = conn.cursor()

    cursor.execute("SELECT password FROM users WHERE email=?", (email,))
    result = cursor.fetchone()

    if result is not None:
        stored_password = result[0]
        if encrypt_password(password) == stored_password:
            return True

    return False

def start_users_database_connection() -> sqlite3.Connection:
    # TODO: integration test?
    conn = sqlite3.connect(USERS_DATABASE_FILE)
    return conn


def create_users_table(connection: sqlite3.Connection):
    cursor = connection.cursor()

    create_statement = """
    CREATE TABLE IF NOT EXISTS
    users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT,
        password TEXT
    )
    """

    cursor.execute(create_statement)
    connection.commit()
    # TODO: should it really commit here?
