import os
import sqlite3
import time

from dotenv import load_dotenv
from telegram import Bot

from belpost_request import get_data
from db_manager import get_chat_id, get_value_from_db, update_track_data
# from test_json import data

load_dotenv()

bot = Bot(os.getenv('TOKEN'))

REQUEST_TIME_DELAY = 120


def send_message(chat_id, message):
    """Send message response."""
    bot.send_message(chat_id, message)


def checking():
    '''Start checking all active tracks in database.'''
    while True:
        try:
            with sqlite3.connect('belpost_tracker.db') as connection:
                cursor = connection.cursor()
                cursor.execute(
                    'SELECT track FROM tracks WHERE is_active IS NOT FALSE',
                )
                rows = cursor.fetchall()

                if not rows:
                    print('No active tracks to check. Exiting...')
                    send_message(
                        chat_id=5805839575,
                        message='No active tracks to check. Exiting...'
                    )
                    # continue

                print(rows)

                for i in rows:
                    track = i[0]

                    try:
                        chat_id = get_chat_id(track)

                        request_data = get_data(track)
                        if request_data != get_value_from_db(track):
                            if request_data[-1].get('event') == 'Вручено':
                                update_track_data(track, request_data, False)
                                print(f'The parcel {track} has been delivered')
                                send_message(
                                    chat_id=chat_id,
                                    message=(
                                        f'The parcel {track}'
                                        + ' has been delivered'
                                    )
                                )

                            else:
                                update_track_data(track, request_data, True)
                                print(f'Data for {track} has changed')
                                send_message(
                                    chat_id=chat_id,
                                    message=f'Data for {track} has changed'
                                )
                        else:
                            print(f'No new data for {track}')
                            send_message(
                                chat_id=chat_id,
                                message=f'No new data for {track}'
                            )
                        time.sleep(10)

                    except Exception as e:
                        print(
                            "An error occurred while getting "
                            + f"data for {track}: {e}"
                        )
                        send_message(
                            chat_id=chat_id,
                            message=(
                                "An error occurred while getting "
                                + f"data for {track}: {e}"
                            )
                        )

        except sqlite3.Error as e:
            print(f"Database error: {e}")

        time.sleep(REQUEST_TIME_DELAY)


def main():
    checking()


if __name__ == "__main__":
    main()
