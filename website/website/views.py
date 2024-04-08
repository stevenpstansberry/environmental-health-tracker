from flask import Blueprint, Flask, jsonify, render_template
from bson import json_util
from website.mongo import db
import website.calc_data as calc_data

views = Blueprint('views', __name__, static_folder='static')

@views.route('/')
def home():

    data = list(db.test.find({}))
    print(data)
    # for result in data:
    #     print(result)

    return render_template('home.html', data = data)


@views.route('/data_table')
def table():
    data = list(db.test.find({}))  # Convert cursor to list
    print(data)
    for result in data:
        print(result)

    return render_template('data_table.html', data=data)


@views.route('/get_data', methods=['GET'])
def get_data():
    data = db.data.find()
    formatted_data = []
    for document in data:
        document['_id'] = str(document['_id'])  # Convert ObjectId to string
        formatted_data.append(document)
    
    return jsonify(formatted_data)


@views.route('/dashboard')
def dashboard():
    temp = 25.8
    press = 14.21
    hum = 40.8
    qlty = 64
    data = {"timestamp": "2024-04-05 01:07:54", "temp": temp, "press": press, "hum": hum, "qlty": qlty}
    data['dew_point_temp'] = calc_data.dew_point_calc(temp, hum)
    data['heat_index_temp'] = calc_data.calculate_heat_index(temp, hum)

    return render_template('index.html', title="Eco_Health_Tracker", data=data)


@views.route('/analysis')
def analysis():

    return render_template('analysis.html', title="Analysis")

@views.route('/sign_in')
def sign_in():

    return render_template('pages-sign-in.html', title="Sign_In")


@views.route('/sign_up')
def sign_up():

    return render_template('pages-sign-up.html', title="Sign_Up")