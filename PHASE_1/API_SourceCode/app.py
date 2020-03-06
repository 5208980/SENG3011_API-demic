# To run use python3 app.py
# To test open another terminal and curl localhost

from flask import Flask, request
from flask_restful import Resource, Api, reqparse

import re                    # For regex
import datetime
import json

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

        # Error Handling and Logging Status
        date_regex = re.compile('^(\d{4})-(\d\d|xx)-(\d\d|xx)T(\d\d|xx):(\d\d|xx):(\d\d|xx)$')
        if not ( date_regex.match(request.args['start_date']) or date_regex.match(request.args['start_date']) ):
            # Maybe print file error msg, not sure
            info("success")
            return {"status": 400, "message": "Invalid Query Parameters" }, 400

        info(request.url)

        # DB Query
        with open('sample.json') as data_file:
            data = json.load(data_file)

        return data, 200
api.add_resource(Article, '/articles')

# File Log: Should I create a logger class?
# Note: There can be two types of logs for your API- You can return a json snippet
# with your API response to the end user, which includes the details such as team
# name, accessed time, data source. Also you can keep a log file in back-end that
# contain details such as which API end point was accessed at what time, how long
# it took to address the request, resource utilization etc. that are useful for
# API monitoring and performance improvement.
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
