# Environmental-Health-Tracker

Environmental Health Tracker is a web application that monitors and visualizes environmental data from sensors. It provides a user-friendly interface to view real-time and historical data on temperature, humidity, pressure, air quality, dew point, and heat index. The data is sourced from a Raspberry Pi connected to a suite of sensors that read in from the local environment. The data is updated every ten minutes, providing a near live assessment of local meterological conditions

## Features

### Web Interface

- **Dashboard**: Displays the current sensor readings, including temperature, humidity, pressure, and air quality(not implemented/in progress) sensors, and calculates the dew point and heat index based on the collected data. It also shows the highest and lowest values for the selected data type.
  - **Daily Data Movement**: Provides a line chart to visualize the daily trend for temperature, humidity, pressure, or air quality(not implemented/in progress).
  - **Location**: Shows the sensor location on a map (not implemented/in progress).
- **Analysis**: Offers a comprehensive analysis page to explore weekly(using sample data) and monthly(not implemented/in progress) trends for various data types. Users can view average, highest, and lowest values, as well as line charts for all types of data.
- **User Authentication**: Includes sign-in and sign-up pages for user authentication (not implemented/in progress).

### Local Data Collection

- **Temperature**: Both the DHT22 and BME280 sensors are able to read in the ambient temperature and output the temperature.
- **Humidity**: Both the DHT22 and BME280 sensors are able to read in the ambient humidity and output the humidity.
- **Pressure**: The BME280 sensor is able to read in the pressure in the ambient environment.
- **Volatile Organic Compounds (VOC)**: The SGP40 sensors is capable of providing a reading indicating the overall air quality of the ambient environment

### Data Upload

While the the Raspberry Pi is active and collecting data, it will automatically attempt to upload to the MongoDB database which the web interface will interact and obtain its data from.

## Technologies Used

- **Hardware**: Raspberry Pi 3, Sensors: DHT22, BME280,SGP40
- **Front-end**: HTML, CSS, JavaScript, Chart.js
- **Back-end**: Python, Flask
- **Database**: MongoDB

## Project Structure

- `website/`: Contains the Flask application code.
- `__init__.py`: Initializes the Flask application and registers blueprints.
- `calc_data.py`: Functions for calculating dew point and heat index.
- `mongo.py`: Functions for interacting with the MongoDB database.
- `views.py`: Flask routes and view functions.
- `templates/`: HTML templates for the web pages.
  - `index.html`: Dashboard page.
  - `analysis.html`: Analysis page.
  - `pages-sign-in.html`: Sign-in page.
  - `pages-sign-up.html`: Sign-up page.
- `static/`: Static files (CSS, JavaScript, images, fonts).
- `sensors/`: Contains the code for the Raspberry Pi to read in the data from the sensors, parse it, and upload it to MongoDB
  - `BME280_sensor.py`: Code for reading from BME280 sensor
  - `DHT_sensor.py`: Code for reading from DHT22 sensors
  - `driver.py`: Driver code that calls functions from other local files. Serves as entry point to begin data collection
  - `upload.py`: Code for uploading JSON file (output of sensor reading) to MongoDB

## Installation

1. Clone the repository
2. Install the required Python packages: `pip install -r requirements.txt`
3. Set up the MongoDB connection in `mongo.py`.
4. Start the Flask application: `python run.py`
5. Access the application at `http://localhost:5000`.

## Usage

1. Visit the dashboard page to view the current sensor readings and daily data movement.
2. Navigate to the analysis page to explore weekly and monthly (not implemented/in progress) trends for various data types.
3. Use the provided buttons and controls to switch between data types, navigate through weeks/months (not implemented/in progress), and interact with the visualizations.
