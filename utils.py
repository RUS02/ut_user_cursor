import random
import string

def generate_login(email):
    local_part = email.split('@')[0]
    domain = email.split('@')[1].split('.')[0]
    
    if domain.upper() == 'BNIPI':
        return local_part
    else:
        return f"{domain}_{local_part}"

def generate_password():
    chars = string.ascii_letters + string.digits + '#'
    password = ['#']  # Гарантируем наличие символа #
    password.extend(random.choice(string.ascii_uppercase) for _ in range(2))
    password.extend(random.choice(string.ascii_lowercase) for _ in range(2))
    password.extend(random.choice(string.digits) for _ in range(2))
    password.extend(random.choice(chars) for _ in range(1))
    
    random.shuffle(password)
    return ''.join(password) 