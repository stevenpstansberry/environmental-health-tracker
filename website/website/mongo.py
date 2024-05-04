import json
from pymongo import MongoClient
from datetime import datetime, timedelta
import os
from math import log

# Connect to MongoDB cluster
cluster = MongoClient("mongodb+srv://maryiasakharava:SensorDataPassword@sensordata.pjdhs9k.mongodb.net/?retryWrites=true&w=majority&appName=SensorData")
db = cluster["sensor_data"]
collection = db["test_data"]


"""
Get the latest update DHT and BME data 
Returns: result_dict(dict) - key: sensor type, all latest update data from DHT and BME
"""
def get_latest_data():
    pipeline = [
        {
            "$addFields": {
                "DHT": { "$last": "$DHT" },
                "BME": { "$last": "$BME" }
            }
        },
        {
            "$project": {
                "_id": 0,  # exclude _id field
                "DHT": 1,
                "BME": 1
            }
        }
    ]

    result = collection.aggregate(pipeline)

    result_dict = {}
    for doc in result:
        for key, value in doc.items():
            result_dict[key] = value
    
    # print(result_dict)
    return result_dict


"""
Get all the DHT and BME data on the input day
Args: date(str) - "yyyy-mm-dd", The date on which you want to get the sensor_data
Returns: sensor_data(dict) - key: sensor type, all DHT and BME data on the day
    {'DHT': [{'temperature': , 'humidity': , 'timestamp': }, ...], 
     'BME': [{'temperature': , 'humidity': , 'pressure': , 'timestamp': }, ...]}
"""
def get_day_sensor_data(date):
    start_date = datetime.strptime(date, "%Y-%m-%d")
    end_date = start_date + timedelta(days=1)
    # end_date -= timedelta(seconds=1)

    pipeline = [
        {
            '$project': {
                '_id': 0, 
                'DHT': {
                    '$filter': {
                        'input': '$DHT', 
                        'cond': {
                            '$and': [
                                {
                                    '$gte': [
                                        '$$this.timestamp', start_date.strftime("%Y-%m-%d 00:00:00")
                                    ]
                                }, {
                                    '$lt': [
                                        '$$this.timestamp', end_date.strftime("%Y-%m-%d 00:00:00")
                                    ]
                                }
                            ]
                        }
                    }
                }, 
                'BME': {
                    '$filter': {
                        'input': '$BME', 
                        'cond': {
                            '$and': [
                                {
                                    '$gte': [
                                        '$$this.timestamp', start_date.strftime("%Y-%m-%d 00:00:00")
                                    ]
                                }, {
                                    '$lt': [
                                        '$$this.timestamp', end_date.strftime("%Y-%m-%d 00:00:00")
                                    ]
                                }
                            ]
                        }
                    }
                }
            }
        }
    ]

    result = collection.aggregate(pipeline)

    sensor_data = {}
    for doc in result:
        for key, value in doc.items():
            sensor_data[key] = value

    # print(sensor_data)
    return sensor_data


"""
Convert all the data seperate by sensor to seperate by type of data for chart use
Args: day_sensor_data(dict) - data seperate by sensor
    {'DHT': [{'temperature': , 'humidity': , 'timestamp': }, ...], 
     'BME': [{'temperature': , 'humidity': , 'pressure': , 'timestamp': }, ...]}
Returns: chart_data(dict) - key: type of data, all data on the day
    {'temperature': [], 'humidity': [], 'pressure': [], 'timestamp': []}
"""
def convert_day_chart_data(day_sensor_data):
    chart_data = {'temperature': [], 'humidity': [], 'pressure': [], 'timestamp': []}

    for d in day_sensor_data['DHT']:
        chart_data['temperature'].append(d['temperature'])
        chart_data['humidity'].append(d['humidity'])
        chart_data['timestamp'].append(d['timestamp'])

    for d in day_sensor_data['BME']:
        chart_data['pressure'].append(d['pressure'])


    # print(chart_data)
    return chart_data

"""
Get all the DHT and BME data at the time
Args: timestamp - "yyyy-mm-dd hh:mm:ss"
Returns: data_dict(dict) - key: sensor type, all DHT and BME data at the time
    {'DHT': {'temperature': , 'humidity': , 'timestamp': }, 
     'BME': {'temperature': , 'humidity': , 'pressure': , 'timestamp': }}
"""
def get_data_by_timestamp(timestamp):    
    # Query MongoDB for documents with the specified timestamp
    query = {"$or": [{"DHT.timestamp": timestamp}, {"BME.timestamp": timestamp}]}
    result = collection.find_one(query)
    
    # Extract DHT and BME data
    dht_data = next((d for d in result.get("DHT", []) if d["timestamp"] == timestamp), None)
    bme_data = next((d for d in result.get("BME", []) if d["timestamp"] == timestamp), None)
    
    # Check if both DHT and BME data are found
    if dht_data is None or bme_data is None:
        return None
    
    # Format the data
    data_dict = {
        "DHT": {
            "temperature": dht_data["temperature"],
            "humidity": dht_data["humidity"],
            "timestamp": dht_data["timestamp"]
        },
        "BME": {
            "temperature": bme_data["temperature"],
            "humidity": bme_data["humidity"],
            "pressure": bme_data["pressure"],
            "timestamp": bme_data["timestamp"]
        }
    }
    
    return data_dict



####
# cursor = collection.find({})

# for document in cursor:
#     print(document)


# Close the MongoDB connection
# cluster.close()

