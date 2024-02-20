import os
import sqlite3
import time

from dotenv import load_dotenv
from telegram import Bot

# from belpost_request import get_data
from db_manager import get_chat_id, get_value_from_db, update_track_data
from logger import setup_logger
from test_json import data

load_dotenv()

bot = Bot(os.getenv('TOKEN'))

REQUEST_TIME_DELAY = 120

logger = setup_logger()


def send_message(chat_id, message):
    '''Send message response.'''
    bot.send_message(chat_id, message)


def send_new_data_messages(chat_id, response_data):
    """Send new data to telegram"""
    response_message = (
        f"{response_data.get('created_at')}\n"
        f"{response_data.get('event')}\n"
        f"{response_data.get('place')}"
    )
    send_message(chat_id=chat_id, message=response_message)


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
                    logger.info('There are no tracks in the database to check')

                for i in rows:
                    track = i[0]

                    try:
                        chat_id = get_chat_id(track)

                        request_data = data  # get_data(track)

                        if request_data != get_value_from_db(track):
                            if request_data[-1].get('event') == 'Вручено':
                                update_track_data(track, request_data, False)
                                logger.info(
                                    f'The parcel "{track}" has been delivered'
                                )
                                send_new_data_messages(
                                    chat_id, request_data[-1]
                                )
                                send_message(
                                    chat_id=chat_id,
                                    message=(
                                        f'The parcel {track}'
                                        + ' has been delivered'
                                    )
                                )
                                send_message(
                                    chat_id=chat_id, message="\U0001F600"
                                )

                            else:
                                update_track_data(track, request_data, True)
                                logger.info(f'Data for {track} has changed')
                                send_new_data_messages(
                                    chat_id, request_data[-1]
                                )
                        else:
                            logger.info(f'No new data for {track}')

                        time.sleep(10)

                    except Exception as e:
                        logger.error(
                            f"An error {e} occurred while getting "
                            + f"data for {track}"
                        )

        except sqlite3.Error as e:
            logger.error(f"Database error: {e}")

        time.sleep(REQUEST_TIME_DELAY)


def main():
    checking()


if __name__ == "__main__":
    main()
