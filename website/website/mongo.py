import json
from pymongo import MongoClient
from datetime import datetime, timedelta
import os
from math import log

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

def get_last_week_date_range():
    today = datetime.now()
    # The date of last Monday
    last_monday = today - timedelta(days=today.weekday() + 7)
    # The date of last Sunday
    last_sunday = last_monday + timedelta(days=6)
    last_week_ranges = []
    # Calculate the date range for each day of last week using a loop
    for i in range(7):
        # Date of a certain day of last week
        day = last_monday + timedelta(days=i)
        # Start time of that day (00:00)
        start_date = datetime(day.year, day.month, day.day, 0, 0)
        # End time of that day (23:59)
        end_date = datetime(day.year, day.month, day.day, 23, 59)
        # Append the range to the list
        last_week_ranges.append((start_date, end_date))
    return last_week_ranges

def get_weekly_sensor_data(start_date, end_date):
    # MongoDB aggregation pipeline to filter data based on timestamp
    pipeline = [
        {
            "$match": {
                "timestamp": {
                    "$gte": start_date,
                    "$lte": end_date
                }
            }
        },
        {
            "$project": {
                "_id": 0,
                "DHT": 1,
                "BME": 1
            }
        }
    ]
    # Execute the pipeline and retrieve data
    result = collection.aggregate(pipeline)
    sensor_data = {"DHT": [], "BME": []}
    # Process the retrieved data
    for doc in result:
        if 'DHT' in doc:
            sensor_data['DHT'].extend(doc['DHT'])
        if 'BME' in doc:
            sensor_data['BME'].extend(doc['BME'])
    return sensor_data

def calculate_daily_averages(sensor_data):
    # Group data by date and calculate averages
    daily_averages = {}
    # Initialize structure for daily averages
    for sensor_type in sensor_data:
        daily_averages[sensor_type] = {}

    for sensor_type, readings in sensor_data.items():
        for reading in readings:
            date_key = reading['timestamp'].strftime("%Y-%m-%d")
            if date_key not in daily_averages[sensor_type]:
                daily_averages[sensor_type][date_key] = {
                    'temperature': [],
                    'humidity': [],
                    'pressure': [],
                }
            daily_averages[sensor_type][date_key]['temperature'].append(reading['temperature'])
            daily_averages[sensor_type][date_key]['humidity'].append(reading['humidity'])
            if 'pressure' in reading:
                daily_averages[sensor_type][date_key]['pressure'].append(reading['pressure'])

    for sensor_type, dates in daily_averages.items():
        for date, sensors in dates.items():
            for key in sensors:
                sensors[key] = sum(sensors[key]) / len(sensors[key]) if sensors[key] else None

    return daily_averages

def convert_weekly_chart_data(daily_averages):
    chart_data = {'temperature': [], 'humidity': [], 'pressure': [], 'timestamp': []}
    for sensor_type, dates in daily_averages.items():
        for date, data in dates.items():
            if 'temperature' in data:
                chart_data['temperature'].append({'date': date, 'value': data['temperature']})
            if 'humidity' in data:
                chart_data['humidity'].append({'date': date, 'value': data['humidity']})
            if 'pressure' in data:
                chart_data['pressure'].append({'date': date, 'value': data['pressure']})
            chart_data['timestamp'].append(date)

    return chart_data

# Example Usage

# Call the functions in the main program and print the data
if __name__ == "__main__":
    # Get the date range of the last week
    last_week_ranges = get_last_week_date_range()
    print("Last Week Date Ranges:")
    for i, (start_date, end_date) in enumerate(last_week_ranges):
        print(f"Day {i+1}:")
        print("Start Date:", start_date)
        print("End Date:", end_date)
        print()

    # Get sensor data for each day from last Monday to last Sunday
    for i, (start_date, end_date) in enumerate(last_week_ranges):
        print(f"Sensor Data for Day {i+1}:")
        sensor_data = get_weekly_sensor_data(start_date, end_date)
        print(sensor_data)

    # Calculate daily averages for each day
    for i, (start_date, end_date) in enumerate(last_week_ranges):
        print(f"Daily Averages for Day {i+1}:")
        sensor_data = get_weekly_sensor_data(start_date, end_date)
        daily_averages = calculate_daily_averages(sensor_data)
        chart_data = convert_weekly_chart_data(daily_averages)
        print(chart_data)


####

# cursor = collection.find({})

# # Print the data
# print(list(cursor))

# for document in cursor:
#     print(document)



# Close the MongoDB connection
# cluster.close()

