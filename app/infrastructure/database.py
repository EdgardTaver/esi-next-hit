import sqlite3

from app.infrastructure.password import encrypt_password
from app.config import USERS_DATABASE_FILE
from app.exceptions import EmailAlreadyRegisteredException


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

def create_music_table(connection: sqlite3.Connection):
    cursor = connection.cursor()

    create_statement = """
    CREATE TABLE IF NOT EXISTS
    musics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        artist TEXT,
        genre TEXT
    )
    """

    cursor.execute(create_statement)
    connection.commit()


def create_playlists_table(connection: sqlite3.Connection):
    cursor = connection.cursor()

    create_statement = """
    CREATE TABLE IF NOT EXISTS
    playlists (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        user_id INTEGER,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    """

    cursor.execute(create_statement)
    connection.commit()


def register_user(connection: sqlite3.Connection, email: str, password: str):
    cursor = connection.cursor()

    select_statement = """
    SELECT email FROM users WHERE email=?
    """

    cursor.execute(select_statement, (email,))
    result = cursor.fetchone()

    if result is not None:
        raise EmailAlreadyRegisteredException()

    insert_statement = """
    INSERT INTO users (email, password)
    VALUES (?, ?)
    """

    encrypted_password = encrypt_password(password)
    cursor.execute(insert_statement, (email, encrypted_password))
    connection.commit()

def authenticate_user(connection: sqlite3.Connection, email: str, password: str):
    cursor = connection.cursor()

    cursor.execute("SELECT password FROM users WHERE email=?", (email,))
    result = cursor.fetchone()

    if result is not None:
        stored_password = result[0]
        return encrypt_password(password) == stored_password

    return False