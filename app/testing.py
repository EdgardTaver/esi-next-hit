# functions useful for testing

import sqlite3


def start_sqlite_in_memory_database_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    return conn
