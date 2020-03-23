import requests                 # for fetching raw html of websites
from bs4 import BeautifulSoup   # to scrape data from html requests
import re                       # Filter publication, disease, and location
import time                     # Time conversion
import datetime                 # Used for scraping article by days
from datetime import timedelta  # Used to increment day
import json                     # JSON Parser
from geotext import GeoText         # Lib to determine locations

# Classes
from article import *
from reports import *
from locations import *

# from fuzzywuzzy import fuzz     # Temporary text matcher
    # print("############ {}".format(publication.get_text()[x.end():]))
    #
    # # Options Text match with or use fuzzy wuzzy to match closest
    # numbers = []
    # for disease in data_disease:
    #     ratio = fuzz.partial_ratio(disease, publication.get_text()[x.end():])
    #     # print(ratio)
    #     numbers.append(ratio)
    #
    # m = max(numbers)
    # indexs = [i for i, j in enumerate(numbers) if j == m]
    # print(data[indexs[0]])
import pickle                       # FOR TESTING STATIC DATA (WILL REMOVE WHEN DB IS OUT)

MONTHS_PATTERN = r"January|February|March|April|May|June|July|August|September|October|November|December|Jan\.|Feb\.|Mar\.|Apr\.|May\.|Jun\.|Jul\.|Aug\.|Sep\.|Sept\.|Oct\.|Nov\.|Dec\."
MONTHS_MAP = {
    "Jan.": "January",
    "Feb.": "February",
    "Mar.": "March",
    "Apr.": "April",
    "May.": "May",
    "Jun.": "June",
    "Jul.": "July",
    "Aug.": "August",
    "Sept.": "September",
    "Oct.": "October",
    "Nov.": "November",
    "Dec.": "December"
}

# Load list of disease
with open('dataset/disease_list.json') as data_file:
    data_disease = json.load(data_file)
# country to text match country
with open('dataset/country.json') as data_file:
    data_country = json.load(data_file)
# Load list of disease
with open('dataset/syndrome_list.json') as data_file:
    data_syndrome = json.load(data_file)

def country_text_is_refering(text):
    country_found = []
    shortword = re.compile(r'\W*\b\w{1,3}\b')
    text = shortword.sub('', text)

    for country in data_country:
        if country['name'] in text:
            results = GeoText(text, country['alpha_2']).cities
            if results != []:
                results = list(dict.fromkeys(results))
                for result in results:
                    country_found.append(Locations(country['name'], result, country['alpha_3']))
            else:
                country_found.append(Locations(country['name'], "", country['alpha_3']))

    return country_found

def disease_text_is_refering(text):
    disease_found = ""
    for disease in data_disease:
        if disease['name'].lower() in text:
            disease_found = disease['name']

    return disease_found

def syndrome_text_is_refering(text):
    syndrome_found = ""
    for syndrome in data_syndrome:
        if syndrome['name'].lower() in text:
            syndrome_found = syndrome['name']

    return syndrome_found

# Assumption: That the year corresponds to the year the article was written
# Return: string
def found_event_date(main_text, date):
    date_regex = re.compile(MONTHS_PATTERN)
    x = re.finditer(date_regex, main_text)
    event_dates = []            # keeps all event dates found in text
    for y in x:
        s = re.sub(r'[^\w\s]','',main_text[y.start()-3:y.end()+3]).split()
        for i in s:
            if i.isdigit():
                year, month, day = date[0:4], time.strptime(MONTHS_MAP.get(y.group(), y.group()), "%B").tm_mon, i
                if int(i) <= 0 or int(i) > 31:
                    day = "1"
                # print("{}-{}-{}".format(year, month, day))
                event_dates.append(datetime.date(int(year),int(month),int(day)))

    if len(event_dates) == 1:
        return "{} xx:xx:xx".format(event_dates[0].isoformat())
    elif len(event_dates) >= 2:
        return "{} xx:xx:xx to {} xx:xx:xx".format(min(event_dates).isoformat(), max(event_dates).isoformat())

    return ""

articles = []               # DELETE LATER
##### Scraping process #####
def scrape_url(link):
    html_doc = requests.get(link)
    soup = BeautifulSoup(html_doc.content, 'html.parser')

    # Found all header, text, date of publish
    headers = soup.findAll("h3", {"class": "entry-header"})
    main_texts = soup.findAll("div", {"class": "entry-body"})
    publications = soup.findAll("span", {"class": "post-footers"})

    next_page = soup.findAll("span", {"class": "pager-right"})
    next_page_exist = False
    if next_page != []:
        next_page_exist = True

    dates = []
    key_terms = []
    for publication in publications:
        # Key Terms
        terms = []
        for link in publication.find_all('a'):
            # print(link.get_text())
            terms.append(link.get_text())

        key_terms.append(terms)

        # Date
        x = re.search("^.* PM|^.* AM", publication.get_text())
        date = publication.get_text()[x.start():x.end()].split()

        # TODO: CONVERT TIME INTO 24 HR
        # m2 = '1:35 PM'
        # in_time = datetime.strptime(m2, "%I:%M %p")
        # out_time = datetime.strftime(in_time, "%H:%M")
        # print(out_time)

        datetime = "{}-{:02d}-{} {}:{}".format(date[2], time.strptime(date[0], "%B").tm_mon, date[1][:-1], date[4], "00")
        dates.append(datetime)

    for header, main_text, date, key_term in zip(headers, main_texts, dates, key_terms):
        print("######################################################")

        tmp = {}
        tmp['url'] = ""
        if not main_text.a is None:
            tmp['url'] = main_text.a.get('href')
        tmp['date_of_publication'] = date
        tmp['headline'] = header.get_text()
        tmp['main_text'] = main_text.get_text()
        tmp['key_terms'] = key_term

        # print(key_term)
        # We can add other stuff to help with postgres like KEYWORDS, TERMS, ETC
        raw_text = ' '.join([header.get_text(), main_text.get_text()])
        tmp['reports'] = Reports(found_event_date(main_text.get_text(), date), country_text_is_refering(raw_text), disease_text_is_refering(raw_text.lower()), syndrome_text_is_refering(raw_text.lower()));

        # One article created here
        article = Article(tmp['url'], tmp['date_of_publication'], tmp['headline'], tmp['main_text'], tmp['reports'], tmp['key_terms'])
        # print(article.get_terms())
        articles.append(article)    # DELETE LATER

    return next_page_exist

##### Use to scrape all articles from start to end date #####
def main_function():
    start_date = datetime.datetime(2020, 1, 1)
    end_date = datetime.datetime.now()
    while start_date < end_date:
        # print(type(start_date.month))
        page_number = 1;
        next_page_exist = True;
        # Scraping Function will go here
        while next_page_exist:
            url = "https://crofsblogs.typepad.com/h5n1/{}/{:02d}/{:02d}/page/{}".format(start_date.year, start_date.month, start_date.day, page_number)
            print(url)
            next_page_exist = scrape_url(url)
            page_number = page_number + 1

        start_date = start_date + timedelta(days=1)

    # DELETE LATER
    print("HERE")
    with open('output.pickle', 'wb') as p:
        pickle.dump(articles, p)


# INSTRUCTIONS
# Scraper can fulfil all requirements if they exist. Very Basic string matching
# To run scraper for database use main_function() above and change the dates
# scrape_url('https://crofsblogs.typepad.com/h5n1/2020/02/05/page/1')
main_function()
