import Adafruit_DHT
from datetime import datetime



# Function to read DHT sensor data
def read_dht_sensor():
    # Extract data from Sensor
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 19)
    if humidity is not None and temperature is not None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return {
            'temperature': temperature,
            'humidity': humidity,
            'timestamp': timestamp
        }
    else:
        print("Failed to read from DHT sensor")
        return None
