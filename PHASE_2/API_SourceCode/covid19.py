import pandas as pd
import json
import datetime
import requests
import re
from bs4 import BeautifulSoup   # to scrape data from html requests
from datetime import timedelta, datetime
from collections import OrderedDict
from operator import *
from countries import countries
import pycountry

def identify_country(country):
    switcher = {
        # "US": "United States",
        "Congo (Brazzaville)": "Republic of the Congo",
        "Congo (Kinshasa)": "Democratic Republic of the Congo",
        "Diamond Princess": "",
        "Holy See": "Holy See (Vatican City State)",
        "Korea, South": "South Korea",
        "Kosovo": "",
        "Syria": "Syrian Arab Republic",
        "Taiwan*": "Taiwan",
        "Tanzania": "United Republic of Tanzania",
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

    print(list(pycountry.countries)[0])

    dataset = {}
    total = {}
    total['Confirmed'] = 0
    total['Deaths'] = 0
    total['Recovered'] = 0
    for index, row in df.iterrows():
        convert_country = identify_country(row['Country_Region'])
        convert_country = re.sub('\,', '', convert_country)
        convert_country = re.sub('\"', '', convert_country)
        data = dataset.get(convert_country, False)
        if not data:

            data = {}
            data['Code'] = ""
            if countries.get(convert_country, "") != "":
                if pycountry.countries.get(alpha_3=countries.get(convert_country, "")).alpha_2 == 'TW':
                    print(pycountry.countries.get(alpha_3=countries.get(convert_country, "")).alpha_2)
                data['Code'] = pycountry.countries.get(alpha_3=countries.get(convert_country, "")).alpha_2
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
    while len(dataset) > 10:
        dataset.popitem()

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

    return ret

import urllib

def nsw_positive_cases():
    get_limit = requests.get('https://data.nsw.gov.au/data/api/3/action/datastore_search?resource_id=21304414-1ff1-4243-a5d2-f52778048b29&limit=20')
    limit = get_limit.json()['result']['total']
    r = requests.get('https://data.nsw.gov.au/data/api/3/action/datastore_search?resource_id=21304414-1ff1-4243-a5d2-f52778048b29&limit={}'.format(limit))
    # print(r.json())

    dataset = {}
    records = r.json()['result']['records']
    for i in records:
        nsw_lga__3 = re.sub('\(A\)|\(C\)|\(NSW\)', '', i['lga_name19']).strip().lower()
        # dataset['nsw_lga__3'] = nsw_lga__3
        # print(nsw_lga__3.strip().lower())
        data = dataset.get(nsw_lga__3, False)
        if not data:
            tmp = {}
            tmp['positive'] = 1
            tmp['latest_confirmed'] = i['notification_date']
            dataset[nsw_lga__3] = tmp
        else:
            dataset[nsw_lga__3]['positive'] += 1
            dataset[nsw_lga__3]['latest_confirmed'] = i['notification_date']
    # return r.json()

    latest_cases = requests.get('https://data.nsw.gov.au/data/api/3/action/datastore_search?resource_id=21304414-1ff1-4243-a5d2-f52778048b29&limit={}&offset={}'.format(limit, limit-50))
    # print(latest_cases.json()['result']['records'])
    dataset_2 = {}
    data = []
    records = latest_cases.json()['result']['records']
    for i in records:
        nsw_lga__3 = re.sub('\(A\)|\(C\)|\(NSW\)', '', i['lga_name19']).strip().lower()
        tmp = {}
        # tmp['nsw_lga__3'] = nsw_lga__3
        tmp['nsw_lga__3'] = nsw_lga__3 if nsw_lga__3 != "" else "unknown"
        # tmp['postcode'] = i['postcode']
        tmp['postcode'] = i['postcode'] if not i['postcode'] is None else "unknown"
        tmp['notification_date'] = i['notification_date']

        data.append(tmp);

    dataset_2['records'] = data

    return dataset, dataset_2

# nsw_positive_cases()

# from pytrends.request import TrendReq
#
# pytrends = TrendReq(hl='en-US', tz=360)
# pytrends.build_payload(kw_list=['Coronavirus'])
# related_queries = pytrends.related_queries()
#
# for i in related_queries.values():
#     print(i)


# def covidWhoAdvice():
#     html_doc = requests.get('https://www.who.int/emergencies/diseases/novel-coronavirus-2019/advice-for-public')
#     soup = BeautifulSoup(html_doc.content, 'html.parser')
#
#     main = soup.find(id="PageContent_C003_Col01")
#     blocks = main.findAll("div", {"class": "content-block"})
#
#     for block in blocks:
#         print(block.get_text())
#
# covidWhoAdvice()

generate_data()
