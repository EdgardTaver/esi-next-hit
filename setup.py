import pandas as pd

from app.backend.config import MUSICS_CSV_FILE
from app.backend.database import (database_fill_up_musics_table,
                                  database_setup,
                                  start_users_database_connection)

if __name__ == "__main__":
    connection = start_users_database_connection()
    
    database_setup(connection)
    database_fill_up_musics_table(connection)
    
    connection.close()
