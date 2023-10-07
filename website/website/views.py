from flask import Blueprint, render_template

from website.mongo import db

views = Blueprint('views', __name__)

@views.route('/')
def home():

    data = db.test.find({})
    for result in data:
        print(result)

    return render_template('home.html', data = data)
