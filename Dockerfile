FROM python:3.11.1
COPY . .
RUN pip install -r requirements.txt
CMD python3 main_bot.py
