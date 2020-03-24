from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_swagger_ui import get_swaggerui_blueprint    # Swagger UI
from database import db
import re                                               # For regex
import datetime
import json
import os
import pickle
import time
from database import Article, Report, Location
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

os.environ['DATABASE_URL'] = 'https://data.heroku.com/datastores/21dc3eb7-162b-4505-bbbe-850727c5b24a#administration'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']

api = Api(app)
db.init_app(app)

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
            exe_end_time = time.perf_counter()
            logger["runtime"] = round(exe_end_time - exe_start_time, 2)
            logger["reponse"] = 400

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
        date_regex = re.compile('^(\d{4})-(\d\d|xx)-(\d\d|xx)T(\d\d|xx):(\d\d|xx):(\d\d|xx)$')

        start_date, end_date = validate_date(request.args['start_date'], request.args['end_date'])

        if not date_regex.search(start_date) or not date_regex.search(end_date) or start_date >= end_date:
            logger["runtime"] = runtime(start_time, time.perf_counter())
            logger["reponse"] = 400

            backend_log(logger)
            return {"status": 400, "message": "Invalid Query Parameters (Date)" }, 400, {'Access-Control-Allow-Origin': '*'}

        # limit is for the value of article they want to return
        if 'limit' in request.args and not request.args['limit'].isdigit():
            logger["runtime"] = runtime(start_time, time.perf_counter())
            logger["reponse"] = 400

            backend_log(logger)
            return {"status": 400, "message": "limit needs to be number" }, 400, {'Access-Control-Allow-Origin': '*'}

        ## Create json
        json = query_and_convert(start_date, end_date)          # Main function
        logger["runtime"] = runtime(start_time, time.perf_counter())

        if json['articles'] != []:
            logger["reponse"] = 200
            backend_log(logger)
            return json, 200, {'Access-Control-Allow-Origin': '*'}
        else:
            logger["reponse"] = 404
            backend_log(logger)
            return {"status": 404, "message": "No result for query"}, 404, {'Access-Control-Allow-Origin': '*'}

api.add_resource(ArticleV11, '/v1.1/articles')

## Helper Functions ##

def validate_date(start_date, end_date):
    # start month = xx then change to 01
    if start_date[5:7] == 'xx':
        start_date = start_date[0:5] + '01' + start_date[7:19]

    # start day = xx change to 01
    if start_date[8:10] == 'xx':
        start_date = start_date[0:8] + '01' + start_date[10:19]

    # start hour = xx change to 00
    if start_date[11:13] == 'xx':
        start_date = start_date[0:11] + '00' + start_date[13:19]

    # start minute = xx change to 00
    if start_date[14:16] == 'xx':
        start_date = start_date[0:14] + '00' + start_date[16:19]

    # start second = xx change to 00
    if start_date[17:19] == 'xx':
        start_date = start_date[0:17] + '00'


    end_date = request.args['end_date']

    # end month = xx then change to 12
    if end_date[5:7] == 'xx':
        end_date = end_date[0:5] + '12' + end_date[7:19]

    # end day = xx change to 30 or 31
    if end_date[8:10] == 'xx':
        month = end_date[5:7]

        def day(m):
            switcher={
                '01':'31',
                '02':'28',
                '03':'31',
                '04':'30',
                '05':'31',
                '06':'30',
                '07':'31',
                '08':'31',
                '09':'30',
                '10':'31',
                '11':'30',
                '12':'31'
            }
            return switcher.get(m,"30")

        day = day(month)

        if end_date[0:4] != 'xxxx':
            if int(end_date[0:4]) % 4 == 0 and day == '28':
                day = '29'

        end_date = end_date[0:8] + day + end_date[10:19]

    # end hour = xx change to 00
    if end_date[11:13] == 'xx':
        end_date = end_date[0:11] + '23' + end_date[13:19]

    # end minute = xx change to 00
    if end_date[14:16] == 'xx':
        end_date = end_date[0:14] + '59' + end_date[16:19]

    # end second = xx change to 00
    if end_date[17:19] == 'xx':
        end_date = end_date[0:17] + '59'

    return (start_date, end_date)

