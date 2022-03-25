import json
import re
from quiz import bcrypt

def checkuser(username, password):
    with open('quiz/hash.txt') as f:
        data = f.read()

    if strong_password(password) and normal_username(username):
        if not data:
            new_user = {
                username: encrypt_password(password)
            }
            with open('quiz/hash.txt', 'w') as f:
                f.write(json.dumps(new_user))
                return True


        else:
            js = json.loads(data)
            if username not in js:
                js[username] = encrypt_password(password)
                with open('quiz/hash.txt', 'w') as f:
                    f.write(json.dumps(js))
                    return True
            else:
                if check_password_correction(js[username], password):
                    return True
                else:
                    return False


def normal_username(username):
    if re.fullmatch('^[a-zA-Z0-9_.-]+$', username):
        return True
    else:
        return False

def strong_password(password):
    if re.fullmatch(r'[A-Za-z0-9@#$%^&+=]{12,}', str(password)):
        return True
    else:
        return False

def encrypt_password(password):
    return bcrypt.generate_password_hash(password).decode('utf-8')

def check_password_correction(stored_password, attempted_password):
        return bcrypt.check_password_hash(stored_password, attempted_password)


