import pymongo
from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://Viewer:1234@sensordata.1v3p4ie.mongodb.net/?retryWrites=true&w=majority")
db = cluster["test"]  # space in cloud

collection = db["test"]  # table


#post = {"_id": 0, "temp": 70, "pressure": 2, "humidity" : 16}

#collection.insert_one(post)

#results = collection.find({})
