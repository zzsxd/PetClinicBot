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
import copy
import base64
import datetime
import calendar
from io import BytesIO
from telebot import types
from threading import Lock
from config_parser import ConfigParser
from backend import TempUserData, DbAct, PDFCreate
from frontend import Bot_inline_btns
from db import DB


def cart_visualize(user_id, animals, flag, s='', raw_s=''):
    fields = {0: 'Кличка', 1: 'Номер телефона', 2: 'Жалобы', 3: 'Рентген', 4: 'Узи', 5: 'Диагноз', 6: 'Операции'}
    buttons = Bot_inline_btns()
    photos = list()
    raw = list()
    # На индексе 7 в этом цикле появляется массив с фотограиями в виде байт строки, я не знаю как их отправить в
    # сообщении (их много)
    temp_user_data.temp_data(user_id)[user_id][3] = copy.deepcopy({})
    for index, pidor in enumerate(animals):
        for index, el in enumerate(pidor[1:]):
            if index == 7:
                for i in json.loads(el):
                    raw.append(base64.b64decode(i))
                    photos.append(telebot.types.InputMediaPhoto(base64.b64decode(i)))
            else:
                s += f'<b>{fields[index]}</b> {el}\n'
                raw_s += f'{fields[index]}: {el}\n'
        if not flag:
            if len(photos) != 0:
                bot.send_media_group(user_id, media=photos)
                temp_user_data.temp_data(user_id)[user_id][3].update({index: [raw, raw_s]})
            temp_user_data.temp_data(user_id)[user_id][3].update({index: [None, raw_s]})
            bot.send_message(user_id, f'Карта больного:\n\n{s}',
                             parse_mode='html', reply_markup=buttons.change_pidor_btns(pidor[0], index))
        else:
            if len(photos) != 0:
                bot.send_media_group(user_id, media=photos)
            bot.send_message(user_id, f'Карта больного:\n\n{s}',
                             parse_mode='html', reply_markup=buttons.select_pidor_btns(pidor[0]))


