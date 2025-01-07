from flask import Flask, render_template, request, jsonify
from database import DatabaseManager
from mail_manager import MailManager
from utils import generate_login, generate_password
import traceback

app = Flask(__name__)
db = DatabaseManager()
mail = MailManager()

@app.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        print(f"Ошибка при рендеринге страницы: {str(e)}")
        traceback.print_exc()
        return str(e), 500

@app.route('/connect', methods=['POST'])
def connect():
    data = request.json
    success, message = db.connect(data['login'], data['password'])
    return jsonify({'success': success, 'message': message})

@app.route('/create_users', methods=['POST'])
def create_users():
    data = request.json
    emails = data['emails'].split('\n')
    emails = [email.strip() for email in emails if email.strip()]
    
    results = []
    for email in emails:
        login = generate_login(email)
        password = generate_password()
        
        success, message = db.create_user(login, password)
        results.append(message)
        
        if success:
            success, message = mail.send_welcome_email(email, login, password)
            results.append(message)
            
    return jsonify({'messages': results})

if __name__ == '__main__':
    print("Запуск веб-сервера...")
    try:
        app.run(debug=True, port=5000)
    except Exception as e:
        print(f"Ошибка запуска сервера: {str(e)}")
        traceback.print_exc() 