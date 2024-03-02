from flask import Blueprint, Flask, jsonify, render_template

from website.mongo import db

views = Blueprint('views', __name__, static_folder='static')
# views = Flask('views', __name__,  static_folder='static/')

@views.route('/')
def home():

    data = list(db.test.find({}))
    for result in data:
        print(result)

    return render_template('home.html', data = data)


@views.route('data_table/')
def table():
    # sensor_data = {}
    data = list(db.test.find({}))  # Convert cursor to list
    print(data)
    for result in data:
        print(result)

    return render_template('data_table.html', data=data)

@views.route('dashboard/')
def dashboard():

    return render_template('index.html', title="Eco_Health_Tracker")