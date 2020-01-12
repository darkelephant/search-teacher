import json
import random
from flask import Flask, render_template, request

app = Flask(__name__)

def load_json(file_name):
    with open(file_name, 'r', encoding='utf8') as f:
        contents = f.read()
    return json.loads(contents)

list_goals = load_json('goals.json')
teachers = load_json('teachers.json')

@app.route('/')
@app.route('/index')
def index():
    all_teachers = [x for x in teachers]
    random.seed()
    random.shuffle(all_teachers)
    page = render_template("index.html", profiles = teachers, six_teachers = all_teachers[:6],  goals = list_goals)
    return page

@app.route('/goals/<goal>')
def goals(goal):
    list_id_teachers = []
    for key_teach, profile_teach in sorted(teachers.items(), key=lambda x: x[1]['rating'], reverse=True):
        if goal in profile_teach['goals']:
            list_id_teachers.append(key_teach)
    print(list_id_teachers)
    page = render_template("goal.html", profiles = teachers, teachers = list_id_teachers, goal = list_goals[goal])
    return page

@app.route('/profiles/<id_teach>')
def profile(id_teach):
    print(id_teach)
    try:
        if int(id_teach) > 0:
            page = render_template("profile.html", profile = teachers[id_teach], goals = list_goals, id = id_teach)
            return page
        else:
            page = render_template("profiles.html", profiles = teachers)
            return page
    except:
        return '<p>ОШИБКА</p>'

@app.route('/search', methods=['GET'])
def search():
    pass
    
@app.route('/request')
def selection():
    pass    
    
@app.route('/booking/<id_teach>', methods=['GET'])
def booking(id_teach):
    return id_teach

@app.route('/message', methods=['GET'])
def message():
    id = request.args['id']
    page = render_template("message.html", profile = teachers[id], id = id)
    return page

@app.route('/send_message', methods=['POST'])
def send_message():
    id = request.form.get('id_teach')
    fio = request.form.get('fio')
    phone = request.form.get('phone')
    text_message = request.form.get('text_message')
    page = render_template("sent_message.html", profile = teachers[id], fio = fio, phone = phone, text_message = text_message)
    return page

    
if __name__ == "__main__":
    app.debug = True
    app.run('localhost', 8000)
    