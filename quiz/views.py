from flask import Blueprint, redirect, url_for, jsonify, request
from . import my_jwt
from . import handle_question

views = Blueprint("views", __name__)

@views.route("/")
def home():
    return redirect(url_for('auth.login'))

@views.route("/quiz/question", methods=['GET', 'POST', 'DELETE'])
def questions():
    tokenStatus = my_jwt.jwtVerify(request.cookies)

    if(tokenStatus == "ValidToken"):
        if request.method == 'POST':
            try:
                content_type = request.headers.get('Content-Type')
                if (content_type == 'application/json'):
                    question = request.json
                    check = handle_question.check_question(question)
                    if(check == False):
                        return jsonify({"status": 401, "message": "Invalid JSON format"})

                    return "<h1>questions page</h1>"
                else:
                    return jsonify({"status": 401, "message": "Invalid JSON format"})
            except:
                return jsonify({"status" : 401, "message" : "Invalid JSON format"})


        elif request.method == 'GET':
            return jsonify(handle_question.get_questions())



    elif(tokenStatus == "TokenExpired"):
        return jsonify({"status" : 402, "message" : "Login session expired. Please log in again."})
    else:
        if request.method == 'POST' or request.method == 'DELETE':
            return jsonify({"status" : 402, "message" : "You need to be logged in to perform this action. Please log in."})
        else:
            return redirect(url_for('auth.login'))

@views.route("/quiz/question/<id>", methods=['DELETE'])
def delete_question(id):
    tokenStatus = my_jwt.jwtVerify(request.cookies)

    if (tokenStatus == "ValidToken"):
        if request.method == 'DELETE':
            if int(id) <= 0:
                return jsonify({"status": 401, "message": "Invalid question index"})
            else:
                check = handle_question.delete_question(id)
                if (check == False):
                    return jsonify({"status": 401, "message": "Invalid question index"})


        return '<h1>DELETE PAGE</h1>'

    elif (tokenStatus == "TokenExpired"):
        return jsonify({"status": 402, "message": "Login session expired. Please log in again."})

    else:
        return jsonify({"status": 402, "message": "You need to be logged in to perform this action. Please log in."})
