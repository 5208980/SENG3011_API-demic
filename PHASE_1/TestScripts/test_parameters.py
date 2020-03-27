import pytest
import requests
import json

from version import *

# start_date parameter not present
def test_no_start_date_param():
    start_date ='2020-01-10T12:00:00'
    location ='australia'
    key_term ='coronavirus'

    r = requests.get('{}?&end_date={}&location={}&key_term={}'.format(URL, start_date, location, key_term))

    assert(r.request.method == "GET")
    assert(not r.ok)
    assert(r.status_code == 400)

# end_date parameter not present
def test_no_end_date_param():
    end_date ='2020-01-10T12:00:00'
    location ='australia'
    key_term ='coronavirus'

    r = requests.get('{}?&end_date={}&location={}&key_term={}'.format(URL, end_date, location, key_term))

    assert(r.request.method == "GET")
    assert(not r.ok)
    assert(r.status_code == 400)

# location parameter not present
def test_no_location_param():
    start_date = '2020-01-01T12:00:00'
    end_date ='2020-01-10T12:00:00'
    key_term ='coronavirus'

    r = requests.get('{}?start_date={}&end_date={}&key_term={}'.format(URL, start_date, end_date, key_term))

    with open('output_param/test_no_location_param.json') as f:
        expected = json.load(f)

    assert(r.request.method == "GET")
    assert(r.ok)
    assert(r.status_code == 200)
    assert(r.json() == expected)

# key_term parameter not present
def test_no_key_term_param():
    start_date = '2020-01-01T12:00:00'
    end_date ='2020-01-10T12:00:00'
    location ='australia'

    r = requests.get('{}?start_date={}&end_date={}&location={}'.format(URL, start_date, end_date, location))

    with open('output_param/test_no_key_term_param.json') as f:
        expected = json.load(f)

    assert(r.request.method == "GET")
    assert(r.ok)
    assert(r.status_code == 200)
    assert(r.json() == expected)

# no location or key_term param
def test_no_location_key_term_param():
    start_date = '2020-01-01T12:00:00'
    end_date ='2020-01-10T12:00:00'

    r = requests.get('{}?start_date={}&end_date={}'.format(URL, start_date, end_date))

    with open('output_param/test_no_location_key_term_param.json') as f:
        expected = json.load(f)

    assert(r.request.method == "GET")
    assert(r.ok)
    assert(r.status_code == 200)
    assert(r.json() == expected)

    # urls with param needs to be subset of url without params
    with open('output_param/test_no_key_term_param.json') as f:
        subset = json.load(f)
    assert(len(r.json()['articles']) >= len(subset['articles']))

    with open('output_param/test_no_location_param.json') as f:
        subset = json.load(f)
    assert(len(r.json()['articles']) >= len(subset['articles']))

# no param
def test_no_param():
    r = requests.get('{}'.format(URL))

    with open('output_param/test_no_location_key_term_param.json') as f:
        expected = json.load(f)

    assert(r.request.method == "GET")
    assert(not r.ok)
    assert(r.status_code == 400)

test_no_start_date_param()
test_no_end_date_param()
test_no_location_param()
test_no_key_term_param()
test_no_location_key_term_param()
test_no_param()
