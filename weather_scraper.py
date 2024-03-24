import requests
import openmeteo_requests
import sqlite3
from geopy.geocoders import Nominatim

def get_location_coordinates(location_query):
    geolocator = Nominatim(user_agent="my_geocoder")
    location = geolocator.geocode(location_query)
    if location:
        return location.latitude, location.longitude
    else:
        print("Location not found.")
        return None, None

def get_weather(latitude, longitude):
    # Setup the Open-Meteo API client
    openmeteo = openmeteo_requests.Client()

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": ["temperature_2m", "weather_code"],
        "forecast_days": 1
    }

    # Send the request and get the responses
    responses = openmeteo.weather_api('https://api.open-meteo.com/v1/forecast', params=params)

    # Process the first response
    response = responses[0]

    # Get the current weather parameters
    current = response.Current()
    current_temperature_2m = current.Variables(0).Value()
    current_weather_code = current.Variables(1).Value()

    return round(current_temperature_2m), current_weather_code

def interpret_weather_code(current_weather_code):
    code_dict = {
        0: "☀️ Clear sky",
        1: "🌤️ Mainly clear", 
        2: "🌥️ Partly cloudy", 
        3: "☁️ Overcast",
        45: "🌫️ Fog",
        48: "🌫️ Depositing rime fog",
        51: "🌧️ Light Drizzle",
        53: "🌧️ Moderate Drizzle",
        55: "🌧️ Dense Drizzle",
        56: "🌧️ Freezing Light Drizzle",
        57: "🌧️ Freezing Dense Drizzle",
        61: "☂️ Slight Rain",
        63: "☔️ Moderate Rain",
        65: "☔️ Heavy Rain",
        66: "☂️ Freezing Light Rain",
        67: "☔️ Freezing Heavy Rain",
        71: "🌨️ Slight Snow Fall",
        73: "❄️ Moderate Snow Fall",
        75: "☃️ Heavy Snow Fall",
        77: "🌨️ Snow Grains",
        80: "☔️ Slight Rain Showers",
        81: "☔️ Moderate Rain Showers",
        82: "⛈️ Violent Rain Showers",
        85: "⛄️ Slight Snow Showers",
        86: "☃️ Heavy Snow Showers",
        95: "🌩️ Slight / Moderate Thunderstorm",
        96: "⛈️ Thunderstorm with Slight Hail",
        99: "⛈️ Thunderstorm with Heavy Hail"
    }

    return code_dict.get(current_weather_code, "Unknown weather code")


def ingest_data_to_db(table_name, data, db_path):
    con = sqlite3.connect(db_path, isolation_level=None)
    cur = con.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS cities (
            id INTEGER PRIMARY_KEY,
            city TEXT,
            date TEXT,
            weather TEXT,
            temperature TEXT
        )
        """
    )

    placeholders = ', '.join(['?'] * len(data))

    insert_query = f"INSERT INTO {table_name} (city, date, weather, temperature) VALUES (?, ?, ?, ?)"
    cur.execute(insert_query, data)

    con.commit()
    con.close()