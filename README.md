# Проект: Телеграм-бот для отслеживания посылок

##  [Статус посылки Белпочты бот](https://t.me/belpost_tracker_status_bot)

## Стек навыков проекта:

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) ![Telegram API](https://img.shields.io/badge/Telegram_API-26A5E4?style=for-the-badge&logo=telegram&logoColor=white) ![Logging](https://img.shields.io/badge/Logging-292929?style=for-the-badge&logo=logging&logoColor=white) ![API Requests](https://img.shields.io/badge/API_Requests-009688?style=for-the-badge&logo=requests&logoColor=white)![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)


## Описание проекта

Этот проект представляет собой телеграм-бота, который позволяет пользователям отслеживать свои посылки по трек-коду. Пользователи могут отправлять трек-коды посылок боту, и бот будет периодически проверять статус посылок и уведомлять пользователей о их движении.

 
## Как использовать

1. Подключитесь к боту, отправив команду /start.
2. Бот запросит у вас трек-код для отслеживания посылки.
3. Вы можете отправить один или несколько трек-кодов.
4. Бот сохранит трек-коды в базу данных SQLite.
5. Бот будет периодически проверять статус посылок.
6. Когда посылка будет доставлена, вы получите сообщение о ее статусе.
7. Если вы отправите трек-код, который уже доставлен, бот вышлет вам историю движения посылки.

## Запуск проекта

Для запуска в Docker контейнере:
    Создайте файл .env в корне проекта по образцу файла .env.example.
    Создайте образ и контейнер Docker.

## Важно

1. Бот использует базу данных SQLite для хранения трек-кодов и их статусов.
2. Для периодической проверки статусов посылок используется модуль threading, для многопоточности, в частности, threading.Thread(target=checking).start(), для запуска фонового процесса проверки.
3. Для запуска в Docker контейнере, обязательно наличие файла .env в корне проекта.
4. События логируются в файл main.log
