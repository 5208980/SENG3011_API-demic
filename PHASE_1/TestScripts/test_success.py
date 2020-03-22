import pytest
import requests
import json

LOCAL_HOST = "http://127.0.0.1:5000"           # TEST in terminal
HEROKU = "https://api-demic.herokuapp.com"     # TeST on web
VERSION = "v1.1"

def test_success():
    # Test correct use of input parameters
    start_date = "2020-01-01T12:00:00"
    end_date = "2020-02-01T12:00:00"
    location = "Australia"
    key_term = "coronavirus"
    r = requests.get('{}/{}/articles?start_date={}&end_date={}&location={}&key_term={}'.format(LOCAL_HOST, VERSION, start_date, end_date, location, key_term))

    with open('output/test_success_output.json') as f:
        expected = json.load(f)

    print (r.request == "GET")
    assert(r.json() == expected)
    assert(r.ok)
    assert(r.status_code == 200)

test_success()
