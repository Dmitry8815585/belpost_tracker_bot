from datetime import datetime
import json
import sqlite3

import pytz

# from test_json import data


def create_user(chat_id, username, first_name):
    """Adding new user to DB using data from message."""

    try:
        connection = sqlite3.connect('belpost_tracker.db')
        cursor = connection.cursor()

        cursor.execute(
            """CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    chat_id INTEGER UNIQUE,
                    username TEXT,
                    first_name TEXT,
                    date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )"""
        )

        connection.execute(
            'INSERT INTO users (chat_id, username, first_name, date_added)'
            + ' VALUES (?, ?, ?, datetime("now"))', (
                chat_id, f'@{username}', first_name
            )
        )
        connection.commit()
    except sqlite3.IntegrityError:
        pass
    finally:
        connection.close()


def create_track(track, user_id, response_data):
    """Adding track data to DB."""
    try:
        connection = sqlite3.connect('belpost_tracker.db')
        cursor = connection.cursor()

        cursor.execute(
            """CREATE TABLE IF NOT EXISTS tracks (
                    track_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    track TEXT UNIQUE,
                    data TEXT,
                    user_id INTEGER,
                    date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    is_active BOOLEAN DEFAULT 1,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
            )"""
        )

        cursor.execute(
            'SELECT user_id FROM users WHERE chat_id = ?', (user_id,)
        )
        row = cursor.fetchone()

        response_data_json = json.dumps(response_data)

        minsk_tz = pytz.timezone('Europe/Minsk')
        current_time = datetime.now(minsk_tz)

        connection.execute(
            '''
            INSERT INTO tracks (track, data, user_id, date_added)
            VALUES (?, ?, ?, ?)
            ''',
            (track, response_data_json, row[0], current_time)
        )
        connection.commit()
        return True, "The track has been successfully added to the database!"

    except sqlite3.IntegrityError:
        return False, "Track already being tracked!"

    finally:
        connection.close()


def update_track_data(track, new_data, is_active):
    """Update track data in DB."""
    try:
        connection = sqlite3.connect('belpost_tracker.db')
        cursor = connection.cursor()

        serialized_new_data = json.dumps(new_data)

        cursor.execute(
            '''
            UPDATE tracks SET
            data = ?,
            is_active = ?
            WHERE track = ?
            ''',
            (serialized_new_data, is_active, track)
        )

        connection.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        connection.close()


def delete_track(track, user_id):
    """Delete track from DB."""
    try:
        connection = sqlite3.connect('belpost_tracker.db')
        cursor = connection.cursor()

        cursor.execute(
            'DELETE FROM tracks WHERE track = ? AND user_id = ?',
            (track, user_id)
        )

        connection.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        connection.close()


def get_value_from_db(text: str) -> list:
    """Return list(data) text value from DB."""
    connection = sqlite3.connect('belpost_tracker.db')
    cursor = connection.cursor()

    cursor.execute(
            'SELECT data FROM tracks WHERE track = ?', (text,)
    )
    data = cursor.fetchone()

    if data is None or data[0] is None:
        return []
    return json.loads(data[0])


def get_chat_id(text: str) -> list:
    """Return chat_id using track."""
    connection = sqlite3.connect('belpost_tracker.db')
    cursor = connection.cursor()

    cursor.execute(
            'SELECT user_id FROM tracks WHERE track = ?', (text,)
    )
    user_id = cursor.fetchone()

    cursor.execute(
        'SELECT chat_id FROM users WHERE user_id = ?', user_id
    )

    return cursor.fetchone()[0]


def main():
    print(get_chat_id('NEWDATA'))


if __name__ == "__main__":
    main()
