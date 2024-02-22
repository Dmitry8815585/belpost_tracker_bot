import os
import threading

from dotenv import load_dotenv
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    CommandHandler, Filters, MessageHandler, Updater, CallbackQueryHandler
)

from checking import checking
from db_manager import (
    check_track_in_db, create_track, create_user, get_value_from_db,
    list_my_tracks, update_track_data, create_database
)
from logger import setup_logger
from belpost_request import get_data

load_dotenv()

bot = Bot(os.getenv('TOKEN'))

updater = Updater(token=os.getenv('TOKEN'))

logger = setup_logger()

create_database()


def send_message(chat_id, message):
    """Send message response."""
    bot.send_message(chat_id, message)


def send_response_messages(chat_id: str, response_data: list):
    """Send response messages with data."""
    for i in response_data:
        response_message = (
            f"{i.get('created_at')}\n"
            f"{i.get('event')}\n{i.get('place')}"
        )
        send_message(chat_id=chat_id, message=response_message)


def track_selection(update, context):
    query = update.callback_query
    track_text = query.data
    chat_id = query.message.chat_id
    context.bot.send_message(chat_id, f"You selected track: {track_text}")
    send_response_messages(chat_id, get_value_from_db(track_text))


def list_tracks(update, context):
    chat_id = update.effective_chat.id
    value, tracks = list_my_tracks(chat_id)
    if not value:
        send_message(chat_id, tracks)
    else:
        buttons = []
        for track_text in tracks:
            buttons.append(
                [InlineKeyboardButton(track_text, callback_data=track_text)]
            )
        reply_markup = InlineKeyboardMarkup(buttons)
        context.bot.send_message(
            chat_id, "Ваши трек-коды:", reply_markup=reply_markup
        )
        context.dispatcher.add_handler(CallbackQueryHandler(track_selection))


def wake_up(update, context):
    chat = update.effective_chat
    context.bot.send_message(
        chat_id=chat.id,
        text=(
            'Спасибо, что включили меня\n'
            'Отправте мне код-трек Вашей посылки!\n'
            'Буквы могут быть в любом регистре!'
        )
    )
    message = update.message

    create_user(
        message.chat.id,
        message.chat.username,
        message.chat.first_name
    )


def get_status(update, context):
    """Main function."""
    message = update.message
    chat_id = message.chat_id
    text = (message.text).upper()

    track_exists, track_data = check_track_in_db(text)
    if track_exists:
        send_message(chat_id, 'Отслеживание завершено.')
        send_response_messages(chat_id=chat_id, response_data=track_data)
        return

    response_data = get_data(text)  # Get data

    if isinstance(response_data, list):

        if response_data[-1].get('event') == 'Вручено':
            send_message(chat_id=chat_id, message='Посылка вручена!')
            logger.info(f'Parsel {text} has been delivered.')
            update_track_data(text, response_data, False)
            send_response_messages(chat_id, response_data)
        else:
            success, response_message = create_track(
                text, chat_id, response_data
            )

            if success:
                send_message(chat_id=chat_id, message=response_message)
                send_response_messages(chat_id, response_data)

            else:
                send_message(chat_id=chat_id, message=response_message)
                send_response_messages(chat_id, response_data)
    else:
        send_message(chat_id=chat_id, message=response_data)


updater.dispatcher.add_handler(CommandHandler('start', wake_up))
updater.dispatcher.add_handler(CommandHandler('list', list_tracks))
updater.dispatcher.add_handler(MessageHandler(Filters.text, get_status))

threading.Thread(target=checking).start()  # strat checking function

updater.start_polling()

updater.idle()
