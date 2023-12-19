import pandas as pd

from app.config import MUSICS_CSV_FILE
from app.backend.database import (create_music_table,
                                         create_playlist_music_table,
                                         create_playlists_table,
                                         create_users_table,
                                         start_users_database_connection)

if __name__ == "__main__":
    connection = start_users_database_connection()
    create_users_table(connection)
    create_music_table(connection)
    create_playlists_table(connection)
    create_playlist_music_table(connection)

    cursor = connection.cursor()

    select_musics = """
    SELECT COUNT(*) FROM musics
    """

    cursor.execute(select_musics)
    musics_count = cursor.fetchone()[0]

    if musics_count == 0:
        musics_df = pd.read_csv(MUSICS_CSV_FILE)
        musics_df.to_sql("musics", connection, if_exists="append", index=False)

    cursor.close()
    connection.close()