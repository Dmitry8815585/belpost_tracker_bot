import json
import sqlite3
from ast import List, Tuple
from contextlib import contextmanager

from logger import setup_logger

logger = setup_logger()
DATABASE_NAME = 'belpost_tracker.db'


@contextmanager
def database_connection():
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()
    try:
        yield cursor
    finally:
        connection.commit()
        connection.close()


def execute_query(query: str, params: Tuple = None):
    with database_connection() as cursor:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)


def delete_track() -> None:
    query = """
    DELETE FROM tracks
    """
    execute_query(query)
    print('Data from track is deleted.')


def create_database() -> None:
    create_users_table_query = """
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        chat_id INTEGER UNIQUE,
        username TEXT,
        first_name TEXT,
        date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """

    create_tracks_table_query = """
    CREATE TABLE IF NOT EXISTS tracks (
        track_id INTEGER PRIMARY KEY AUTOINCREMENT,
        track TEXT UNIQUE,
        data TEXT,
        user_id INTEGER,
        date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        is_active BOOLEAN DEFAULT 1,
        FOREIGN KEY (user_id) REFERENCES users (user_id)
    )
    """

    execute_query(create_users_table_query)
    execute_query(create_tracks_table_query)


def create_user(chat_id, username, first_name):
    try:
        query = """
        INSERT INTO users (chat_id, username, first_name, date_added)
        VALUES (?, ?, ?, datetime('now'))
        """
        execute_query(query, (chat_id, username, first_name))
        logger.info(f"User {first_name} (@{username}) added successfully.")
    except sqlite3.IntegrityError:
        logger.error(
            f"User {first_name} (@{username}) already exists in the database!"
        )


def create_track(track, chat_id, response_data):
    try:
        query = """
        INSERT INTO tracks (track, data, user_id, date_added)
        SELECT ?, ?, users.user_id, datetime('now')
        FROM users
        WHERE users.chat_id = ?
        """
        response_data_json = json.dumps(response_data)
        execute_query(query, (track, response_data_json, chat_id))
        logger.info(f"The track '{track}' has been added to the database!")
        return True, "Трек-код успешно добавлен в базу данных."
    except sqlite3.IntegrityError:
        logger.info(f"The track '{track}' already exists in the database!")
        return False, "Трек уже существует в базе данных."


def update_track_data(track, new_data, is_active):
    try:
        query = """
        UPDATE tracks SET data = ?, is_active = ? WHERE track = ?
        """
        execute_query(query, (json.dumps(new_data), is_active, track))
        logger.info(f'Track "{track}" has been updated')
        return True
    except sqlite3.Error:
        logger.error(f'Error updating track "{track}"')
        return False


def get_value_from_db(track: str) -> List:
    query = """
    SELECT data FROM tracks WHERE track = ?
    """
    with database_connection() as cursor:
        cursor.execute(query, (track,))
        data = cursor.fetchone()
        return json.loads(data[0]) if data and data[0] else []


def get_chat_id(track: str):
    query = """
    SELECT chat_id FROM users
    JOIN tracks ON users.user_id = tracks.user_id
    WHERE track = ?
    """
    with database_connection() as cursor:
        cursor.execute(query, (track,))
        result = cursor.fetchone()
        if result is None:
            logger.error(f"No chat_id found for track: {track}")
            return None
        return result[0]


def check_track_in_db(track: str) -> Tuple:
    query = """
    SELECT data FROM tracks WHERE track = ? AND is_active = 0
    """
    with database_connection() as cursor:
        cursor.execute(query, (track,))
        data = cursor.fetchone()
        return (True, json.loads(data[0])) if data else (False, [])


def list_my_tracks(chat_id: str) -> Tuple:
    query = """
    SELECT track FROM tracks
    JOIN users ON users.user_id = tracks.user_id
    WHERE users.chat_id = ? AND tracks.is_active = 1
    """
    with database_connection() as cursor:
        cursor.execute(query, (chat_id,))
        tracks = cursor.fetchall()
        tracks = [track[0] for track in tracks]
        if not tracks:
            return False, 'У Вас нет активных трек-кодов.'
        else:
            return True, tracks


def main():
    pass


if __name__ == "__main__":
    main()


# def main():
#     print(list_my_tracks('5805839575'))


# if __name__ == "__main__":
#     main()
