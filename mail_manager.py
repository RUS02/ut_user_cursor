import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import os
from config import CONFIG

class MailManager:
    def send_welcome_email(self, to_email, login, password):
        try:
            msg = MIMEMultipart()
            msg['From'] = CONFIG['smtp']['sender']
            msg['To'] = to_email
            msg['Subject'] = "Добро пожаловать!"
            
            body = f"""
            Здравствуйте!
            
            Ваша учетная запись создана.
            Логин: {login}
            Пароль: {password}
            
            С уважением,
            Администрация
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Прикрепляем картинки
            pics_folder = CONFIG['pics_folder']
            for filename in os.listdir(pics_folder):
                if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                    with open(os.path.join(pics_folder, filename), 'rb') as f:
                        img = MIMEImage(f.read())
                        img.add_header('Content-Disposition', 'attachment', filename=filename)
                        msg.attach(img)
            
            server = smtplib.SMTP(CONFIG['smtp']['server'], CONFIG['smtp']['port'])
            server.starttls()
            server.login(CONFIG['smtp']['sender'], CONFIG['smtp']['password'])
            server.send_message(msg)
            server.quit()
            
            return True, f"Письмо успешно отправлено на {to_email}"
        except Exception as e:
            return False, f"Ошибка отправки письма: {str(e)}" 