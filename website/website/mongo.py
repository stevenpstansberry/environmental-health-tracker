import pymongo
import json
from pymongo import MongoClient
import os


cluster = MongoClient("mongodb+srv://Viewer:1234@sensordata.1v3p4ie.mongodb.net/?retryWrites=true&w=majority")
db = cluster["test"]  # space in cloud
collection = db["data"]  # table


cursor = collection.find({})

# Print the data
# print(list(cursor))

# for document in cursor:
#     print(document)



# Close the MongoDB connection
# cluster.close()

