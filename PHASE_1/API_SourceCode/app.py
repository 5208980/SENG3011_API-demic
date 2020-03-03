# To run use python3 app.py
# To test open another terminal and curl localhost

from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

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
