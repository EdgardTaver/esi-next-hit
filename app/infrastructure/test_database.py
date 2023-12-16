import sqlite3
from app.infrastructure.database import create_users_table

def test_create_users_table():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    create_users_table()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
    result = cursor.fetchone()

    assert result is not None