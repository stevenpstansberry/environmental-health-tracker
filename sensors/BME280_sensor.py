import smbus2
import bme280
from datetime import datetime



def read_bme_sensor():
    # Set BME sensor Address
    address = 0x76 
    # Init I2C bus
    bus = smbus2.SMBus(1)

    # Calibration parameters
    calibration_params = bme280.load_calibration_params(bus, address)
    # Fetch data
    data = bme280.sample(bus, address, calibration_params)
    
    # Extract data and return as dict
    temperature = data.temperature
    humidity = data.humidity
    pressure = data.pressure
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


    return{
            'temperature': temperature,
            'humidity': humidity,
            'pressure': pressure,
            'timestamp': timestamp
        }

