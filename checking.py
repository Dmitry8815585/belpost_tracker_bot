import json
import sqlite3
import time

from belpost_request import get_data
from db_manager import get_chat_id, get_value_from_db, update_track_data
# from main_bot import send_message
from test_json import data


def checking():
    while True:
        connection = sqlite3.connect('belpost_tracker.db')
        cursor = connection.cursor()
        cursor.execute(
            'SELECT track FROM tracks WHERE is_active IS NOT FALSE',
        )
        rows = cursor.fetchall()

        if not rows:
            connection.close()
            print('No tracks to check. Exiting...')
            return

        print(rows)

        for i in rows:
            track = i[0]

            try:
                request_data = get_data(track)
                time.sleep(5)
                if request_data != get_value_from_db(track):
                    if request_data[-1].get('event') == 'Вручено':
                        update_track_data(track, request_data, False)
                        print('Вручено')

                    else:
                        update_track_data(track, request_data, True)
                        print(f'Data for {track} has changed')
                else:
                    print(f'No new data for {track}')

            except Exception as e:
                print(
                    f"An error occurred while getting data for {track}: {e}"
                )
                time.sleep(5)
        connection.close()
        print('Loop done!')
        time.sleep(5)
        continue


def main():
    checking()


if __name__ == "__main__":
    main()
