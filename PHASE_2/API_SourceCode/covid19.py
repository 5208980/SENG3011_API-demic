import pandas as pd
import json
import datetime
import requests
import re
from bs4 import BeautifulSoup   # to scrape data from html requests
from datetime import timedelta, datetime
from collections import OrderedDict
from operator import *
# import pycountry

from countries import countries
from countryISO import *

def identify_country(country):
    switcher = {
        "Diamond Princess": "Cruise Ship",
        "Cote d'Ivoire": "Ivory Coast",
        "Holy See": "Holy See",
        "Korea, South": "South Korea",
        "Kosovo": "",
        "Taiwan*": "Taiwan",
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
        convert_country = re.sub('\,', '', convert_country)
        convert_country = re.sub('\"', '', convert_country)
        data = dataset.get(convert_country, False)
        if not data:
            data = {}
            data['Code'] = ISO_3_to_2(countries.get(convert_country, ""))

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
    resource_id = '2776dbb8-f807-4fb2-b1ed-184a6fc2c8aa'; # Location and source
    # 21304414-1ff1-4243-a5d2-f52778048b29 # location
    get_limit = requests.get('https://data.nsw.gov.au/data/api/3/action/datastore_search?resource_id={}&limit=20'.format(resource_id))
    limit = get_limit.json()['result']['total']
    r = requests.get('https://data.nsw.gov.au/data/api/3/action/datastore_search?resource_id={}&limit={}'.format(resource_id, limit))

    dataset = {}
    records = r.json()['result']['records']
    for i in records:
        nsw_lga__3 = re.sub('\(A\)|\(C\)|\(NSW\)', '', i['lga_name19']).strip().lower()
        # dataset['nsw_lga__3'] = nsw_lga__3
        # print(nsw_lga__3.strip().lower())
        data = dataset.get(nsw_lga__3, False)
        if not data:
            tmp = {}
            tmp['count'] = 1
            tmp['date'] = i['notification_date']
            dataset[nsw_lga__3] = tmp
        else:
            dataset[nsw_lga__3]['count'] += 1
            dataset[nsw_lga__3]['latest_confirmed'] = i['notification_date']

    # return r.json()

    latest_cases = requests.get('https://data.nsw.gov.au/data/api/3/action/datastore_search?resource_id={}&limit={}&offset={}'.format(resource_id, limit, limit-50))
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
        tmp['likely_source_of_infection'] = i['likely_source_of_infection']

        data.append(tmp);

    dataset_2['records'] = data

    return dataset, dataset_2

def wa_positive_cases():
    cases = requests.get('https://interactive.guim.co.uk/covidfeeds/wa.json'.format())
    # print(latest_cases.json()['result']['records'])
    json = {}
    for i in cases.json():
        tmp = {}
        tmp['count'] = i['count']
        tmp['date'] = i['date']
        json[re.sub('\([ACTS]\)', '', i['place']).strip().lower()] = tmp

    return json

def vic_positive_cases():
    cases = requests.get('https://interactive.guim.co.uk/covidfeeds/victoria.json'.format())
    json = {}
    for i in cases.json():
        tmp = {}
        tmp['count'] = i['count']
        tmp['date'] = i['date']
        json[re.sub('\([ACTSB]\)|\(Rc\)', '', i['place']).strip().lower()] = tmp

    return json

def qld_positive_cases():
    cases = requests.get('https://interactive.guim.co.uk/covidfeeds/queensland.json'.format())
    # print(latest_cases.json()['result']['records'])
    json = {}
    for i in cases.json():
        tmp = {}
        tmp['count'] = i['count']
        tmp['date'] = i['date']
        json[re.sub('\\n', '', i['place']).strip().lower()] = tmp

    return json

def au_time_series():
    cases = requests.get('https://interactive.guim.co.uk/docsdata/1q5gdePANXci8enuiS4oHUJxcxC13d6bjMRSicakychE.json'.format())
    json = {}
    json['ACT'] = []
    json['NSW'] = []
    json['VIC'] = []
    json['TAS'] = []
    json['WA'] = []
    json['SA'] = []
    json['QLD'] = []
    records = cases.json()['sheets']['updates']
    for record in records:
        tmp = {}
        tmp['date'] = record['Date']
        tmp['cases'] = 0 if record['Cumulative case count'] == '' else int(record['Cumulative case count'])
        tmp['deaths'] = 0 if record['Cumulative deaths'] == '' else int(record['Cumulative deaths'])
        tmp['recovered'] = 0 if record['Recovered (cumulative)'] == '' else int(record['Recovered (cumulative)'])
        tmp['tests'] = 0 if record['Tests conducted (total)'] == '' else int(record['Tests conducted (total)'])
        tmp['hospitalised'] = 0 if record['Hospitalisations (count)'] == '' else int(record['Hospitalisations (count)'])
        print(record['State'])
    return json

def australia_latest():
    cases = requests.get('https://interactive.guim.co.uk/docsdata/1q5gdePANXci8enuiS4oHUJxcxC13d6bjMRSicakychE.json'.format())
    records = cases.json()['sheets']['latest totals']
    main = {}
    states = {}
    for record in records:
        if(record['State or territory'] != 'National'):
            tmp = {}
            tmp['cases'] = 0 if record['Confirmed cases (cumulative)'] == '' else int(record['Confirmed cases (cumulative)'])
            tmp['deaths'] = 0 if record['Deaths'] == '' else int(record['Deaths'])
            tmp['recovered'] = 0 if record['Recovered'] == '' else int(record['Recovered'])
            tmp['tests'] = 0 if record['Tests conducted'] == '' else int(record['Tests conducted'])
            tmp['hospitalised'] = 0 if record['Current hospitalisation'] == '' else int(record['Current hospitalisation'])
            states[record['State or territory']] = tmp
        else:
            main['last_updated'] = record['Last updated']
    main['states'] = states

    latest_deaths = cases.json()['sheets']['deaths']
    arr = []
    for death in latest_deaths:
        arr.append({
            'state': death['State'],
            'date': death['Date of death'],
            'details': death['Details'],
            'source': death['Source']
        });

    # print(arr.reverse())
    main['deaths'] = arr

    sites = {}
    sources = cases.json()['sheets']['sources']
    for source in sources:
        sites[source['state']] = source['daily update']

    return main, sites

# Be integrated in our API, if we had time
advices = [
    {'icon': 'fa-hands-wash', 'tip': 'Wash your hands often'},
    {'icon': 'fa-people-arrows', 'tip': 'Practise social distancing'},
    {'icon': 'fa-handshake-slash', 'tip': 'Avoid touching your faces and others'},
    {'icon': 'fa-virus', 'tip': 'Wear mask to limit exposure when going outside'},
    {'icon': 'fa-stethoscope', 'tip': 'If you have sick, stay home and call your doctor'},
    {'icon': 'fa-user-slash', 'tip': 'Be sure to follow your country\\\'s social gathering limit'},
]

def generateSafetyAdvices():

    json = {}
    json['advices'] = advices
    json['length'] = len(advices)
    return json

nsw_positive_cases()



# from pytrends.request import TrendReq
#
# pytrends = TrendReq(hl='en-US', tz=360)
# pytrends.build_payload(kw_list=['Coronavirus'])
# related_queries = pytrends.related_queries()
#
# for i in related_queries.values():
#     print(i)
