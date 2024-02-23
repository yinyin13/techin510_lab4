# ⏰ World Clock
This is a web app that provides the current time and real-time weather information for selected countries. Users can hoose up to 4 countries to monitor, and the weather data is fetched every hour.
## How to run
1. Make sure that Python is installed on your device
2. Clone this repo
```bash
git clone https://github.com/yinyin13/techin510_lab4.git
```
3. Open project directory
```bash
cd project-directory
```
4. Install packages
```bash
pip install -r requirements.txt
```
5. Run the app on local host
```bash
streamlit run app.py
```

To access the web app directly online, go to [World Clock ⏰](http://yinyin13-worldclock.azurewebsites.net/)
## Lessons Learned
- I'm now more familiar with OOP, web scraping, and calling APIs
- I learned how to use regex and the `zoneinfo` library
- I'm comfortable with using `for` and `while` loops with `lists`

## Future Improvements for the App
- Improve app performance and efficiency: Right now there is a slight delay between the user's selection and the actual display of time and weather. Also, whenever the selection is updated, there will be another delay. I think this experienced can be optimized by handling the data fetching and display in a different way.
- Add a ❤️ feature to allow users to save specific locations
- Improve overall UI and usability
