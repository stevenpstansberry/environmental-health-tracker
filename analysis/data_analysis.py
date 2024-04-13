import pymongo
from datetime import datetime
from statistics import mean

client = pymongo.MongoClient("mongodb://localhost:27017/")

db = client["sensor_data"]
collection = db["data"]

def calculate_statistics(field_name, interval):
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
    
    query = {
        "DHT.timestamp": {"$gte": start_date, "$lt": end_date},
        f"DHT.{field_name}": {"$exists": True}
    }
    documents = collection.find(query)

    field_values = [entry["DHT"][field_name] for document in documents for entry in document["DHT"]]

    if field_values:
        average_value = mean(field_values)
        highest_value = max(field_values)
        lowest_value = min(field_values)
        print(f"Average{field_name}（{interval}）: {average_value:.2f}")
        print(f"Highest{field_name}（{interval}）: {highest_value:.2f}")
        print(f"Lowest{field_name}（{interval}）: {lowest_value:.2f}")
    else:
        print(f"can't find {interval} the {field_name} data")

calculate_statistics("temperature", "daily")
calculate_statistics("temperature", "weekly")
calculate_statistics("temperature", "monthly")
print("-------------------------------------------------------")
calculate_statistics("humidity", "daily")
calculate_statistics("humidity", "weekly")
calculate_statistics("humidity", "monthly")


client.close()
