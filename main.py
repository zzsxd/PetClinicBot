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
import json
import base64
import datetime
from threading import Lock
from config_parser import ConfigParser
from backend import TempUserData, DbAct
from frontend import Bot_inline_btns
from db import DB


def get_calendar(message):
    current_date = datetime.datetime.now


def cart_visualize(data, s=''):
    fields = {0: 'Кличка', 1: 'Номер телефона', 2: 'Жалобы', 3: 'Рентген', 4: 'Узи', 5: 'Диагноз', 6: 'Операции'}
    # На индексе 7 в этом цикле появляется массив с фотограиями в виде байт строки, я не знаю как их отправить в сообщении (их много)
    for index, el in enumerate(data):
        if index == 7:
            photos = json.loads(el)
        else:
            s += f'<b>{fields[index]}</b> {el}\n'
    return s


def main():
    @bot.message_handler(commands=['start'])
    def start_msg(message):
        user_id = message.from_user.id
        buttons = Bot_inline_btns()
        db_actions.add_user(user_id, message.from_user.first_name, message.from_user.last_name,
                            f'@{message.from_user.username}')
        bot.send_message(user_id, 'start msg', reply_markup=buttons.start_btns())

    @bot.message_handler(content_types=['text', 'photo'])
    def text_msg(message):
        user_id = message.chat.id
        user_input = message.text
        photo = message.photo
        buttons = Bot_inline_btns()
        code = temp_user_data.temp_data(user_id)[user_id][0]
        if db_actions.user_is_existed(user_id):
            match code:
                case 0:
                    if user_input is not None:
                        temp_user_data.temp_data(user_id)[user_id][1][0] = user_input
                        temp_user_data.temp_data(user_id)[user_id][0] = 1
                        bot.send_message(user_id, 'введите номер телефона собаки')
                    else:
                        bot.send_message(user_id, 'ti pidor')
                case 1:
                    if user_input is not None:
                        temp_user_data.temp_data(user_id)[user_id][1][1] = user_input
                        temp_user_data.temp_data(user_id)[user_id][0] = 2
                        bot.send_message(user_id, 'введите жалобы животного')
                    else:
                        bot.send_message(user_id, 'ti pidor')
                case 2:
                    if user_input is not None:
                        temp_user_data.temp_data(user_id)[user_id][1][2] = user_input
                        temp_user_data.temp_data(user_id)[user_id][0] = 3
                        bot.send_message(user_id, 'введите результаты рентгена')
                    else:
                        bot.send_message(user_id, 'ti pidor')
                case 3:
                    if user_input is not None:
                        temp_user_data.temp_data(user_id)[user_id][1][3] = user_input
                        temp_user_data.temp_data(user_id)[user_id][0] = 4
                        bot.send_message(user_id, 'введите результаты узи')
                    else:
                        bot.send_message(user_id, 'ti pidor')
                case 4:
                    if user_input is not None:
                        temp_user_data.temp_data(user_id)[user_id][1][4] = user_input
                        temp_user_data.temp_data(user_id)[user_id][0] = 5
                        bot.send_message(user_id, 'введите диагнозы')
                    else:
                        bot.send_message(user_id, 'ti pidor')
                case 5:
                    if user_input is not None:
                        temp_user_data.temp_data(user_id)[user_id][1][5] = user_input
                        temp_user_data.temp_data(user_id)[user_id][0] = 6
                        bot.send_message(user_id, 'введите операции')
                    else:
                        bot.send_message(user_id, 'ti pidor')
                case 6:
                    if user_input is not None:
                        temp_user_data.temp_data(user_id)[user_id][1][6] = user_input
                        temp_user_data.temp_data(user_id)[user_id][0] = None
                        db_actions.add_your_mom(temp_user_data.temp_data(user_id)[user_id][1])
                        bot.send_message(user_id, 'Животное добавлено!')
                    else:
                        bot.send_message(user_id, 'ti pidor')
                case 7:
                    if user_input is not None:
                        animals = db_actions.get_animal(user_input)
                        if len(animals) != 0:
                            temp_user_data.temp_data(user_id)[user_id][0] = None
                            for pidor in animals:
                                bot.send_message(user_id, f'Карта больного:\n\n{cart_visualize(pidor[1:])}', parse_mode='html', reply_markup=buttons.change_pidor_btns(pidor[0]))
                        else:
                            bot.send_message(user_id, 'Животное не найдено')
                    else:
                        bot.send_message(user_id, 'ti pidor')
                case 8:
                    if photo is not None:
                        photo_id = photo[-1].file_id
                        photo_file = bot.get_file(photo_id)
                        photo_base64 = base64.b64encode(bot.download_file(photo_file.file_path)).decode('latin1')
                        db_actions.add_photo_to_pidor(temp_user_data.temp_data(user_id)[user_id][2], photo_base64)
                        bot.send_message(user_id, 'Операция совершена успешно!')
                    else:
                        bot.send_message(user_id, 'ti axuel')

    @bot.callback_query_handler(func=lambda call: True)
    def callback(call):
        buttons = Bot_inline_btns()
        user_id = call.message.chat.id
        if db_actions.user_is_existed(user_id):
            if call.data == 'search':
                temp_user_data.temp_data(user_id)[user_id][0] = 7
                bot.send_message(call.message.chat.id, 'Введите кличку или номер животного')

            elif call.data == 'calendar':
                bot.send_message(call.message.chat.id, 'Календарь бота', reply_markup=buttons.calendar_day())

            elif call.data == 'zapis':
                temp_user_data.temp_data(user_id)[user_id][0] = 0
                bot.send_message(call.message.chat.id, 'введите кличку животного')

            elif call.data[:6] == 'change':
                temp_user_data.temp_data(user_id)[user_id][0] = 8
                temp_user_data.temp_data(user_id)[user_id][2] = call.data[6:]
                bot.send_message(user_id, 'Отправьте фото в формате .jpg')

    bot.polling(none_stop=True)

if '__main__' == __name__:
    os_type = platform.system()
    work_dir = os.path.dirname(os.path.realpath(__file__))
    config = ConfigParser(f'{work_dir}/{config_name}', os_type)
    temp_user_data = TempUserData()
    db = DB(config.get_config()['db_file_name'], Lock())
    db_actions = DbAct(db, config, config.get_config()['xlsx_path'])
    bot = telebot.TeleBot(config.get_config()['tg_api'])
    main()
