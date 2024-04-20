#####################################
#            Created by             #
#               zzsxd               #
#               SBR                 #
#####################################
config_name = 'secrets.json'
MONTHS = [
    "Январь",
    "Февраль",
    "Март",
    "Апрель",
    "Май",
    "Июнь",
    "Июль",
    "Август",
    "Сентябрь",
    "Октябрь",
    "Ноябрь",
    "Декабрь"
]

#####################################

import os
import telebot
import platform
import json
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


def cart_visualize(data, s=''):
    fields = {0: 'Кличка', 1: 'Номер телефона', 2: 'Жалобы', 3: 'Рентген', 4: 'Узи', 5: 'Диагноз', 6: 'Операции'}
    # На индексе 7 в этом цикле появляется массив с фотограиями в виде байт строки, я не знаю как их отправить в
    # сообщении (их много)
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
                            for pidor in animals:
                                bot.send_message(user_id, f'Карта больного:\n\n{cart_visualize(pidor[1:])}',
                                                 parse_mode='html', reply_markup=buttons.change_pidor_btns(pidor[0]))
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

    @bot.callback_query_handler(func=lambda call: True)
    def callback(call):
        buttons = Bot_inline_btns()
        user_id = call.message.chat.id
        if db_actions.user_is_existed(user_id):
            if call.data == 'search':
                temp_user_data.temp_data(user_id)[user_id][0] = 7
                bot.send_message(call.message.chat.id, 'Введите кличку или номер животного')

            elif call.data == 'calendar':
                show_month_selection(call.message.chat.id)
            elif call.data == 'zapis':
                temp_user_data.temp_data(user_id)[user_id][0] = 0
                bot.send_message(call.message.chat.id, 'Введите кличку животного')
            elif call.data == 'export':
                pdf_creator.create_pdf()
                with open("plan.pdf", "rb") as misc:
                    obj = BytesIO(misc.read())
                    obj.name = 'plan.pdf'
                bot.send_document(user_id, obj)
                os.remove('plan.pdf')
            elif call.data[:6] == 'change':
                temp_user_data.temp_data(user_id)[user_id][0] = 8
                temp_user_data.temp_data(user_id)[user_id][2] = call.data[6:]
                bot.send_message(user_id, 'Отправьте фото в формате .jpg')

    def show_month_selection(message):
        markup = types.ReplyKeyboardMarkup(row_width=3)
        for month in MONTHS:
            btn_month = types.KeyboardButton(month)
            markup.add(btn_month)

        current_month = datetime.datetime.now().strftime("%B")
        bot.send_message(chat_id=message.chat.id, text=f"Выберите месяц (Текущий месяц: {current_month}):",
                         reply_markup=markup)

    @bot.message_handler(func=lambda message: message.text in MONTHS)
    def handle_month_choice(message):
        global month
        month = message.text
        current_year = datetime.datetime.now().year
        days_in_month = calendar.monthrange(current_year, MONTHS.index(month) + 1)[1]
        show_date_selection(message, month, current_year, days_in_month)

    def show_date_selection(message, month, year, days_in_month):
        markup = types.ReplyKeyboardMarkup(row_width=7)
        for day in range(1, days_in_month + 1):
            btn_day = types.KeyboardButton(str(day))
            markup.add(btn_day)

        bot.send_message(message.chat.id, f"Выберите день в {month}, {year}:", reply_markup=markup)

    @bot.message_handler(func=lambda message: True)
    def handle_date_choice(message):
        day = message.text
        selected_date = f"Вы выбрали {day}, {month}, {datetime.datetime.now().year}"
        bot.send_message(message.chat.id, selected_date)

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
