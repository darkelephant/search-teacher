import os
import json
import random
from flask import Flask, render_template, request

def load_json(file_name):
    with open(file_name, 'r', encoding='utf8') as f:
        contents = f.read()
    return json.loads(contents)

def save_json(file_name, data_json):
    with open(file_name, "w", encoding='utf8') as write_file:
        json.dump(data_json, write_file)

list_goals = load_json('goals.json')
teachers = load_json('teachers.json')

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    all_teachers = [x for x in teachers]
    random.seed()
    random.shuffle(all_teachers)
    return render_template("index.html", profiles = teachers, six_teachers = all_teachers[:6],  goals = list_goals)

@app.route('/goals/<goal>')
def goals(goal):
    list_id_teachers = []
    for key_teach, profile_teach in sorted(teachers.items(), key=lambda x: x[1]['rating'], reverse=True):
        if goal in profile_teach['goals']:
            list_id_teachers.append(key_teach)
    print(list_id_teachers)
    return render_template("goal.html", profiles = teachers, teachers = list_id_teachers, goal = list_goals[goal])

@app.route('/profiles/<id_teach>')
def profile(id_teach):
    print(id_teach)
    try:
        if int(id_teach) > 0:
            return render_template("profile.html", profile = teachers[id_teach], goals = list_goals, id = id_teach)
        else:
            return render_template("profiles.html", profiles = teachers)
    except:
        return '<p>Ошибка значения идентификатора</p>'

@app.route('/search', methods=['GET'])
def search():
    search_query = request.args.get('s','').strip()
    return render_template("search.html", search_query = search_query)
    
@app.route('/request')
def selection():
    return render_template("pick.html", goals = list_goals)
    
@app.route('/send_request', methods=['POST'])
def send_selection():
    json_file_name = 'request.json'
    goal = request.form.get('goal') 
    time = request.form.get('time')
    fio = request.form.get('fio')
    phone = request.form.get('phone')
    if os.path.isfile(json_file_name):
        request_json = load_json(json_file_name)
        last_id_request = max([int(x) for x in request_json])
        request_json[last_id_request + 1] = {'goal':goal, 'time':time, 'fio':fio, 'phone':phone}
        save_json(json_file_name, request_json)
    else:
        request_json = {'0':{'goal':goal, 'time':time, 'fio':fio, 'phone':phone}}
        save_json(json_file_name, request_json)
    return render_template("sent_pick.html", fio = fio, phone = phone)

@app.route('/booking/<id_teach>', methods=['GET'])
def booking(id_teach):
    time_booking = request.args['time']
    day_booking = request.args['day']
    return render_template("booking.html", time_booking = time_booking, day_booking = day_booking, id_teach = id_teach, profile = teachers[id_teach])

@app.route('/sending_booking', methods=['POST'])
def sending_booking():
    json_file_name = 'booking.json'
    information_booking = {
        'day_booking':request.form.get('day_booking'),
        'time_booking':request.form.get('time_booking'),
        'id_teach':request.form.get('id_teach'),
        'fio_user':request.form.get('fio'),
        'phone_user':request.form.get('phone'),
    }
    if os.path.isfile(json_file_name):
        request_json = load_json(json_file_name)
        last_id_request = max([int(x) for x in request_json])
        request_json[last_id_request + 1] = information_booking
        save_json(json_file_name, request_json)
    else:
        request_json = {'0':information_booking}
        save_json(json_file_name, request_json)
    return render_template("sent.html", information_booking = information_booking)

@app.route('/message', methods=['GET'])
def message():
    id_teach = request.args['id']
    return render_template("message.html", profile = teachers[id_teach], id = id_teach)

@app.route('/send_message', methods=['POST'])
def send_message():
    id_teach = request.form.get('id_teach')
    fio = request.form.get('fio')
    phone = request.form.get('phone')
    text_message = request.form.get('text_message')
    return render_template("sent_message.html", profile = teachers[id_teach], fio = fio, phone = phone, text_message = text_message)

if __name__ == "__main__":
    app.debug = True
    app.run('localhost', 8000)
