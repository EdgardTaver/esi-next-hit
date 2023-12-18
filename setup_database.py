import pandas as pd

from app.infrastructure.database import create_music_table, create_playlists_table, create_playlist_music_table, create_users_table, start_users_database_connection
from app.config import MUSICS_CSV_FILE

if __name__ == "__main__":
    connection = start_users_database_connection()
    create_users_table(connection)
    create_music_table(connection)
    create_playlists_table(connection)
    create_playlist_music_table(connection)

    musics_df = pd.read_csv(MUSICS_CSV_FILE)
    musics_df.to_sql("musics", connection, if_exists="append", index=False)

    connection.close()