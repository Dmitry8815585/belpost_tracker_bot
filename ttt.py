import sqlite3


def update_track_data(track, new_data):
    """Update track data in DB."""
    try:
        connection = sqlite3.connect('belpost_tracker.db')
        cursor = connection.cursor()

        cursor.execute(
            'UPDATE tracks SET is_active = ? WHERE track <> ?',
            (new_data, track)
        )

        connection.commit()
        print(f"Data of {track} is update!")
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        connection.close()


update_track_data('BV280488510BY', False)
