import pandas as pd
import json
import datetime
import requests
import re
from datetime import timedelta
from countries import countries

def identify_country(country):
    switcher = {
        "US": "United States",
        "Bolivia": "Bolivia, Plurinational State of",
        "Brunei": "Brunei Darussalam",
        "Congo (Brazzaville)": "Congo",
        "Congo (Kinshasa)": "Congo, The Democratic Republic of the",
        "Cote d'Ivoire": "Côte d'Ivoire",
        "Diamond Princess": "",
        "Holy See": "Holy See (Vatican City State)",
        "Iran": "Iran, Islamic Republic of",
        "Korea, South": "Korea, Republic of",
        "Kosovo": "",
        "Laos": "Lao People's Democratic Republic",
        "Moldova": "Moldova, Republic of",
        "Russia": "Russian Federation",
        "Syria": "Syrian Arab Republic",
        "Taiwan*": "Taiwan, Province of China",
        "Tanzania": "Tanzania, United Republic of",
        "Venezuela": "Venezuela, Bolivarian Republic of",
        "Vietnam": "Viet Nam",
        "West Bank and Gaza": "",
    }

    return switcher.get(country, country)

def generate_data():
    GIT = 'https://raw.githubusercontent.com/'
    PATH = 'CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/'
    TODAY = datetime.datetime.now()
    FILENAME = '{:02d}-{:02d}-{}.csv'.format(TODAY.month, TODAY.day, TODAY.year)
    URL = '{}{}{}'.format(GIT, PATH, FILENAME)

    r = requests.get(URL)
    while not r.ok:
        TODAY = TODAY - timedelta(days=1)
        FILENAME = '{:02d}-{:02d}-{}.csv'.format(TODAY.month, TODAY.day, TODAY.year)
        URL = '{}{}{}'.format(GIT, PATH, FILENAME)
        r = requests.get(URL)

    df = pd.read_csv(URL, error_bad_lines=False)

    dataset = {}

    for index, row in df.iterrows():
        convert_country = identify_country(row['Country_Region'])
        convert_country = identify_country(row['Country_Region'])
        # print(countries.get(convert_country, ""))
        data = dataset.get(convert_country, False)
        if not data:

            data = {}
            data['Code'] = countries.get(convert_country, "")
            data['Confirmed'] = row['Confirmed']
            data['Deaths'] = row['Deaths']
            data['Recovered'] = row['Recovered']
            data['Active'] = row['Active']
            dataset[convert_country] = data
        else:
            # print('already in dataset')
            dataset[convert_country]['Confirmed'] += row['Confirmed']
            dataset[convert_country]['Deaths'] += row['Deaths']
            dataset[convert_country]['Recovered'] += row['Recovered']
            dataset[convert_country]['Active'] += row['Active']

    return dataset
