import cx_Oracle
import logging
from config import CONFIG

class DatabaseManager:
    def __init__(self):
        self.connection = None
        
    def connect(self, username, password):
        try:
            dsn = cx_Oracle.makedsn(
                CONFIG['db']['host'],
                CONFIG['db']['port'],
                service_name=CONFIG['db']['service_name']
            )
            self.connection = cx_Oracle.connect(
                username,
                password,
                dsn,
                encoding=CONFIG['db']['encoding']
            )
            return True, "Подключение успешно установлено"
        except Exception as e:
            return False, f"Ошибка подключения к БД: {str(e)}"
            
    def create_user(self, login, password):
        try:
            if not self.connection:
                return False, "Нет подключения к базе данных"
                
            cursor = self.connection.cursor()
            cursor.callproc('rnkin.ut_user.create_user', [login, password])
            self.connection.commit()
            return True, f"Пользователь {login} успешно создан"
        except Exception as e:
            return False, f"Ошибка создания пользователя: {str(e)}" 