import json
import sqlite3

from test_json import data


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

        connection.execute(
            '''
            INSERT INTO tracks (track, data, user_id, date_added)
            VALUES (?, ?, ?, datetime("now"))
            ''',
            (track, response_data_json, row[0])
        )
        connection.commit()
        return True, "Data added to the database successfully!"

    except sqlite3.IntegrityError:
        return False, "Track already being tracked!"

    finally:
        connection.close()


def update_track_data(track, new_data):
    """Update track data in DB."""
    try:
        connection = sqlite3.connect('belpost_tracker.db')
        cursor = connection.cursor()

        serialized_new_data = json.dumps(new_data)

        cursor.execute(
            'UPDATE tracks SET data = ? WHERE track = ?',
            (serialized_new_data, track)
        )

        connection.commit()
        print(f"Data of {track} is update!")
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


def main():
    update_track_data('FIRST', data)


if __name__ == "__main__":
    main()
