FROM python:3.6

MAINTAINER hulk.oh "snuboy89@gmail.com"

ENV TZ ROK

WORKDIR /usr/src/app

ADD requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY ./hulk_telebot /hulk_telebot/
WORKDIR /hulk_telebot

EXPOSE 80
CMD ["python", "testbot.py" "--token" "YOUR TOKEN HERE"]