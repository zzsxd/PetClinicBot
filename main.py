#####################################
#            Created by             #
#               zzsxd               #
#               SBR                 #
#####################################
config_name = 'secrets.json'
#####################################

import os
import telebot
import platform
import datetime
from config_parser import ConfigParser
from backend import TempUserData
from frontend import Bot_inline_btns

def get_calendar(message):
    current_date = datetime.datetime.now

def main():
    @bot.message_handler(commands=['start'])
    def start_msg(message):
        buttons = Bot_inline_btns()
        bot.send_message(message.chat.id, 'start msg', reply_markup=buttons.start_btns())

    @bot.callback_query_handler(func=lambda call: True)
    def callback(call):
        buttons = Bot_inline_btns()

        if call.data == 'search':
            bot.send_message(call.message.chat.id, 'Поиск пациента')

        elif call.data == 'calendar':
            bot.send_message(call.message.chat.id, 'Календарь бота', reply_markup=buttons.calendar_day())

        elif call.data == 'zapis':
            bot.send_message(call.message.chat.id, 'Запись пациента')
        elif call.data == 'add':
            bot.send_message(call.message.chat.id, 'Добавить пациента')

    bot.polling(none_stop=True)

if '__main__' == __name__:
    os_type = platform.system()
    work_dir = os.path.dirname(os.path.realpath(__file__))
    config = ConfigParser(f'{work_dir}/{config_name}', os_type)
    temp_user_data = TempUserData()
    bot = telebot.TeleBot(config.get_config()['tg_api'])
    main()
