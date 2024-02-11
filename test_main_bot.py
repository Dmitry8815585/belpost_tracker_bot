import os

from dotenv import load_dotenv
from telegram import Bot
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

from db_manager import create_track, create_user

load_dotenv()

bot = Bot(os.getenv('TOKEN'))

updater = Updater(token=os.getenv('TOKEN'))

TRACKER = os.getenv('TRACKER')


def send_message(chat_id, message):
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

    if create_track(text, message.chat.id):
        response_message = "Data added to the database successfully!"
    else:
        response_message = f"Track {text} already exists."

    context.bot.send_message(chat_id=chat_id, text=response_message)

    # while True:
    #     new_data = get_data(text)

    #     if new_data != get_value_from_db(text):
    #         update_track_data(text, new_data)

    #     if new_data[-1].get('value') == 'Вручено':
    #         break


updater.dispatcher.add_handler(CommandHandler('start', wake_up))
updater.dispatcher.add_handler(MessageHandler(Filters.text, get_status))

# Метод start_polling() запускает процесс polling,
# приложение начнёт отправлять регулярные запросы для получения обновлений.
updater.start_polling()
# Бот будет работать до тех пор, пока не нажмете Ctrl-C
updater.idle()
