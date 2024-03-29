from flask import Blueprint, Flask, jsonify, render_template
from bson import json_util
from website.mongo import db

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
    sensor_data = {"temp": 25.8, "press": 14.21, "hum": 40.8, "qlty": 64}

    return render_template('index.html', title="Eco_Health_Tracker", sensor_data=sensor_data)


@views.route('/sign_in')
def sign_in():

    return render_template('pages-sign-in.html', title="Sign_In")


@views.route('/sign_up')
def sign_up():

    return render_template('pages-sign-up.html', title="Sign_Up")