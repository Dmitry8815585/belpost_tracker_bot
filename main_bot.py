import os

from dotenv import load_dotenv
from telegram import Bot
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

from db_manager import create_track, create_user
from belpost_request import get_data
from test_json import data

load_dotenv()

bot = Bot(os.getenv('TOKEN'))

updater = Updater(token=os.getenv('TOKEN'))


def send_message(chat_id, message):
    """Send message response."""
    bot.send_message(chat_id, message)


def wake_up(update, context):
    chat = update.effective_chat
    context.bot.send_message(
        chat_id=chat.id,
        text=(
            'Спасибо, что включили меня\n Отправте мне код Вашей посылки!'
            '\nПисать буквы можно в любом регистре!'
        )
    )
    message = update.message

    create_user(
        message.chat.id,
        message.chat.username,
        message.chat.first_name
    )


def get_status(update, context):
    message = update.message
    chat_id = message.chat_id
    text = (message.text).upper()

    response_data = data
    # response_data = get_data(text)  # Get data

    if isinstance(response_data, list):

        if response_data[-1].get('event') == 'Вручено':
            send_message(chat_id=chat_id, message='Посылка вручена!')

            for i in response_data:
                response_message = (
                    f"{i.get('created_at')}\n"
                    f"{i.get('event')}\n{i.get('place')}"
                )
                send_message(chat_id=chat_id, message=response_message)
        else:
            success, response_message = create_track(
                text, chat_id, response_data
            )

            if success:
                send_message(chat_id=chat_id, message=response_message)

                for i in response_data:
                    response_message = (
                        f"{i.get('created_at')}\n"
                        f"{i.get('event')}\n{i.get('place')}"
                    )
                    send_message(chat_id=chat_id, message=response_message)
            else:
                send_message(chat_id=chat_id, message=response_message)

                for i in response_data:
                    response_message = (
                        f"{i.get('created_at')}\n"
                        f"{i.get('event')}\n{i.get('place')}"
                    )
                    send_message(chat_id=chat_id, message=response_message)
    else:
        send_message(chat_id=chat_id, message=response_data)


updater.dispatcher.add_handler(CommandHandler('start', wake_up))
updater.dispatcher.add_handler(MessageHandler(Filters.text, get_status))

updater.start_polling()

updater.idle()
