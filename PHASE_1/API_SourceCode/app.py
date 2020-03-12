# To run use python3 app.py
# To test open another terminal and curl localhost

from flask import Flask, request
from flask_restful import Resource, Api, reqparse

import re                    # For regex
import datetime
import json

import pickle                   # FOR TESTING STATIC DATA (WILL REMOVE WHEN DB IS OUT)

app = Flask(__name__)
api = Api(app)

# Test url: http://127.0.0.1:5000/articles?start_date=2020-01-01T12:00:00&end_date=2020-02-01T12:00:00&location=australia&key_term=coronavirus
class Article(Resource):
    def get(self):
        # Query Parameters
        print(request.args['start_date'])
        print(request.args['end_date'])
        print(request.args['location'])
        print(request.args['key_term'])

        ## Error Handling and Logging Status ##
        # Validate Date
        date_regex = re.compile('^(\d{4})-(\d\d|xx)-(\d\d|xx)T(\d\d|xx):(\d\d|xx):(\d\d|xx)$')
        if not date_regex.search(request.args['start_date']) or not date_regex.search(request.args['end_date']) or request.args['start_date'] > request.args['end_date']:
            # Maybe print file error msg, not sure
            return {"status": 400, "message": "Invalid Query Parameters (Date)" }, 400

        # Validate Location
        # with open('dataset/country.json') as data_file:
        #     data_country = json.load(data_file)
        #
        # found_country = False
        # for country in data_country:
        #     if country['name'].lower() in request.args['location'].lower():
        #         found_country = True
        #         break
        #
        # if not found_country:
        #     return {"status": 400, "message": "Invalid Query Parameters (Country)" }, 400

        # Validate Key Term
        print("HERE")
        ## Log ##
        info(request.url)

        ## DB Query ##

        with open('output.pickle', 'rb') as p:
            articles = pickle.load(p)

        data = {}
        data['articles'] = []
        for article in articles:
            dict_article = {}
            dict_article['url'] = article.get_url()
            dict_article['date_of_publication'] = article.get_date_of_publication()
            dict_article['headline'] = article.get_headline()
            dict_article['main_text'] = article.get_main_text()

            dict_reports = {}
            dict_reports["event_date"] = article.get_reports().get_event_date()
            dict_reports["locations"] = []
            for location in article.get_reports().get_locations():
                dict_location = {}
                dict_location["country"] = location.get_country()
                dict_location["location"] = location.get_location()
                # print(location.get_country())
                dict_reports["locations"].append(dict_location)
            dict_reports["disease"] = article.get_reports().get_disease()
            dict_reports["syndrome"] = article.get_reports().get_syndrome()
            dict_article['reports'] = dict_reports

            data['articles'].append(dict_article)

        return data, 200

        # if data['articles'] != []:
        #     return data, 200
        # else:
        #     return {"status": 404, "message": "No result for query"}, 404

api.add_resource(Article, '/articles')

# File Log: Should I create a logger class?
def info(msg):
    f = open("log.txt", "a")
    f.write("Log: {} {}\n".format(msg, datetime.datetime.now()))
    f.close()

# Test Function
class HelloWorld(Resource):
    def get(self):
        return {
            "url": "https://www.who.int/csr/don/17-january-2020-novel-coronavirus-japan-exchina/en/",
            "date_of_publication": "2020-01-17 xx:xx:xx",
            "headline": "Novel Coronavirus – Japan (ex-China)",
            "main_text": "The case-patient is male, between the age of 30- 39 years, living in Japan. The case-patient travelled to Wuhan, China in late December and developed fever on 3 January 2020 while staying in Wuhan. He did not visit the Huanan Seafood Wholesale Market or any other live animal markets in Wuhan. He has indicated that he was in close contact with a person with pneumonia. On 6 January, he traveled back to Japan and tested negative for influenza when he visited a local clinic on the same day.",
            "reports": [
                {
                    "event_date": "2020-01-03 xx:xx:xx to 2020-01-15",
                    "locations": [
                        {
                            "country": "China",
                            "location": "Wuhan, Hubei Province"
                        },
                        {
                            "country": "Japan",
                            "location": ""
                        }
                    ],
                    "diseases": [
                        "2019-nCoV"
                    ],
                    "syndromes": [
                        "Fever of unknown Origin"
                    ]
                }
            ]
        }
api.add_resource(HelloWorld, '/test')

if __name__ == '__main__':
    app.run(debug=True)
