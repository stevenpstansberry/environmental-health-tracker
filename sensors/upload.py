from pymongo import MongoClient
import json
from pymongo.errors import ServerSelectionTimeoutError

def upload_json_to_mongo(json_file, uri):
    try:
        # Establish a connection to the MongoDB server
        client = MongoClient(uri, serverSelectionTimeoutMS=5000)  # Adjust timeout as needed

        # Select the database and collection
        db = client['EcoHealthTracking']
        collection = db['SensorData']

        # Read the JSON file
        with open(json_file, 'r') as file:
            data = json.load(file)

        # Upload the data to MongoDB
        for sensor_type, readings in data.items():
            for reading in readings:
                # Ensure each reading is a document and has a sensor type
                reading['sensor'] = sensor_type
                collection.insert_one(reading)

        print("Data uploaded successfully!")

    except ServerSelectionTimeoutError:
        print("Server selection timeout error: Unable to connect to the MongoDB server.")

    finally:
        # Close the connection
        client.close()

# Call the function to upload the data
upload_json_to_mongo('sensor_data.json', uri='mongodb+srv://maryiasakharava:SensorDataPassword@sensordata.pjdhs9k.mongodb.net/?retryWrites=true&w=majority&appName=SensorData')
