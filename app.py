import streamlit as st
import datetime
from zoneinfo import ZoneInfo
import time
from timezone_scraper import timezone_scraper
from weather_scraper import get_location_coordinates, get_weather, ingest_data_to_db, interpret_weather_code

# Set page configurations
st.set_page_config(
    page_title="World Clock",
    page_icon=":alarm_clock:",
    layout="centered",  # centered or wide
    initial_sidebar_state="auto",
)

# Display title of the page
st.title("World Clock")

# Import timezone locations
location = timezone_scraper()
location.sort()

# Show drop-down menu to select location
selected_countries = st.multiselect(
    "Which countries would you like to see the time for? You can select up to 4.",
    location,
    max_selections=4
)

if selected_countries:
    # Create a 2x2 layout
    cols = st.columns(2)

    # Display time for each selected country in the layout
    time_placeholders = [cols[i % 2].empty() for i in range(len(selected_countries))]
    weather_data = [{} for _ in range(len(selected_countries))]

    cycles = 0

    while True:
        time_now = datetime.datetime.now()
        for i, (country, placeholder) in enumerate(zip(selected_countries, time_placeholders)):

            # Convert to specific timezone inside strftime
            date_str = time_now.astimezone(ZoneInfo(country)).strftime("%Y-%m-%d")
            time_str = time_now.astimezone(ZoneInfo(country)).strftime("%H:%M:%S")
            
            # Fetch weather only every hour
            if cycles % 3600 == 0: 
                latitude, longitude = get_location_coordinates(country)
                temperature, weather_description = get_weather(latitude, longitude)
                weather_description = interpret_weather_code(weather_description)

                db_path = 'weather.sqlite'
                data = (country, date_str, weather_description, temperature)
                ingest_data_to_db("cities", data, db_path)

                weather_data[i] = {'description': weather_description, 'temperature': temperature}

            placeholder.markdown(f'{country}\n### {time_str}\n{date_str}\n{weather_data[i]["description"]}, {weather_data[i]["temperature"]}°C')

        time.sleep(1)

        cycles += 1  # Increment the cycle count after each sleep to update the seconds