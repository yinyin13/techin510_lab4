import requests
from bs4 import BeautifulSoup

def timezone_scraper():
    url = 'https://timezonedb.com/time-zones'
    res = requests.get(url).text
    soup = BeautifulSoup(res, 'html.parser')
    country = soup.find('tbody').text

    country_ls = country.split('\n')

    while '' in country_ls:
        country_ls.remove('')

    tz_ls = country_ls[2::4]
    return tz_ls