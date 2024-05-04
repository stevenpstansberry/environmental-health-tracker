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
                # Check if the document already exists in the collection
                existing_doc = collection.find_one({"sensor": sensor_type, "timestamp": reading["timestamp"]})

                if existing_doc is None:
                    # Document doesn't exist, insert it into the collection
                    reading['sensor'] = sensor_type
                    collection.insert_one(reading)
                    print("Inserted document:", reading)
                else:
                    # Document already exists, skip insertion
                    print("Document already exists, skipping insertion:", reading)

        print("Data uploaded successfully!")

    except ServerSelectionTimeoutError:
        print("Server selection timeout error: Unable to connect to the MongoDB server.")

    finally:
        # Close the connection
        client.close()

# Call the function to upload the data
upload_json_to_mongo('sample_sensor_data.json', uri='mongodb+srv://maryiasakharava:SensorDataPassword@sensordata.pjdhs9k.mongodb.net/?retryWrites=true&w=majority&appName=SensorData')