def main():

    @bot.message_handler(commands=['start'])
    def start_msg(message):
        user_id = message.from_user.id
        buttons = Bot_inline_btns()
        db_actions.add_user(user_id, message.from_user.first_name, message.from_user.last_name,
                            f'@{message.from_user.username}')
        bot.send_message(user_id, 'Привет! Я бот для ветеринарной клиники, выбирай действие ниже!',
                         reply_markup=buttons.start_btns())

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
                        bot.send_message(user_id, 'Введите номер телефона')
                    else:
                        bot.send_message(user_id, 'Неправильный ввод')
                case 1:
                    if user_input is not None:
                        temp_user_data.temp_data(user_id)[user_id][1][1] = user_input
                        temp_user_data.temp_data(user_id)[user_id][0] = 2
                        bot.send_message(user_id, 'Введите жалобы животного')
                    else:
                        bot.send_message(user_id, 'Неправильный ввод')
                case 2:
                    if user_input is not None:
                        temp_user_data.temp_data(user_id)[user_id][1][2] = user_input
                        temp_user_data.temp_data(user_id)[user_id][0] = 3
                        bot.send_message(user_id, 'Введите результаты рентгена')
                    else:
                        bot.send_message(user_id, 'Неправильный ввод')
                case 3:
                    if user_input is not None:
                        temp_user_data.temp_data(user_id)[user_id][1][3] = user_input
                        temp_user_data.temp_data(user_id)[user_id][0] = 4
                        bot.send_message(user_id, 'Введите результаты узи')
                    else:
                        bot.send_message(user_id, 'Неправильный ввод')
                case 4:
                    if user_input is not None:
                        temp_user_data.temp_data(user_id)[user_id][1][4] = user_input
                        temp_user_data.temp_data(user_id)[user_id][0] = 5
                        bot.send_message(user_id, 'Введите диагнозы')
                    else:
                        bot.send_message(user_id, 'Неправильный ввод')
                case 5:
                    if user_input is not None:
                        temp_user_data.temp_data(user_id)[user_id][1][5] = user_input
                        temp_user_data.temp_data(user_id)[user_id][0] = 6
                        bot.send_message(user_id, 'Введите операции')
                    else:
                        bot.send_message(user_id, 'Неправильный ввод')
                case 6:
                    if user_input is not None:
                        temp_user_data.temp_data(user_id)[user_id][1][6] = user_input
                        temp_user_data.temp_data(user_id)[user_id][0] = None
                        db_actions.add_your_mom(temp_user_data.temp_data(user_id)[user_id][1])
                        bot.send_message(user_id, 'Животное добавлено!')
                    else:
                        bot.send_message(user_id, 'Неправильный ввод')
                case 7:
                    if user_input is not None:
                        animals = db_actions.get_animal(user_input)
                        if len(animals) != 0:
                            temp_user_data.temp_data(user_id)[user_id][0] = None
                            cart_visualize(user_id, animals, False)
                        else:
                            bot.send_message(user_id, 'Животное не найдено')
                    else:
                        bot.send_message(user_id, 'Неправильный ввод')
                case 8:
                    if photo is not None:
                        photo_id = photo[-1].file_id
                        photo_file = bot.get_file(photo_id)
                        photo_base64 = base64.b64encode(bot.download_file(photo_file.file_path)).decode('latin1')
                        db_actions.add_photo_to_pidor(temp_user_data.temp_data(user_id)[user_id][2], photo_base64)
                        bot.send_message(user_id, 'Операция совершена успешно!')
                    else:
                        bot.send_message(user_id, 'Неправильный ввод')
                case 9:
                    if user_input.lower() in temp_user_data.get_month():
                        temp_user_data.temp_data(user_id)[user_id][4] = temp_user_data.get_month().index(user_input)+1
                        temp_user_data.temp_data(user_id)[user_id][0] = 10
                        days = calendar.monthrange(datetime.datetime.now().year, temp_user_data.get_month().index(user_input)+1)[1]
                        temp_user_data.temp_data(user_id)[user_id][5] = days
                        bot.send_message(user_id, 'Выберите день', reply_markup=buttons.days_btns(days))
                    else:
                        bot.send_message(user_id, 'Вы ввели неправильный месяц')
                case 10:
                    try:
                        if int(user_input) in range(1, temp_user_data.temp_data(user_id)[user_id][5]+1):
                            temp_user_data.temp_data(user_id)[user_id][5] = user_input
                            temp_user_data.temp_data(user_id)[user_id][0] = 11
                            bot.send_message(user_id, 'Выберите время в формате XX:XX')
                        else:
                            bot.send_message(user_id, 'В этом месяце нет такого числа')
                    except:
                        bot.send_message(user_id, 'Это не число')
                case 11:
                    try:
                        temp_user_data.temp_data(user_id)[user_id][6] = datetime.datetime.strptime(f'{temp_user_data.temp_data(user_id)[user_id][5]}{temp_user_data.temp_data(user_id)[user_id][4]}{datetime.datetime.now().year} {user_input}', "%d%m%Y %H:%M")
                        temp_user_data.temp_data(user_id)[user_id][0] = 12
                        bot.send_message(user_id, 'Введите кличку животного или номер телефона для поиска больного')
                    except:
                        bot.send_message(user_id, 'неправильное время')
                case 12:
                    if user_input is not None:
                        animals = db_actions.get_animal(user_input)
                        if len(animals) != 0:
                            temp_user_data.temp_data(user_id)[user_id][0] = 13
                            cart_visualize(user_id, animals, True)
                        else:
                            bot.send_message(user_id, 'Животное не найдено')
                    else:
                        bot.send_message(user_id, 'Неправильный ввод')
                case 14:
                    if user_input is not None:
                        temp_user_data.temp_data(user_id)[user_id][0] = None
                        db_actions.add_application(temp_user_data.temp_data(user_id)[user_id][6], temp_user_data.temp_data(user_id)[user_id][7], user_input)
                        bot.send_message(user_id, 'Заметка успешно добавлена')
                    else:
                        bot.send_message(user_id, 'Неправильный ввод')

    @bot.callback_query_handler(func=lambda call: True)
    def callback(call):
        buttons = Bot_inline_btns()
        user_id = call.message.chat.id
        if db_actions.user_is_existed(user_id):
            code = temp_user_data.temp_data(user_id)[user_id][0]
            if call.data == 'search':
                temp_user_data.temp_data(user_id)[user_id][0] = 7
                bot.send_message(call.message.chat.id, 'Введите кличку или номер животного')
            elif call.data == 'calendar':
                temp_user_data.temp_data(user_id)[user_id][0] = 9
                current_month = datetime.datetime.now().strftime("%B")
                bot.send_message(chat_id=user_id, text=f"Выберите месяц (Текущий месяц: {current_month}):",
                                 reply_markup=buttons.month_btns(temp_user_data.get_month()))
            elif call.data == 'zapis':
                temp_user_data.temp_data(user_id)[user_id][0] = 0
                bot.send_message(call.message.chat.id, 'Введите кличку животного')
            elif call.data[:6] == 'export':
                data = temp_user_data.temp_data(user_id)[user_id][3][int(call.data[6:])]  # [list->photos, str->text]
                pdf_creator.create_pdf(data)
                with open("plan.pdf", "rb") as misc:
                    obj = BytesIO(misc.read())
                    obj.name = 'plan.pdf'
                bot.send_document(user_id, obj)
                os.remove('plan.pdf')
            elif call.data[:6] == 'change':
                temp_user_data.temp_data(user_id)[user_id][0] = 8
                temp_user_data.temp_data(user_id)[user_id][2] = call.data[6:]
                bot.send_message(user_id, 'Отправьте фото в формате .jpg')
            elif call.data[:6] == 'select' and code == 13:
                temp_user_data.temp_data(user_id)[user_id][0] = 14
                temp_user_data.temp_data(user_id)[user_id][7] = call.data[6:]
                bot.send_message(user_id, 'введите описание к заметке')



    bot.polling(none_stop=True)


if '__main__' == __name__:
    os_type = platform.system()
    work_dir = os.path.dirname(os.path.realpath(__file__))
    config = ConfigParser(f'{work_dir}/{config_name}', os_type)
    temp_user_data = TempUserData()
    db = DB(config.get_config()['db_file_name'], Lock())
    db_actions = DbAct(db, config, config.get_config()['xlsx_path'])
    pdf_creator = PDFCreate()
    bot = telebot.TeleBot(config.get_config()['tg_api'])
    main()
