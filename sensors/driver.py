import RPi.GPIO as GPIO
import time
import json
import threading
from datetime import datetime, timedelta
from DHT_sensor import read_dht_sensor
from BME280_sensor import read_bme_sensor


# Set lED to GPIO 18
LED_PIN = 18  
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

def blink_led():
    """Function to blink the LED every second."""
    while True:
        GPIO.output(LED_PIN, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(LED_PIN, GPIO.LOW)
        time.sleep(0.5)


# Function to store data locally
def store_data_locally(data, sensor_name, filename='sensor_data.json'):
    # Create a dictionary to store data by sensor
    organized_data = {
        sensor_name: data
    }
    
    # Read the existing data and update it
    try:
        with open(filename, 'r') as file:
            file_data = json.load(file)
        # Ensure there is a list corresponding to sensor_name parameter
        if sensor_name in file_data:
            # If it's not a list yet, make it a list
            if not isinstance(file_data[sensor_name], list):
                file_data[sensor_name] = [file_data[sensor_name]]
            file_data[sensor_name].append(data)
        else:
            # Create a new list for this sensor if it doesn't exist
            file_data[sensor_name] = [data]
    except (FileNotFoundError, json.JSONDecodeError):
        # Create JSON if it doesn't exist.
        file_data = {sensor_name: [data]}
    
    # Write the updated data to the file
    with open(filename, 'w') as file:
        json.dump(file_data, file, indent=4)       

if __name__ == '__main__':
	 # Start the LED blinking in a separate thread
    led_thread = threading.Thread(target=blink_led)
    led_thread.daemon = True
    led_thread.start()
    
    
    try:
        while True:
            # Read sensor data
            dht_sensor_data = read_dht_sensor()
            bme_sensor_data = read_bme_sensor()
            
            # Print out DHT sensor data and store it if it exists
            if dht_sensor_data:
                print("DHT:", dht_sensor_data)
                # Store data locally
                store_data_locally(dht_sensor_data,"DHT")
                
            
            # Print out BME sensor data and store it if it exists
            if bme_sensor_data:
                print("BME: ", bme_sensor_data)
                # Store data locally
                store_data_locally(bme_sensor_data,"BME")



            #TODO upload here
            # use sensor_data.json to upload to mongodb 
            
            # Calculate and print the time for the next reading
            next_reading_time = datetime.now() + timedelta(minutes=10)
            print(f"Next reading will occur at: {next_reading_time.strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Wait for 10 minutes before next iteration
            time.sleep(600) 
            
    # Control C to terminate
    except KeyboardInterrupt:
        print("Exiting program")
    finally:
        GPIO.cleanup()
        print("GPIO cleaned up")

   
