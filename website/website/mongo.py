import pymongo
import json
from pymongo import MongoClient
import os


cluster = MongoClient("mongodb+srv://Viewer:1234@sensordata.1v3p4ie.mongodb.net/?retryWrites=true&w=majority")
# cluster = MongoClient("mongodb+srv://tonyhan:tonyhan@sensordata.1v3p4ie.mongodb.net/?retryWrites=true&w=majority")
db = cluster["test"]  # space in cloud

collection = db["data"]  # table

current_directory = os.getcwd()
print(current_directory)

# Specify the filename
json_filename = 'data.json'

# Create the full path to the JSON file
json_file_path = os.path.join(current_directory, json_filename)

# Open the JSON file
# with open(json_file_path, 'r') as file:
#     json_data = json.load(file)

# print(json_data)
# collection.insert_one(json_data)

# print(result)
# cursor = collection.find({})


# Print the data
# print(cursor)
# for document in cursor:
#     print(document)

# Close the MongoDB connection
# cluster.close()

#post = {"_id": 0, "temp": 70, "pressure": 2, "humidity" : 16}

#collection.insert_one(post)

#results = collection.find({})
