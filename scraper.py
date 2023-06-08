import datetime
import csv
import requests
import sys
import time
import pandas as pd
from random import randint
from bs4 import BeautifulSoup
from dateutil import parser

scrape_datetime = datetime.datetime.utcnow().isoformat()
all_country = {
    "IND":"India",
    "UK": "UK",
    "US": "US",
    "AUS": "AUS",
    "NZ": "NZ",
    "UAE": "UAE",
    "MY": "MALAYSIA",
    "DE": "GERMANY",
    "PK": "Pakistan",
    "CN": "China"
}

def scraping_data(soup, country):
    soup = soup
    all_deta = []
    all_tr = soup.find_all("tr", class_="table-row")
    if country == "India":
        for x in all_tr[1:]:
            name = x.find_all("td", class_="table-cell")[0].text
            release_data = x.find_all("td", class_="table-cell")[1].text
            date_time = parser.parse(release_data)
            relase = str(date_time).replace("00:00:00", "").replace("-", "/")
            opening_day = x.find_all("td", class_="table-cell")[2].text
            opening_day = float(opening_day) if "N.A" not in opening_day else ""
            opening_weekend = x.find_all("td", class_="table-cell")[3].text
            opening_weekend = float(opening_weekend) if "N.A" not in opening_weekend else ""
            end_off_wek = x.find_all("td", class_="table-cell")[4].text
            end_off_wek = float(end_off_wek) if "N.A" not in end_off_wek else ""
            lifetime = x.find_all("td", class_="table-cell")[5].text
            lifetime = float(lifetime) if "N.A" not in lifetime else ""
            full_objekt = {
                "scrape_datetime": scrape_datetime,
                "country": country,
                "movie name": name,
                "release data": relase,
                "total groos": "",
                "opening day": opening_day,
                "opening weekend": opening_weekend,
                "end off wek": end_off_wek,
                "lifetime": lifetime
            }
            all_deta.append(full_objekt)
    else:
        for x in all_tr[1:]:
            name = x.find_all("td", class_="table-cell")[0].text
            release_data = x.find_all("td", class_="table-cell")[1].text
            date_time = parser.parse(release_data)
            relase = str(date_time).replace("00:00:00", "").replace("-", "/")
            total_groos = x.find_all("td", class_="table-cell")[2].text.replace(",", ".")
            full_objekt = {
                "scrape_datetime": scrape_datetime,
                "country": country,
                "movie name": name,
                "release data": relase,
                "total groos":total_groos,
                "opening day": "",
                "opening weekend": "",
                "end off wek": "",
                "lifetime": ""
                
            } 
            all_deta.append(full_objekt)
    return all_deta
def all_country_data():
    finally_data=[]
    for coun, country in all_country.items():
        time.sleep(randint(2,4))
        url=f"https://www.bollywoodhungama.com/box-office-collections/filterbycountry/{coun}/2023/"
        re = requests.get(url)
        soup = BeautifulSoup(re.content, 'html.parser')
        country_deta=scraping_data(soup, country)
        finally_data.extend(country_deta)
    return finally_data

def run(filename: str):
    """
    This function will be the main entrypoint to your code and will be called with a filename.
    """
    
    # We use the requests library to load data but you could also use `get_countries_via_chrome()`.
    countries = all_country_data()
    
    output = pd.DataFrame(countries)
    
    output.to_csv(
        filename,
        encoding="utf-8",
        quotechar='"',
        quoting=csv.QUOTE_ALL,
        index=False
    )