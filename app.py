import streamlit as st
import datetime
from zoneinfo import ZoneInfo
import requests
from bs4 import BeautifulSoup
import time
from timezone_scraper import timezone_scraper


# Set page configurations
st.set_page_config(
    page_title="World Clock",
    page_icon="⏰",
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
    "Which countries would you like to see the time for? You can select up to 4.", location, max_selections=4
)

# placeholder = st.empty()

col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

# Create variables to store time data
time1 = datetime.datetime.now(tz=ZoneInfo(selected_countries[0])).isoformat("\n", "seconds")

col1.metric(selected_countries[0], time1)
col2.metric(selected_countries[1], "9 mph", "-8%")
col3.metric(selected_countries[2], "86%", "4%")
col4.metric(selected_countries[3], "86%", "4%")

# cnt = 0
# while True:
#     with placeholder.container():
#         placeholder.metric("Seconds since you arrived this page", cnt)
#         cnt += 1
#     time.sleep(1)