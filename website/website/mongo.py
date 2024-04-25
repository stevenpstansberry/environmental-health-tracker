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

"""""
Get the DHT and BME data every day on last week
Returns: result_dict(dict) - key: sensor type, all daily data from DHT and BME
"""""
def calculate_last_week_avg_data():
    # Get the current date and current day of the week (Monday is 0, Sunday is 6)
    today = datetime.today()
    current_weekday = today.weekday()

    # Calculate the dates of last Monday and last Sunday
    last_monday = today - timedelta(days=current_weekday + 7)
    last_sunday = last_monday + timedelta(days=6)

    # Define the MongoDB aggregation pipeline, filter out the data from last Monday to Sunday, 
    #group it by date, and calculate the average data for each day
    pipeline = [
        {
            '$match': {
                'timestamp': {
                    '$gte': last_monday,
                    '$lte': last_sunday
                }
            }
        },
        {
            '$group': {
                '_id': {
                    '$dateToString': {
                        'format': '%Y-%m-%d',
                        'date': '$timestamp'
                    }
                },
                'avg_temperature': {
                    '$avg': '$DHT.temperature'  # Calculate the average temperature
                },
                'avg_humidity': {
                    '$avg': '$DHT.humidity'  # Calculate the average humidity
                },
                'avg_pressure':{
                    '$avg': '$DME.pressure' # Calculate the average pressure
                },

                # it can continue to add average calculations for other fields
            }
        }
    ]

    #Execute aggregate query
    result = list(collection.aggregate(pipeline))

    # Store the calculation results in a dictionary 
    #where the keys are date strings and the values ​​are dictionaries containing average data
    week_avg_data = {}
    for entry in result:
        date_str = entry['_id']
        avg_temp = entry['avg_temperature']
        avg_humidity = entry['avg_humidity']
        avg_pressure = entry['avg_pressure']
        # it can continue to add other fields.

        week_avg_data[date_str] = {
            'avg_temperature': avg_temp,
            'avg_humidity': avg_humidity,
            'avg_pressure': avg_pressure
            # it can continue to add other fields.
        }
    print(week_avg_data)
    return week_avg_data

"""
Dew point temperature is calculated based on temperature (Celsius) and relative humidity.
Use the Magnus-Tetens formula for approximate calculations.
"""
def calculate_dew_point(temperature, humidity):
    temp_celsius = temperature
    rh = humidity / 100.0 # Convert relative humidity from percentage to decimal

# Constants for the Magnus-Tetens formula
    a = 17.27
    b = 237.7

# Calculate intermediate value (gamma) for Dew Point calculation
    gamma = (a * temp_celsius) / (b + temp_celsius) + log(rh)

# Calculate Dew Point temperature (in Celsius)
    dew_point = (b * gamma) / (a - gamma)
    return dew_point

def calculate_last_week_avg_data_dew_points():
# Get the current date and current day of the week (Monday is 0, Sunday is 6)
    today = datetime.today()
    current_weekday = today.weekday()   
    # Calculate the dates of last Monday and last Sunday
    last_monday = today - timedelta(days=current_weekday + 7)
    last_sunday = last_monday + timedelta(days=6)

    # Define MongoDB aggregation pipeline
    pipeline = [
        {
            '$match': {
                'timestamp': {
                    '$gte': last_monday,
                    '$lte': last_sunday
                }
            }
        },
        {
            '$group': {
                '_id': {
                    '$dateToString': {
                        'format': '%Y-%m-%d',
                        'date': '$timestamp'
                    }
                },
                'avg_temperature': {
                    '$avg': '$DME.temperature'  # Calculate the average temperature
                },
                'avg_pressure': {
                    '$avg': '$DME.pressure' # Calculate the average pressure

                }
            }
        }
    ]

    #Execute aggregate query
    result = list(collection.aggregate(pipeline))

    # Collect daily dew point temperature data
    week_dew_points = {}
    for entry in result:
        date_str = entry['_id']
        avg_temp = entry['avg_temperature']
        avg_pressure = entry['avg_pressure']

        # Calculate dew point temperature based on daily average temperature and air pressure
        dew_point = calculate_dew_point(avg_temp, avg_pressure)

        # Store data in dictionary
        week_dew_points[date_str] = dew_point

    return week_dew_points

