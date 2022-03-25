import json

def check_question(data):
    if len(data) == 3:
        if all(key in data for key in ('question', 'answers', 'correctAnswer')):

            if (type(data['question']) == str):
                if(type(data['answers']) == list and len(data['answers']) >= 2 and check_list_type(data['answers'])):
                    if(type(data['correctAnswer']) == type(data['answers'][0]) and data['correctAnswer'] in data['answers']):
                        add_question(data)
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False
    else:
        return False


def check_list_type(mylist):
    list_type = str
    if all(isinstance(x, list_type) for x in mylist):
        return True
    else:
        return False

def get_questions():
    with open('quiz/questions.json', 'r') as f:
        data = f.read()
        if not data:
            return []
        else:
            with open('quiz/questions.json', 'r') as f:
                questions = json.load(f)
                return questions

def add_question(data):
    questions_list = []
    questions = get_questions()
    for q in questions:
        questions_list.append(q)

    if data not in questions_list:
        questions_list.append(data)

    with open("quiz/questions.json", "w") as f:
        json.dump(questions_list, f)


def delete_question(id):
    questions_list = get_questions()
    try:
        questions_list.pop(int(id)-1)
        with open("quiz/questions.json", "w") as f:
            json.dump(questions_list, f)
    except:
        return False