def query_and_convert(start, end):
    # print(request.args['start_date']) # print(request.args['end_date'])
    # print(request.args['location']) # print(request.args['key_term'])

    start_date = datetime.datetime.strptime(start, '%Y-%m-%dT%H:%M:%S')
    end_date = datetime.datetime.strptime(end, '%Y-%m-%dT%H:%M:%S')
    limit = int(request.args['limit']) if 'limit' in request.args else 1000     # threshold: 1000

    exist_location_parameter = True if 'location' in request.args else False
    exist_key_terms_parameter = False
    if 'key_term' in request.args:
        exist_key_terms_parameter = True
        key_terms = request.args['key_term'].lower().split(',')
        print(key_terms)

    with open('output.pickle', 'rb') as p:
        articles = pickle.load(p)           # 1273 articles

    json = {}
    json['articles'] = []
    counter = 0;
    for article in articles:
        if counter >= limit:
            break
        date_of_publication = datetime.datetime.strptime(article.get_date_of_publication(), '%Y-%m-%d %H:%M:%S')

        if date_of_publication >= start_date and date_of_publication <= end_date:   # Date Query
            if exist_location_parameter and not exist_key_terms_parameter:           # check location only
                if query_location(article):
                    json['articles'].append(jsonify(article))
                    counter+=1
            elif not exist_location_parameter and exist_key_terms_parameter:         # check key_terms only
                if query_key_terms(article):
                    json['articles'].append(jsonify(article))
                    counter+=1
            elif exist_location_parameter and exist_key_terms_parameter:             # check both
                print(query_location(article))
                if query_location(article) and query_key_terms(article):
                    json['articles'].append(jsonify(article))
                    counter+=1
            else:
                json['articles'].append(jsonify(article))
                counter+=1

    # SO DONE WITH PSYCOPG2
    # articles = Article.query.filter(Article.date_of_publication >= start)
    # print(articles)

    # if exist_location_parameter and not exist_key_terms_parameter:           # check location only
    #     # articles = Article.query.filter(and_(Article.date_of_publication >= start, Article.date_of_publication >= end))
    # elif not exist_location_parameter and exist_key_terms_parameter:         # check key_terms only
    #     # articles = Article.query.filter(and_(Article.date_of_publication >= start, Article.date_of_publication >= end))
    # elif exist_location_parameter and exist_key_terms_parameter:             # check both
    #     # articles = Article.query.filter(and_(Article.date_of_publication >= start, Article.date_of_publication >= end))
    # else:
    #     # articles = Article.query.filter(and_(Article.date_of_publication >= start, Article.date_of_publication >= end))

    return json

def jsonify(article):
    dict_article = {}
    dict_article['url'] = article.get_url()
    dict_article['date_of_publication'] = article.get_date_of_publication()
    dict_article['headline'] = article.get_headline()
    dict_article['main_text'] = article.get_main_text()
    dict_article['key_terms'] = article.get_key_terms()

    dict_reports = {}
    dict_reports["event_date"] = article.get_reports().get_event_date()
    dict_reports["locations"] = []
    for location in article.get_reports().get_locations():
        dict_location = {}
        dict_location["country"] = location.get_country()
        dict_location["location"] = location.get_location()
        dict_location["code"] = location.get_code()
        dict_reports["locations"].append(dict_location)
    dict_reports["disease"] = article.get_reports().get_disease()
    dict_reports["syndrome"] = article.get_reports().get_syndrome()
    dict_article['reports'] = dict_reports

    return dict_article

def query_location(article):
    location_query = request.args['location'].lower()
    location_exist = False
    for location in article.get_reports().get_locations():
        if location.get_country().lower() == location_query or location.get_country().lower() == location_query:
            location_exist = True;
    return location_exist

def query_key_terms(article):
    key_terms = request.args['key_term'].lower().split(',')
    key_terms_exist = False
    for key_term in key_terms:
        if key_term.lower() in article.get_main_text().lower():
            key_terms_exist = True;

    return key_terms_exist

# runtime of API in ms
def runtime(start, end):
    return round(end-start, 5)*1000

def backend_log(logger):
    f = open("log.txt", "a")
    f.write("{{\"Time\": \"{}\", \"Url\": \"{} {}\", \"Status\": \"{}\", \"Time\": \"{}ms\" }}\n".format(logger['time'], logger['method'], logger["url"], logger["reponse"], logger["runtime"]))
    f.close()

if __name__ == '__main__':
    app.run(debug=True)
