# CMPE-195-Environmental-Health-Tracker
CMPE 195AB

Environmental Health Tracker is a web application that monitors and visualizes environmental data from sensors. It provides a user-friendly interface to view real-time and historical data on temperature, humidity, pressure, air quality, dew point, and heat index.

## Features
Web Interface
- **Dashboard**: Displays the current sensor readings, including temperature, humidity, pressure, and air quality(not implemented/in progress) sensors, and calculates the dew point and heat index based on the collected data. It also shows the highest and lowest values for the selected data type.
  - **Daily Data Movement**: Provides a line chart to visualize the daily trend for temperature, humidity, pressure, or air quality(not implemented/in progress).
  - **Location**: Shows the sensor location on a map (not implemented/in progress).
- **Analysis**: Offers a comprehensive analysis page to explore weekly(using sample data) and monthly(not implemented/in progress) trends for various data types. Users can view average, highest, and lowest values, as well as line charts for all types of data.
- **User Authentication**: Includes sign-in and sign-up pages for user authentication (not implemented/in progress).

## Technologies Used
- **Hardware**: Raspberry Pi 3, Sensors: DHT22, BME280
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
