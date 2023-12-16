from app.infrastructure.database import create_users_table
from app.testing import start_sqlite_in_memory_database_connection


def test_create_users_table():
    connection = start_sqlite_in_memory_database_connection()
    cursor = connection.cursor()
    
    create_users_table(connection)

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
    result = cursor.fetchone()
    
    cursor.close()

    assert result is not None
