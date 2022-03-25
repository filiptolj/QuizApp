from flask import Blueprint, render_template, redirect, url_for, request, jsonify, make_response, session
from . import handleusers, my_jwt


auth = Blueprint("auth", __name__)


@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        if handleusers.strong_password(password):
            if handleusers.checkuser(username, password):
                resp = make_response(redirect(url_for('views.questions')))
                resp.set_cookie("JWT", my_jwt.jwtSign(username))
                session['username'] = username
                return resp
            else:
                return jsonify({"status" : 402, "message" : "Wrong password"})

        else:
            return jsonify({"status" : 401, "message" : "Invalid password"})
    return render_template("login.html")




