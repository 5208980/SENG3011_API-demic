import pandas as pd
import json
import datetime
import requests
import re
from datetime import timedelta, datetime
from collections import OrderedDict
from operator import *
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
    TODAY = datetime.now()
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
    total = {}
    total['Confirmed'] = 0
    total['Deaths'] = 0
    total['Recovered'] = 0
    for index, row in df.iterrows():
        convert_country = identify_country(row['Country_Region'])
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

    return OrderedDict(sorted(dataset.items(), reverse=True, key=lambda x: getitem(x[1], 'Confirmed')))

def head_generate_data():
    dataset = generate_data()
    while len(dataset) > 5:
        dataset.popitem()
    print(dataset)

    return dataset

def generate_total():
    GIT = 'https://raw.githubusercontent.com/'
    PATH = 'CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/'
    TODAY = datetime.now()
    FILENAME = '{:02d}-{:02d}-{}.csv'.format(TODAY.month, TODAY.day, TODAY.year)
    URL = '{}{}{}'.format(GIT, PATH, FILENAME)

    r = requests.get(URL)
    while not r.ok:
        TODAY = TODAY - timedelta(days=1)
        FILENAME = '{:02d}-{:02d}-{}.csv'.format(TODAY.month, TODAY.day, TODAY.year)
        URL = '{}{}{}'.format(GIT, PATH, FILENAME)
        r = requests.get(URL)

    df = pd.read_csv(URL, error_bad_lines=False)

    total = {}
    total['Confirmed'], total['Deaths'], total['Recovered'], total['Active'] = 0, 0, 0, 0
    for index, row in df.iterrows():
        total['Confirmed'] += row['Confirmed']
        total['Deaths'] += row['Deaths']
        total['Recovered'] += row['Recovered']
        total['Active'] += row['Active']

    return total

def validate_date(d):
    try:
        date = datetime.strptime(d, "%Y-%m-%d")
        if date > datetime.now():
            return False;
        return True
    except ValueError:
        return False

def json_to_string(s):
    ret = str(s)
    ret = re.sub('\'', '\"', ret)
    ret = re.sub('[a-zA-Z]\,', '', ret)
    ret = re.sub('[a-zA-Z]\"[a-zA-Z]', '', ret)

    return ret
