from pymongo import MongoClient
import json
from datetime import datetime, timedelta
import random
import os


# Connect to MongoDB cluster
cluster = MongoClient("mongodb+srv://maryiasakharava:SensorDataPassword@sensordata.pjdhs9k.mongodb.net/?retryWrites=true&w=majority&appName=SensorData")
db = cluster["sensor_data"]
collection = db["test_data"]

# cursor = collection.find({})

# # Print the data
# print(list(cursor))

# for document in cursor:
#     print(document)

# # Function to generate random data for a specific timestamp
# def generate_sensor_data(timestamp):
#     return {
#         "@timestamp": timestamp.strftime("%Y-%m-%dT%H:%M:%SZ"),
#         "sensors": {
#             "humidity": random.uniform(20.0, 80.0),
#             "temperature": random.uniform(10.0, 30.0),
#             "pressure": random.uniform(900.0, 1100.0),
#             "quality": random.uniform(0.0, 100.0)
#         }
#     }

# # Number of data points to generate
# num_data_points = 20

# # Starting timestamp
# start_timestamp = datetime.now()

# # List to store generated data
# generated_data = []

# # Generate 20 data points
# for i in range(num_data_points):
#     current_timestamp = start_timestamp + timedelta(minutes=i)
#     data_point = generate_sensor_data(current_timestamp)
#     generated_data.append(data_point)


# # Insert the generated data into the collection
# collection.insert_many(generated_data)

# # Convert the list of dictionaries to JSON format
# json_data = json.dumps(generated_data, indent=2)

# # Print or save the generated data
# print(json_data)


#################
# # Store json file
# current_directory = os.getcwd()

# # Specify the filename
# json_filename = 'sample_sensor_data_2.json'

# # Create the full path to the JSON file
# json_file_path = os.path.join(current_directory, json_filename)

# # Open the JSON file
# with open(json_file_path, 'r') as file:
#     json_data = json.load(file)

# collection.insert_one(json_data)



# Close the MongoDB connection
# cluster.close()