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
    data = {"timestamp": latest_data['DHT']['timestamp'], 
            "temp": round(latest_data['DHT']['temperature'], 2), 
            "press": round(latest_data['BME']['pressure'], 2), 
            "hum": round(latest_data['DHT']['humidity'], 2), 
            "qlty": qlty}
    data['dew_point'] = calc_data.dew_point_calc(latest_data['DHT']['temperature'], latest_data['DHT']['humidity'])
    data['heat_index'] = calc_data.calculate_heat_index(latest_data['DHT']['temperature'], latest_data['DHT']['humidity'])

    return render_template('index.html', title="Eco_Health_Tracker", data=data)

@views.route('/analysis')
def analysis():
    # Sample data
    week_avg_data = {
        "2024-03-31": {
            'temperature' : [21.1, 18.2, 23.3, 16.4, 25.5, 20.6, 27.7], 
            'humidity' : [48.1, 40.2, 38.3, 42.4, 40.5, 45.6, 40.7], 
            'pressure' : [998.3, 1003.2, 1004.3, 1006.4, 999.5, 1009.6, 999.7], 
            'air_quality' : [12,10,9,8,13,10,11], 
            'dew_point': [10.72, 6.24, 10.96, 4.88, 13.60, 9.72, 15.84], 
            'heat_index' : [21.1, 18.2, 23.3, 16.4, 25.5, 20.6, 27.7]
        },
        "2024-04-07": {
        'temperature': [19.0, 21.5, 18.0, 23.0, 16.8, 25.3, 14.7], 
        'humidity': [30.2, 35.4, 28.8, 33.7, 36.2, 31.9, 37.0], 
        'pressure': [1015.5, 1013.4, 1016.1, 1014.5, 1012.7, 1017.2, 1013.1], 
        'air_quality': [11,10,13,14,10,12,9], 
        'dew_point': [10.1, 11.6, 9.7, 12.5, 8.9, 13.3, 7.8], 
        'heat_index': [18.5, 21.0, 17.6, 22.4, 16.0, 24.9, 14.1]
    },
    "2024-04-14": {
        'temperature': [20.5, 22.8, 19.9, 25.1, 17.4, 27.3, 15.5],
        'humidity': [32.1, 34.3, 31.7, 33.2, 30.4, 29.6, 35.5],
        'pressure': [1014.5, 1011.3, 1015.6, 1012.1, 1018.4, 1010.6, 1016.7],
        'air_quality': [10,14,13,15,10,8,9],
        'dew_point': [11.0, 12.2, 10.5, 13.7, 9.3, 14.4, 8.2],
        'heat_index': [19.8, 22.1, 19.3, 24.5, 17.2, 26.8, 14.8]
    }
    }
    
    week_high_data = {
        "2024-03-31": {
            'temperature': [23.2, 24.1, 25.0, 26.3, 27.4, 28.6, 29.7],
            'humidity': [32.1, 33.2, 34.3, 35.4, 36.5, 37.6, 38.7],
            'pressure': [1018.2, 1020.1, 1019.3, 1021.5, 1022.7, 1023.8, 1024.9],
            'air_quality': [14, 12, 13, 15, 11, 10, 9]
        },
        "2024-04-07": {
            'temperature': [23.3, 24.5, 25.6, 26.7, 27.8, 28.9, 30.0],
            'humidity': [32.0, 33.5, 34.0, 35.5, 36.0, 37.5, 38.0],
            'pressure': [1020.3, 1018.4, 1017.6, 1016.8, 1015.9, 1014.7, 1013.8],
            'air_quality': [12, 9, 7, 8, 10, 13, 12]
        },
        "2024-04-14": {
            'temperature': [24.1, 25.2, 26.3, 27.4, 28.5, 29.6, 30.7],
            'humidity': [31.7, 32.8, 33.9, 35.0, 36.1, 37.2, 38.3],
            'pressure': [1019.2, 1021.4, 1022.6, 1023.8, 1024.7, 1025.9, 1026.5],
            'air_quality': [14, 13, 12, 11, 10, 9, 8]
        }
    }

    week_low_data = {
        "2024-03-31": {
            'temperature': [20.2, 21.3, 22.4, 23.5, 24.6, 25.7, 26.8],
            'humidity': [30.1, 31.2, 32.3, 33.4, 34.5, 35.6, 36.7],
            'pressure': [1012.3, 1013.5, 1014.6, 1015.8, 1016.9, 1017.4, 1018.6],
            'air_quality': [15, 14, 13, 12, 11, 10, 9]
        },
        "2024-04-07": {
            'temperature': [20.5, 21.6, 22.7, 23.8, 24.9, 26.0, 27.1],
            'humidity': [30.0, 31.0, 32.0, 33.0, 34.0, 35.0, 36.0],
            'pressure': [1011.1, 1012.2, 1013.3, 1014.4, 1015.5, 1016.6, 1017.7],
            'air_quality': [8, 7, 6, 5, 4, 3, 2]
        },
        "2024-04-14": {
            'temperature': [21.1, 22.2, 23.3, 24.4, 25.5, 26.6, 27.7],
            'humidity': [29.9, 31.1, 32.2, 33.3, 34.4, 35.5, 36.6],
            'pressure': [1010.9, 1011.7, 1012.8, 1013.9, 1014.8, 1015.6, 1016.4],
            'air_quality': [15, 14, 13, 12, 11, 10, 9]
        }
}
    
    return render_template('analysis.html', title="Analysis", week_avg_data=week_avg_data, week_high_data=week_high_data, week_low_data=week_low_data )


@views.route('/sign_in')
def sign_in():

    return render_template('pages-sign-in.html', title="Sign_In")


@views.route('/sign_up')
def sign_up():

    return render_template('pages-sign-up.html', title="Sign_Up")
