#####################################
#            Created by             #
#               zzsxd               #
#               SBR                 #
#####################################

import os
import time
import json
import csv


#####################################


class TempUserData:
    def __init__(self):
        super(TempUserData, self).__init__()
        self.__user_data = {}

    def temp_data(self, user_id):
        if user_id not in self.__user_data.keys():
            self.__user_data.update({user_id: [None, [None, None, None, None, None, None, None], None]})
        return self.__user_data


class DbAct:
    def __init__(self, db, config, path_xlsx):
        super(DbAct, self).__init__()
        self.__db = db
        self.__config = config
        self.__fields = ['Имя', 'Фамилия', 'Никнейм', 'Номер телефона']
        self.__dump_path_xlsx = path_xlsx

    def add_user(self, user_id, first_name, last_name, nick_name):
        if not self.user_is_existed(user_id):
            if user_id in self.__config.get_config()['admins']:
                is_admin = True
            else:
                is_admin = False
            self.__db.db_write(
                'INSERT INTO users (user_id, first_name, last_name, nick_name, is_admin) VALUES (?, ?, ?, ?, ?)',
                (user_id, first_name, last_name, nick_name, is_admin))

    def user_is_existed(self, user_id):
        data = self.__db.db_read('SELECT count(*) FROM users WHERE user_id = ?', (user_id,))
        if len(data) > 0:
            if data[0][0] > 0:
                status = True
            else:
                status = False
            print(status)
            return status

    def user_is_admin(self, user_id):
        data = self.__db.db_read('SELECT is_admin FROM users WHERE user_id = ?', (user_id,))
        if len(data) > 0:
            if data[0][0] == 1:
                status = True
            else:
                status = False
            return status

    def add_your_mom(self, data):
        data.append(json.dumps([]))
        self.__db.db_write(
            f'INSERT INTO pidors (nickname, phone_number, complaint, xray, uzi, diagnosis, operation, photos) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
            data)

    def get_animal(self, data):
        return self.__db.db_read(f'SELECT row_id, nickname, phone_number, complaint, xray, uzi, diagnosis, operation, photos FROM pidors WHERE nickname = "{data}" OR phone_number = "{data}"', ())

    def add_photo_to_pidor(self, pidor_id, new_dick):
        data = self.__db.db_read('SELECT photos FROM pidors WHERE row_id = ?', (pidor_id, ))[0][0]
        photos = json.loads(data)
        photos.append(new_dick)
        photos = json.dumps(photos)
        self.__db.db_write('UPDATE pidors SET photos = ? WHERE row_id = ?', (photos, pidor_id))
