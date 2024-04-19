from flask import Blueprint, Flask, jsonify, render_template
from bson import json_util
import math
import website.mongo as mongo
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


@views.route('/api/data')
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
    data = {}

    qlty = 64
    latest_data = mongo.get_latest_data()
    data = {"timestamp": latest_data['last_DHT']['timestamp'], 
            "temp": round(latest_data['last_DHT']['temperature'], 2), 
            "press": round(latest_data['last_BME']['pressure'], 2), 
            "hum": round(latest_data['last_DHT']['humidity'], 2), 
            "qlty": qlty}
    data['dew_point'] = calc_data.dew_point_calc(latest_data['last_DHT']['temperature'], latest_data['last_DHT']['humidity'])
    data['heat_index'] = calc_data.calculate_heat_index(latest_data['last_DHT']['temperature'], latest_data['last_DHT']['humidity'])

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