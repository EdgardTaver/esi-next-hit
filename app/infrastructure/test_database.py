from app.infrastructure.database import create_users_table, authenticate_user, register_user
from app.testing import start_sqlite_in_memory_database_connection
from app.exceptions import EmailAlreadyRegisteredException
import pytest


def test_create_users_table():
    connection = start_sqlite_in_memory_database_connection()
    cursor = connection.cursor()
    
    create_users_table(connection)

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
    result = cursor.fetchone()
    
    cursor.close()

    assert result is not None

def test_register_user_when_email_is_new():
    connection = start_sqlite_in_memory_database_connection()
    create_users_table(connection)

    new_email = "test@example.com"
    new_password = "password123"
    register_user(connection, new_email, new_password)

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE email=?", (new_email,))
    result = cursor.fetchone()

    assert result is not None
    assert result[1] == new_email

    cursor.close()

def test_register_user_when_email_already_exists():
    connection = start_sqlite_in_memory_database_connection()
    create_users_table(connection)

    existing_email = "test@example.com"
    existing_password = "password123"
    register_user(connection, existing_email, existing_password)

    new_password = "password456"

    with pytest.raises(EmailAlreadyRegisteredException):
        register_user(connection, existing_email, new_password)

    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM users WHERE email=?", (existing_email,))
    result = cursor.fetchone()

    assert result[0] == 1

    cursor.close()

def test_authenticate_user_when_email_is_not_registered():
    connection = start_sqlite_in_memory_database_connection()
    create_users_table(connection)

    existing_email = "test@example.com"
    existing_password = "password123"
    register_user(connection, existing_email, existing_password)

    non_existing_email = "cachorro@banana.com"
    any_password = "password456"

    result = authenticate_user(connection, non_existing_email, any_password)
    assert result is False

def test_authenticate_user_when_email_exists_but_password_is_incorrect():
    connection = start_sqlite_in_memory_database_connection()
    create_users_table(connection)

    existing_email = "test@example.com"
    existing_password = "password123"
    register_user(connection, existing_email, existing_password)

    wrong_password = "cachorro_banana"
    result = authenticate_user(connection, existing_email, wrong_password)
    assert result is False

def test_authenticate_user_when_email_exists_and_password_is_correct():
    connection = start_sqlite_in_memory_database_connection()
    create_users_table(connection)

    existing_email = "test@example.com"
    existing_password = "password123"
    register_user(connection, existing_email, existing_password)

    result = authenticate_user(connection, existing_email, existing_password)
    assert result is True