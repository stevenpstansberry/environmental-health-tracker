import math


"""
Convert temperature from Fahrenheit to Celsius.
Args: fahrenheit(float) - Temperature in Fahrenheit
Returns: celsius(float) - Temperature converted to Celsius
"""
def fahrenheit_to_celsius(fahrenheit):
    celsius = (fahrenheit - 32) * 5 / 9
    return celsius

"""
Convert temperature from Celsius to Fahrenheit.
Args: celsius(float) - Temperature in Celsius
Returns: fahrenheit(float) - Temperature converted to Fahrenheit
"""
def celsius_to_fahrenheit(celsius):
    fahrenheit = (celsius * 9 / 5) + 32
    return fahrenheit


### Dashboard page
"""
Calculates the dew point temperature
Args: temp_c(float) - Temperature in Celsius
    hum(float) - Relative humidity in percentage
Returns: dew_point_temperature(float) - Dew point temperature in Celsius
"""
def dew_point_calc(temp_c, hum):
    a = 17.62
    b = 243.12
    gamma = (a * temp_c) / (b + temp_c) + math.log(hum / 100.0)
    dew_point_temperature = (b * gamma) / (a - gamma)
    return dew_point_temperature


"""
Calculates the heat index temperature
Args: temp_f(float) - Temperature in Celsius
    hum(float) - Relative humidity in percentage
Returns:  heat_index(float) - Heat index temperature in Celsius
"""
def calculate_heat_index(temp_c, hum):
    temp_f = celsius_to_fahrenheit(temp_c)
    if temp_f < 80:
        # Using simpler formula
        heat_index = 0.5 * (temp_f + 61.0 + ((temp_f - 68.0) * 1.2) + (hum * 0.094))
    else:
        # Full regression equation
        heat_index = (-42.379 +
                      2.04901523 * temp_f +
                      10.14333127 * hum -
                      0.22475541 * temp_f * hum -
                      0.00683783 * temp_f ** 2 -
                      0.05481717 * hum ** 2 +
                      0.00122874 * temp_f ** 2 * hum +
                      0.00085282 * temp_f * hum ** 2 -
                      0.00000199 * temp_f ** 2 * hum ** 2)

        if hum < 13 and 80 <= temp_f <= 112:
            adjustment = ((13 - hum) / 4) * math.sqrt((17 - abs(temp_f - 95.0)) / 17)
            heat_index -= adjustment

        if hum > 85 and 80 <= temp_f <= 87:
            adjustment = ((hum - 85) / 10) * ((87 - temp_f) / 5)
            heat_index += adjustment

    heat_index = fahrenheit_to_celsius(heat_index)
    return heat_index





