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
        zapis = types.InlineKeyboardButton('Запись пациента', callback_data='zapis')
        self.__markup.add(calendar, search, zapis)
        return self.__markup

    def calendar_day(self):
        for day in range(1, 32):
            button = types.InlineKeyboardButton(text=str(day), callback_data=f'day_{day}')
            self.__markup.add(button)
            return self.__markup

    def calendar_month(self):
        for month in range(1, 13):
            button = types.InlineKeyboardButton(text=datetime.date(current_date.year, month, 1).strftime("%B"),
                                                callback_data=f'month_{month}')
            self.__markup.add(button)



