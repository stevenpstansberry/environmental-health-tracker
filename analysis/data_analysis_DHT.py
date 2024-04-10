import pymongo
from datetime import datetime
from statistics import mean

#connect the MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")

#select the database and collections
db = client["sensor_data"]
collection = db["data"]

#Define time range based on time interval
def calculate_statistics(field_name, interval, sensor_type):
    if interval == "daily":
        start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = start_date + timedelta(days=1)
    elif interval == "weekly":
        start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=datetime.now().weekday())
        end_date = start_date + timedelta(days=7)
    elif interval == "monthly":
        start_date = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        if start_date.month == 12:
            end_date = start_date.replace(year=start_date.year + 1, month=1)
        else:
            end_date = start_date.replace(month=start_date.month + 1)
    
    #query MongoDB to files within a specified time range
    query = {
        f"{sensor_type}.timestamp": {"$gte": start_date, "$lt": end_date},
        f"{sensor_type}.{field_name}": {"$exists": True}
    }
    documents = collection.find(query)


    #Extract the value of a field within a specified time range
    field_values = []

    for document in documents:
        if sensor_type in document:
            sensor_data = document[sensor_type]
            for entry in sensor_data:
                if field_name in entry:
                    field_values.append(entry[field_name])

    # Calculate statistics
    if field_values:
        average_value = mean(field_values)
        highest_value = max(field_values)
        lowest_value = min(field_values)
        statistics = {
            "average": round(average_value, 2),
            "highest": round(highest_value, 2),
            "lowest": round(lowest_value, 2)
        }
        return statistics
    else:
        return None

# Calculate temperature statistics using "DHT" sensor type
temperature_daily_stats = calculate_statistics("temperature", "daily", "DHT")
temperature_weekly_stats = calculate_statistics("temperature", "weekly", "DHT")
temperature_monthly_stats = calculate_statistics("temperature", "monthly", "DHT")

print("Temperature（Daily）:", temperature_daily_stats)
print("Temperature（Weekly）:", temperature_weekly_stats)
print("Temperature（Monthly）:", temperature_monthly_stats)
print("-------------------------------------------------------")

# Calculate humidity statistics using "DHT" sensor type
humidity_daily_stats = calculate_statistics("humidity", "daily", "DHT")
humidity_weekly_stats = calculate_statistics("humidity", "weekly", "DHT")
humidity_monthly_stats = calculate_statistics("humidity", "monthly", "DHT")

print("humidity（Daily）:", humidity_daily_stats)
print("humidity（Weekly）:", humidity_weekly_stats)
print("humidity（Monthly）:", humidity_monthly_stats)



client.close()
