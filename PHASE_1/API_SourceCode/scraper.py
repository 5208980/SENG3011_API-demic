import requests                 # for fetching raw html of websites
from bs4 import BeautifulSoup   # to scrape data from html requests
import re                       # Filter publication, disease, and location
import time                     # Time conversion
import datetime                 # Used for scraping article by days
from datetime import timedelta  # Used to increment day
import json                     # JSON Parser

# from fuzzywuzzy import fuzz     # Temporary text matcher

# Load list of disease
with open('dataset/disease_list.json') as data_file:
    data_disease = json.load(data_file)
# country to text match country
with open('dataset/country.json') as data_file:
    data_country = json.load(data_file)
# Load list of disease
with open('dataset/syndrome_list.json') as data_file:
    data_syndrome = json.load(data_file)

##### To determine what country the article is talking about #####
def country_text_is_refering(header, main_text):
    country_found = ""
    for country in data_country:
        if country['name'] in header.get_text():
            print(country['name'])
            country_found = country['name']
            break

    # Unable to found country in header, try main_text
    if country_found == "":
        for country in data_country:
            if country['name'] in main_text.get_text():
                print(country['name'])
                country_found = country['name']
                break

##### Scraping process #####
def scrape_url(link):
    # Gets the request          TESTING MAIN PAGE
    html_doc = requests.get(link)
    soup = BeautifulSoup(html_doc.content, 'html.parser')

    # Found all header, text, date of publish
    headers = soup.findAll("h3", {"class": "entry-header"})
    main_texts = soup.findAll("div", {"class": "entry-body"})
    publications = soup.findAll("span", {"class": "post-footers"})

    dates = []
    for publication in publications:
        x = re.search("^.* PM|^.* AM", publication.get_text())
        date = publication.get_text()[x.start():x.end()]
        # print(date.split())

        # print(date.split()[2])
        # print(time.strptime(date.split()[0], "%B").tm_mon)
        # print(date.split()[1][:-1])

        # TODO: CONVERT TIME INTO 24 HR
        # m2 = '1:35 PM'
        # in_time = datetime.strptime(m2, "%I:%M %p")
        # out_time = datetime.strftime(in_time, "%H:%M")
        # print(out_time)

        datetime = "{}-{}-{} {}".format(date.split()[2], time.strptime(date.split()[0], "%B").tm_mon, date.split()[1][:-1], date.split()[4])
        # print(datetime)
        dates.append(datetime)

        ################################
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

    for header, main_text, date in zip(headers, main_texts, dates):
        print("######################################################")
        # print('url: {}'.format(main_text.a.get('href')))
        # print('date_of_publication: {}'.format(date))
        # print('headline: {}'.format(header.get_text()))
        # print('main_text: {}'.format(main_text.get_text()))

        tmp = {}
        tmp['url'] = main_text.a.get('href')
        tmp['date_of_publication'] = date
        tmp['headline'] = header.get_text()
        tmp['main_text'] = main_text.get_text()
        tmp['reports'] = []

        # Very bad method but best so far
        # TODO: Syndrome
        # print('country: {}'.format(country_text_is_refering(header, main_text)))



##### Use to scrape all articles from start to end date #####
# def main_function():
#     start_date = datetime.datetime(2020, 2, 25)
#     end_date = datetime.datetime.now()
#     while start_date < end_date:
#         # print(type(start_date.month))
#         print("https://crofsblogs.typepad.com/h5n1/{}/{:02d}/{:02d}/".format(start_date.year, start_date.month, start_date.day))
#
#         # Scraping Function will go here
#         scrape_url("https://crofsblogs.typepad.com/h5n1/{}/{:02d}/{:02d}/".format(start_date.year, start_date.month, start_date.day))
#         start_date = start_date + timedelta(days=1)


# INSTRUCTIONS
# so far I'm just testing the scrapw with the main PAGE
# so when the scrape is complete and the data can load its dates
# we need to call main_function; main_function need to change start date to whenever
# we like to scrape from
scrape_url('https://crofsblogs.typepad.com/h5n1/')
