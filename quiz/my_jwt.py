import jwt, time, random, string, json
from flask import session

JWT_ISS = "FTOKEN"
JWT_ALGO = "HS256"


def generatePrivateKey(username):
    private_key = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(32))
    print(private_key)
    storePrivateKey(username, private_key)
    return private_key


def storePrivateKey(username, key):
    with open('quiz/key.txt') as f:
      data = f.read()
    if not data:
      new_user = {
        username: key
      }
      with open('quiz/key.txt', 'w') as f:
        f.write(json.dumps(new_user))
    else:
      js = json.loads(data)
      js[username] = key
      with open('quiz/key.txt', 'w') as f:
        f.write(json.dumps(js))

def getPrivateKey(username):
    with open('quiz/key.txt') as f:
      data = f.read()
    js = json.loads(data)
    return js[username]



def jwtSign(username):
    generatePrivateKey(username)
    JWT_KEY = getPrivateKey(username)
    print(JWT_KEY)
    rnd_ID = "".join(random.choice("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz~!@#$%^_-") for i in range(24))
    now = int(time.time())
    return jwt.encode({
      "iat" : now,
      "nbf" : now,
      "exp" : now + 600,
      "jti" : rnd_ID,
      "iss" : JWT_ISS,
      "data" : { "username" : username }
    }, JWT_KEY, algorithm=JWT_ALGO)


def jwtVerify(cookies):
    try:
        username = session['username']
        token = cookies.get("JWT")
        key = getPrivateKey(username)
        decoded = jwt.decode(token, key, algorithms=[JWT_ALGO])
        return "ValidToken"
    except jwt.ExpiredSignatureError:
        return "TokenExpired"
    except:
        return False
