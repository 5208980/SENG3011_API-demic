# To run use python3 app.py
# To test open another terminal and curl localhost

from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_swagger_ui import get_swaggerui_blueprint    # Swagger UI

import re                       # For regex
import datetime
import json

import time                     # For rutime process

import pickle                   # FOR TESTING STATIC DATA (WILL REMOVE WHEN DB IS OUT)

# import psycopg2                # POSTGRES connection
# import sys

# conn = psycopg2.connect("dbname={}")
# cur = conn.cursor()
# conn.close()

app = Flask(__name__)
api = Api(app)

SWAGGER_URL = ''
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={ 'app_name': "API-demic" }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT)

# https://api-demic.herokuapp.com/articles?start_date=2020-01-01T12:00:00&end_date=2020-02-01T12:00:00&location=australia&key_term=coronavirus
# Test url: http://127.0.0.1:5000/articles?start_date=2020-01-01T12:00:00&end_date=2020-02-01T12:00:00&location=australia&key_term=coronavirus
class ArticleV1(Resource):
    def get(self):
        # File
        exe_start_time = time.perf_counter()

        # For backend and end user
        logger = {}
        logger["method"] = request.method
        logger["url"] = request.url
        logger["time"] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        ## Error Handling and Logging Status ##
        # Validate Date
        date_regex = re.compile('^(\d{4})-(\d\d|xx)-(\d\d|xx)T(\d\d|xx):(\d\d|xx):(\d\d|xx)$')
        if not date_regex.search(request.args['start_date']) or not date_regex.search(request.args['end_date']) or request.args['start_date'] > request.args['end_date']:
            # Maybe print file error msg, not sure
            # print("Reponse Status: {}".format(400))
            exe_end_time = time.perf_counter()
            logger["runtime"] = round(exe_end_time - exe_start_time, 2)
            logger["reponse"] = 400
            print(logger)

            backend_log(logger)
            return {"status": 400, "message": "Invalid Query Parameters (Date)" }

        data = query_and_convert()

        exe_end_time = time.perf_counter()
        logger["runtime"] = round(exe_end_time - exe_start_time, 5)

        if data['articles'] != []:
            logger["reponse"] = 200
            print(logger)

            backend_log(logger)
            return data, 200
        else:
            logger["reponse"] = 404
            print(logger)
            return {"status": 404, "message": "No result for query"}, 404

api.add_resource(ArticleV1, '/v1/articles')

# Fixed CORS problem
class ArticleV11(Resource):
    def get(self):
        start_time = time.perf_counter()

        # For backend and end user
        logger = {}
        logger["method"] = request.method
        logger["url"] = request.url
        logger["time"] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        ## Error Handling ##
        # Validate Date
        date_regex = re.compile('^(\d{4})-(\d\d|xx)-(\d\d|xx)T(\d\d|xx):(\d\d|xx):(\d\d|xx)$')
        if not date_regex.search(request.args['start_date']) or not date_regex.search(request.args['end_date']) or request.args['start_date'] > request.args['end_date']:
            logger["runtime"] = runtime(start_time, time.perf_counter())
            logger["reponse"] = 400

            backend_log(logger)
            return {"status": 400, "message": "Invalid Query Parameters (Date)" }, 400, {'Access-Control-Allow-Origin': '*'}

        # Make these parameters optional ???
        if not 'key_term' in request.args or not 'location' in request.args:
            logger["runtime"] = runtime(start_time, time.perf_counter())
            logger["reponse"] = 400

            backend_log(logger)
            return {"status": 400, "message": "Missing Parameter" }, 400, {'Access-Control-Allow-Origin': '*'}

        # n is for the value of article they want to return
        if 'n' in request.args and not request.args['n'].isdigit():
            print("HERE1")
            logger["runtime"] = runtime(start_time, time.perf_counter())
            logger["reponse"] = 400

            backend_log(logger)
            return {"status": 400, "message": "N needs to be number" }, 400, {'Access-Control-Allow-Origin': '*'}

        data = query_and_convert()          # Main function
        logger["runtime"] = runtime(start_time, time.perf_counter())

        if data['articles'] != []:
            logger["reponse"] = 200
            backend_log(logger)
            return data, 200, {'Access-Control-Allow-Origin': '*'}
        else:
            logger["reponse"] = 404
            backend_log(logger)
            return {"status": 404, "message": "No result for query"}, 404, {'Access-Control-Allow-Origin': '*'}

        # return data, 200

api.add_resource(ArticleV11, '/v1.1/articles')

def backend_log(logger):
    f = open("log.txt", "a")
    f.write("{{\"Time\": \"{}\", \"Url\": \"{} {}\", \"Status\": \"{}\", \"Time\": \"{}ms\" }}\n".format(logger['time'], logger['method'], logger["url"], logger["reponse"], logger["runtime"]))
    f.close()

# runtime of API in ms
def runtime(start, end):
    return round(end-start, 5)*1000

def query_and_convert():
    # print(request.args['start_date']) # print(request.args['end_date'])
    # print(request.args['location']) # print(request.args['key_term'])

    with open('output.pickle', 'rb') as p:
        articles = pickle.load(p)

    # TODO IF IMPLEMENT: Number of articles to return: 10
    n = 10
    if 'n' in request.args:
        n = int(request.args['n'])

    json = {}
    json['articles'] = []
    urls = []
    for article in articles:
        dict_article = {}
        # dict_article['id']
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
            dict_location["code"] = location.get_code()
            # print(location.get_country())
            dict_reports["locations"].append(dict_location)
        dict_reports["disease"] = article.get_reports().get_disease()
        dict_reports["syndrome"] = article.get_reports().get_syndrome()
        dict_article['reports'] = dict_reports

        urls.append(article.get_url())
        json['articles'].append(dict_article)

    return json

# Test Function
class HelloWorld(Resource):
    def get(self):
        return {
            "url": "https://www.who.int/csr/don/17-january-2020-novel-coronavirus-japan-exchina/en/",
            "date_of_publication": "2020-01-17 xx:xx:xx",
            "headline": "Novel Coronavirus Japan (ex-China)",
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
        }, 200
api.add_resource(HelloWorld, '/test')

if __name__ == '__main__':
    app.run(debug=True)
