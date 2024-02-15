import json
import sqlite3
import time

from belpost_request import get_data
from db_manager import get_chat_id, get_value_from_db, update_track_data
from main_bot import send_message
from test_json import data


def checking():
    connection = sqlite3.connect('belpost_tracker.db')
    try:
        cursor = connection.cursor()
        cursor.execute(
            'SELECT track FROM tracks WHERE is_active IS NOT FALSE',
        )
        rows = cursor.fetchall()
        print(rows)

        for i in rows:
            track = i[0]

            # request_data = data
            while True:
                try:
                    request_data = get_data(track)

                    if request_data != get_value_from_db(track):
                        if request_data[-1].get('event') == 'Вручено':
                            update_track_data(track, request_data, False)
                            print('Вручено')
                            send_message(
                                chat_id=get_chat_id(track),
                                message='Вручено!'
                            )

                        else:
                            update_track_data(track, request_data, True)
                            print(f'Data for {track} has changed')
                    else:
                        print(f'No new data for {track}')
                        time.sleep(60)
                        continue

                except Exception as e:
                    print(
                        f"An error occurred while getting data for {track}: {e}"
                    )
                    time.sleep(300)
    except Exception as e:
        print("An error occurred:", e)
    finally:
        connection.close()
        print('All done!')


def main():
    checking()


if __name__ == "__main__":
    main()
