import telebot
import argparse
from dbhelper import DBHelper
import sqlite3

## DB Setup section
db = DBHelper()
db.setup()


#user_id = message.chat.id
#text = message.text

help_string = """
HULK TODO APP
- /조회 : 내 TODO List를 조회합니다.
- /추가 <할 일>: 내 TODO List에 등록합니다.
- /삭제 <숫자> : x번째 할 일을 삭제합니다.
"""

get_items_string = """
       할 일
--------------------
{}
--------------------
"""

def make_telebot(token_string):
    bot = telebot.TeleBot(token_string)

    @bot.message_handler(commands=['start', 'help'])
    def send_welcome(message):
        bot.reply_to(message, help_string)


    @bot.message_handler(commands=['조회'])
    def get_items(message):
        def get_items_with_id(telegram_id):
            
            
            lists = db.get_items(message.chat.id)
            lists = ["{} ".format(i+1) + l for i, l in enumerate(lists)]
            liststring = '\n'.join(lists)
            bot.reply_to(message, 
                         get_items_string.format(liststring))

        texts = message.text.split(' ')
        try:
            get_items_with_id(message.chat.id)
        except:
            bot.reply_to(message, "유저가 존재하지 않습니다. 먼저 등록해주세요.")

    @bot.message_handler(commands=['추가'])
    def add_item(message):
        texts = message.text.split(' ')
        todo_text = ' '.join(texts[1:])
        if len(texts) == 1:  # 커맨드만 왔을 때
            bot.reply_to(message, "추가할 일을 적어주세요")
        else:
            lists = db.add_item(todo_text, message.chat.id)
            bot.reply_to(message, 
                         "할일 '{}'가 추가되었습니다.".format(todo_text))
    
    @bot.message_handler(commands=['삭제'])
    def delete_item(message):
        texts = message.text.split(' ')
        if len(texts) == 1:  # 커맨드만 왔을 때
            bot.reply_to(message, "삭제할 숫자를 적어주세요.")
        else:
            args = ' '.join(texts[1:])
            del_idxs = [int(s) - 1  #유저는 1번부터 셀테니까..
                         for s in args.split() if s.isdigit()]
            del_idxs = [i for i in del_idxs if i >= 0]
            del_idxs.sort()

            lists = db.get_items(message.chat.id)
            
            deleted = []
            for idx in del_idxs:
                if idx > len(lists):
                    break
                deleted.append(idx)
                db.delete_item(lists[idx], message.chat.id)
            del_lists = [lists[i] for i in deleted]
            deleted_text  = '\n'.join(del_lists)
            
            bot.reply_to(message, 
                         "할일 \n{}\n가 삭제되었습니다.".format(deleted_text))

    bot.polling()

parser = argparse.ArgumentParser(description='telegram bot')
parser.add_argument('--token', 
                    dest='token',
                    required=True,
                    type=str,
                    help='bot api token key')

args = parser.parse_args()
print("start bot with token {}".format(args.token))
make_telebot(args.token)