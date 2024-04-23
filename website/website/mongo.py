import json
from pymongo import MongoClient
from datetime import datetime, timedelta
import os


cluster = MongoClient("mongodb+srv://Viewer:1234@sensordata.1v3p4ie.mongodb.net/?retryWrites=true&w=majority")
db = cluster["sensor_data"]  # space in cloud
collection = db["data"]  # table

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
    
    print(result_dict)
    return result_dict


"""
Get the DHT and BME data on the latest day
Returns: sensor_data(dict) - key: sensor type, all DHT and BME data on the latest day
"""
def get_latest_day_sensor_data():
    last_data = get_latest_data()
    last_timestamp = last_data["DHT"]["timestamp"].split()[0]
    print(last_timestamp)
    start_date = datetime.strptime(last_timestamp, "%Y-%m-%d")
    end_date = start_date + timedelta(days=1)
    # end_date -= timedelta(seconds=1)
    # print(start_date)
    # print(end_date)

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
    print(sensor_data)
    return sensor_data

"""
Get the DHT and BME data on the latest day for chart use
Returns: chart_data(dict) - key: type of data, all DHT and BME data on the latest day
"""
def latest_day_chart_data():
    daily_data = get_latest_day_sensor_data()
    chart_data = {'temp': [], 'hum': [], 'press': []}

    for d in daily_data['DHT']:
        chart_data['temp'].append(d['temperature'])
        chart_data['hum'].append(d['humidity'])

    for d in daily_data['BME']:
        chart_data['press'].append(d['pressure'])


    print(chart_data)
    return chart_data



####

# cursor = collection.find({})

# # Print the data
# print(list(cursor))

# for document in cursor:
#     print(document)



# Close the MongoDB connection
# cluster.close()

