from flask import Flask
from flask_bcrypt import Bcrypt
from os.path import exists


if not (exists('quiz/questions.json')):
    f = open("quiz/questions.json", "w")
    f.close()
if not (exists('quiz/hash.txt')):
    f = open("quiz/hash.txt", "w")
    f.close()
if not (exists('quiz/key.txt')):
    f = open("quiz/key.txt", "w")
    f.close()


app = Flask(__name__)
app.config['SECRET_KEY'] = "secret8989"
app.config['JSON_SORT_KEYS'] = False
bcrypt = Bcrypt(app)
from .views import views
from .auth import auth

app.register_blueprint(views, url_prefix="/")
app.register_blueprint(auth, url_prefix="/")

