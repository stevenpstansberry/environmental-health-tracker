from pymongo import MongoClient
import json
from pymongo.errors import ServerSelectionTimeoutError
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

def upload_json_to_mongo(json_file):
    try:
        # Get MongoDB URI from environment variables
        uri = os.getenv("MONGO_URI")
        if not uri:
            raise ValueError("MONGO_URI is not set in .env file")

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
    except ValueError as e:
        print(e)
    finally:
        # Close the connection
        client.close()

# Call the function to upload the data
upload_json_to_mongo('sample_sensor_data.json')
