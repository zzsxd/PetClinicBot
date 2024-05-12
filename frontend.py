#####################################
#            Created by             #
#               zzsxd               #
#####################################
import telebot
from telebot import types
import datetime


#####################################



class Bot_inline_btns:
    def __init__(self):
        super(Bot_inline_btns, self).__init__()
        self.__markup = types.InlineKeyboardMarkup(row_width=1)

    def start_btns(self):
        calendar = types.InlineKeyboardButton('Календарь', callback_data='calendar')
        search =  types.InlineKeyboardButton('Поиск пациента', callback_data='search')
        zapis = types.InlineKeyboardButton('Новый пациент', callback_data='zapis')
        add = types.InlineKeyboardButton('Запись пациента', callback_data='calendar')
        self.__markup.add(calendar, search, zapis, add)
        return self.__markup


    def change_pidor_btns(self, id, gay):
        zapis = types.InlineKeyboardButton('Добавить анализы', callback_data=f'change{id}')
        export = types.InlineKeyboardButton('Экспорт в PDF', callback_data=f'export{gay}')
        self.__markup.add(zapis, export)
        return self.__markup

    def month_btns(self, monthes):
        markup = types.ReplyKeyboardMarkup(row_width=3)
        for month in monthes:
            btn_month = types.KeyboardButton(month)
            markup.add(btn_month)
        return markup

    def days_btns(self, days):
        markup = types.ReplyKeyboardMarkup(row_width=3)
        for day in range(days):
            btn_month = types.KeyboardButton(str(day+1))
            markup.add(btn_month)
        return markup

    def select_pidor_btns(self, pidor_id):
        zapis = types.InlineKeyboardButton('Выбрать животное', callback_data=f'select{pidor_id}')
        self.__markup.add(zapis)
        return self.__markup