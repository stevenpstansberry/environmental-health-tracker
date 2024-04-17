from pymongo import MongoClient
import json


# this should take in json file as sensor_data.json
def upload_json_to_mongo(json_file, uri='your_mongodb_uri'):
    # Establish a connection to the MongoDB server
    client = MongoClient(uri)

    # Select the database and collection
    db = client['your_database']
    collection = db['your_collection']

    # Read the JSON file
    with open(json_file, 'r') as file:
        data = json.load(file)

    # Upload the data to MongoDB
    for sensor_type, readings in data.items():
        for reading in readings:
            # Ensure each reading is a document and has a sensor type
            reading['sensor'] = sensor_type
            collection.insert_one(reading)

    # Close the connection
    client.close()

# Call the function to upload the data
upload_json_to_mongo('sensor_data.json', uri='your_mongodb_uri')