def calculate_heat_index(temperature, humidity):
    """
    Heat Index is calculated based on temperature (Celsius) and relative humidity.
    Use the formula provided by the National Weather Service (NWS)
    """
    temp_fahrenheit = (temperature * 9/5) + 32
    heat_index = (
        -42.379 +
        (2.04901523 * temp_fahrenheit) +
        (10.14333127 * humidity) -
        (0.22475541 * temp_fahrenheit * humidity) -
        (6.83783e-3 * temp_fahrenheit**2) -
        (5.481717e-2 * humidity**2) +
        (1.22874e-3 * temp_fahrenheit**2 * humidity) +
        (8.5282e-4 * temp_fahrenheit * humidity**2) -
        (1.99e-6 * temp_fahrenheit**2 * humidity**2)
    )

    return heat_index



"""
Heat Index is calculated based on temperature (Celsius) and relative humidity.
Use the formula provided by the National Weather Service (NWS).
"""
def calculate_last_week_avg_data_heat_indexes():
    today = datetime.today()
    current_weekday = today.weekday()

    # Calculate the dates of last Monday and last Sunday
    last_monday = today - timedelta(days=current_weekday + 7)
    last_sunday = last_monday + timedelta(days=6)

    # Define MongoDB aggregation pipeline
    pipeline = [
        {
            '$match': {
                'timestamp': {
                    '$gte': last_monday,
                    '$lte': last_sunday
                }
            }
        },
        {
            '$group': {
                '_id': {
                    '$dateToString': {
                        'format': '%Y-%m-%d',
                        'date': '$timestamp'
                    }
                },
                'avg_temperature': {
                    '$avg': '$DHT.temperature'  # Calculate the average temperature
                },
                'avg_humidity': {
                   '$avg': '$DHT.humidity'  # Calculate the average humidity
                }
            }
        }
    ]

    #Execute aggregate query
    result = list(collection.aggregate(pipeline))

    # Collect daily Heat Index data
    week_heat_indexes = {}
    for entry in result:
        date_str = entry['_id']
        avg_temp = entry['avg_temperature']
        avg_humidity = entry['avg_humidity']

        # Calculate Heat Index based on daily average temperature and humidity
        heat_index = calculate_heat_index(avg_temp, avg_humidity)

       # Store data in dictionary
        week_heat_indexes[date_str] = heat_index

    return week_heat_indexes   
def calculate_last_week_avg_data_with_chart_data():
    # Calculate last week's average data
    week_avg_data = calculate_last_week_avg_data()

    # Prepare chart data structure
    chart_data = {'temp': [], 'hum': [], 'press': []}

    # Process each day's data
    for date_str, avg_data in week_avg_data.items():
        # Append temperature and humidity to chart data
        if 'avg_temperature' in avg_data:
            chart_data['temp'].append(avg_data['avg_temperature'])
        if 'avg_humidity' in avg_data:
            chart_data['hum'].append(avg_data['avg_humidity'])
        if 'avg_pressure' in avg_data:
            chart_data['press'].append(avg_data['avg_pressure'])

    # Print or return chart data
    print(chart_data)
    return chart_data

def calculate_last_week_avg_data_dew_points_with_chart_data():
    # Calculate last week's average dew point data
    week_dew_points = calculate_last_week_avg_data_dew_points()

    # Prepare chart data structure
    chart_data = {'dew_point': []}

    # Process each day's data
    for date_str, dew_point in week_dew_points.items():
        # Append dew point to chart data
        chart_data['dew_point'].append(dew_point)

    # Print or return chart data
    print(chart_data)
    return chart_data


def calculate_last_week_avg_data_heat_indexes_with_chart_data():
    # Calculate last week's average heat index data
    week_heat_indexes = calculate_last_week_avg_data_heat_indexes()

    # Prepare chart data structure
    chart_data = {'heat_index': []}

    # Process each day's data
    for date_str, heat_index in week_heat_indexes.items():
        # Append heat index to chart data
        chart_data['heat_index'].append(heat_index)

    # Print or return chart data
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

