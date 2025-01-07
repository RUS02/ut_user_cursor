import tkinter as tk
from tkinter import ttk, scrolledtext
from database import DatabaseManager
from mail_manager import MailManager
from utils import generate_login, generate_password
import sys
import traceback

class Application(tk.Tk):
    def __init__(self):
        try:
            super().__init__()
            print("Инициализация приложения...")
            
            self.title("Создание пользователей")
            self.geometry("800x600")
            
            self.db = DatabaseManager()
            self.mail = MailManager()
            
            self.create_widgets()
            print("Приложение успешно инициализировано")
        except Exception as e:
            print(f"Ошибка при инициализации приложения: {str(e)}")
            print("Полный стек ошибки:")
            traceback.print_exc()
            sys.exit(1)
        
        self.create_widgets()
        
    def create_widgets(self):
        # Фрейм для подключения к БД
        db_frame = ttk.LabelFrame(self, text="Подключение к базе данных", padding=10)
        db_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(db_frame, text="Логин:").grid(row=0, column=0, padx=5)
        self.db_login = ttk.Entry(db_frame)
        self.db_login.grid(row=0, column=1, padx=5)
        
        ttk.Label(db_frame, text="Пароль:").grid(row=0, column=2, padx=5)
        self.db_password = ttk.Entry(db_frame, show="*")
        self.db_password.grid(row=0, column=3, padx=5)
        
        ttk.Button(db_frame, text="Подключиться", command=self.connect_to_db).grid(row=0, column=4, padx=5)
        
        # Фрейм для создания пользователей
        user_frame = ttk.LabelFrame(self, text="Создание пользователей", padding=10)
        user_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(user_frame, text="Email адреса:").pack(anchor='w')
        self.email_text = scrolledtext.ScrolledText(user_frame, height=5)
        self.email_text.pack(fill='x')
        
        ttk.Button(user_frame, text="Создать пользователей", command=self.create_users).pack(pady=5)
        
        # Лог
        log_frame = ttk.LabelFrame(self, text="Лог операций", padding=10)
        log_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.log_text = scrolledtext.ScrolledText(log_frame)
        self.log_text.pack(fill='both', expand=True)
        
    def log(self, message):
        self.log_text.insert('end', message + '\n')
        self.log_text.see('end')
        
    def connect_to_db(self):
        success, message = self.db.connect(self.db_login.get(), self.db_password.get())
        self.log(message)
        
    def create_users(self):
        emails = self.email_text.get('1.0', 'end-1c').split('\n')
        emails = [email.strip() for email in emails if email.strip()]
        
        for email in emails:
            login = generate_login(email)
            password = generate_password()
            
            success, message = self.db.create_user(login, password)
            self.log(message)
            
            if success:
                success, message = self.mail.send_welcome_email(email, login, password)
                self.log(message)

if __name__ == "__main__":
    print("Запуск приложения...")
    try:
        app = Application()
        print("Запуск главного цикла...")
        app.mainloop()
    except Exception as e:
        print(f"Критическая ошибка: {str(e)}")
        traceback.print_exc() 