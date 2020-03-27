import pytest
import requests
import json

from version import *

def test_success():
    PARAMS = {
        "start_date": "2020-01-01T12:00:00",
        "end_date": "2020-02-01T12:00:00",
        "location": "Australia",
        "key_term": "coronavirus"
    }

    r = requests.get(url = URL, params = PARAMS)

    with open('output_response/test_success_output.json') as f:
        expected = json.load(f)

    assert(r.request.method == "GET")
    assert(r.ok)
    assert(r.status_code == 200)
    assert(r.json() == expected)

def test_incorrect_use_fail():
    # Test incorrect use of input parameters
    start_date = "20-01-01T12:00:00"
    end_date = "2020-02-01T12:00:00"
    location = "Australia"
    key_term = "coronavirus"
    r = requests.get('{}?start_date={}&end_date={}&location={}&key_term={}'.format(URL, start_date, end_date, location, key_term))

    with open('output_response/test_incorrect_use_fail_output.json') as f:
        expected = json.load(f)

    assert(r.request.method == "GET")
    assert(not r.ok)
    assert(r.status_code == 400)
    assert(r.json() == expected)

def test_end_earlier_fail():
    # end_date earlier than start_date
    start_date = "2020-02-01T12:00:00"
    end_date = "2020-01-01T12:00:00"
    location = "Australia"
    key_term = "coronavirus"
    r = requests.get('{}?start_date={}&end_date={}&location={}&key_term={}'.format(URL, start_date, end_date, location, key_term))

    with open('output_response/test_end_earlier_fail_output.json') as f:
        expected = json.load(f)

    assert(r.request.method == "GET")
    assert(not r.ok)
    assert(r.status_code == 400)
    assert(r.json() == expected)


def test_success_with_x():
    # dates filled with some x's
    start_date = "2020-01-xxTxx:xx:xx"
    end_date = "2020-02-xxTxx:xx:xx"
    location = "Australia"
    key_term = "coronavirus"
    r = requests.get('{}?start_date={}&end_date={}&location={}&key_term={}'.format(URL, start_date, end_date, location, key_term))

    with open('output_response/test_success_with_x_output.json') as f:
        expected = json.load(f)

    assert(r.request.method == "GET")
    assert(r.ok)
    assert(r.status_code == 200)
    assert(r.json() == expected)


def test_incorrect_location_fail():
    # incorrect location zoo used
    start_date = "2020-01-xxTxx:xx:xx"
    end_date = "2020-02-xxTxx:xx:xx"
    location = "zoo"
    key_term = "coronavirus"
    r = requests.get('{}?start_date={}&end_date={}&location={}&key_term={}'.format(URL, start_date, end_date, location, key_term))

    with open('output_response/test_incorrect_location_fail_output.json') as f:
        expected = json.load(f)

    assert(r.request.method == "GET")
    assert(not r.ok)
    assert(r.status_code == 404)
    assert(r.json() == expected)

def test_incorrect_key_term_fail():
    # incorrect key_term
    start_date = "2020-01-xxTxx:xx:xx"
    end_date = "2020-02-xxTxx:xx:xx"
    location = "Australia"
    key_term = "cooties"
    r = requests.get('{}?start_date={}&end_date={}&location={}&key_term={}'.format(URL, start_date, end_date, location, key_term))

    with open('output_response/test_incorrect_key_term_fail_output.json') as f:
        expected = json.load(f)

    assert(r.request.method == "GET")
    assert(not r.ok)
    assert(r.status_code == 404)
    assert(r.json() == expected)

def test_multiple_terms_success():
    # Use of multiple terms for key_terms
    start_date = "2020-01-xxTxx:xx:xx"
    end_date = "2020-02-xxTxx:xx:xx"
    location = "Australia"
    key_term = "Anthrax,Zika"
    r = requests.get('{}?start_date={}&end_date={}&location={}&key_term={}'.format(URL, start_date, end_date, location, key_term))

#    with open('output_response/test_success_with_x_output.json') as f:
#        expected = json.load(f)

#    print (r.request == "GET")
#    assert(r.json() == expected)
#    assert(r.ok)
#    assert(r.status_code == 200)


def test_ambiguous_success():
    # testing ambiguous case
    start_date = "2020-01-03Txx:xx:xx"
    end_date = "2020-01-xxTxx:xx:xx"
    location = "Australia"
    key_term = "Coronavirus"
    r = requests.get('{}?start_date={}&end_date={}&location={}&key_term={}'.format(URL, start_date, end_date, location, key_term))

    with open('output_response/test_ambiguous_success_output.json') as f:
        expected = json.load(f)

    assert(r.request.method == "GET")
    assert(r.ok)
    assert(r.status_code == 200)
    assert(r.json() == expected)

def test_all_x():
    # using all x's
    start_date = "xxxx-xx-xxTxx:xx:xx"
    end_date = "xxxx-xx-xxTxx:xx:xx"
    location = "Australia"
    key_term = "Coronavirus"
    r = requests.get('{}?start_date={}&end_date={}&location={}&key_term={}'.format(URL, start_date, end_date, location, key_term))

    with open('output_response/test_all_x_output.json') as f:
        expected = json.load(f)

    assert(r.request.method == "GET")
    assert(not r.ok)
    assert(r.status_code == 400)
    assert(r.json() == expected)

def test_start_year_higher():
    # start year higher than end year
    start_date = "2021-01-03Txx:xx:xx"
    end_date = "2020-01-xxTxx:xx:xx"
    location = "Australia"
    key_term = "Coronavirus"
    r = requests.get('{}?start_date={}&end_date={}&location={}&key_term={}'.format(URL, start_date, end_date, location, key_term))

    with open('output_response/test_start_year_higher_output.json') as f:
        expected = json.load(f)

    assert(r.request.method == "GET")
    assert(not r.ok)
    assert(r.status_code == 400)
    assert(r.json() == expected)

def test_start_time_higher():
    # start time higher than end time
    start_date = "2021-01-03T04:00:00"
    end_date = "2021-01-03T03:00:00"
    location = "Australia"
    key_term = "Coronavirus"
    r = requests.get('{}?start_date={}&end_date={}&location={}&key_term={}'.format(URL, start_date, end_date, location, key_term))

    with open('output_response/test_start_time_higher_output.json') as f:
        expected = json.load(f)

    assert(r.request.method == "GET")
    assert(not r.ok)
    assert(r.status_code == 400)
    assert(r.json() == expected)

def test_success_by_few_hours():
    # success by few hours
    start_date = "2020-01-21T03:00:00"
    end_date = "2020-01-21T23:00:00"
    location = "Australia"
    key_term = "Coronavirus"
    r = requests.get('{}?start_date={}&end_date={}&location={}&key_term={}'.format(URL, start_date, end_date, location, key_term))

    with open('output_response/test_success_by_few_hours_output.json') as f:
        expected = json.load(f)

    assert(r.request.method == "GET")
    assert(r.ok)
    assert(r.status_code == 200)
    assert(r.json() == expected)

def test_success_year_only():
    # yeasrs used only
    start_date = "2020-xx-xxTxx:xx:xx"
    end_date = "2021-xx-xxTxx:xx:xx"
    location = "Australia"
    key_term = "Coronavirus"
    r = requests.get('{}?start_date={}&end_date={}&location={}&key_term={}'.format(URL, start_date, end_date, location, key_term))

    with open('output_response/test_success_year_only_output.json') as f:
        expected = json.load(f)

    assert(r.request.method == "GET")
    assert(r.ok)
    assert(r.status_code == 200)
    assert(r.json() == expected)

def test_same_date_fail():
    # Use same date
    start_date = "2020-01-01T12:00:00"
    end_date = "2020-01-01T12:00:00"
    location = "Australia"
    key_term = "Coronavirus"
    r = requests.get('{}?start_date={}&end_date={}&location={}&key_term={}'.format(URL, start_date, end_date, location, key_term))

    with open('output_response/test_same_date_fail_output.json') as f:
        expected = json.load(f)

    assert(r.request.method == "GET")
    assert(not r.ok)
    assert(r.status_code == 400)
    assert(r.json() == expected)

def test_same_year_success():
    # use same year
    start_date = "2020-xx-xxTxx:xx:xx"
    end_date = "2020-xx-xxTxx:xx:xx"
    location = "Australia"
    key_term = "Coronavirus"
    r = requests.get('{}?start_date={}&end_date={}&location={}&key_term={}'.format(URL, start_date, end_date, location, key_term))

    with open('output_response/test_same_year_success_output.json') as f:
        expected = json.load(f)

    assert(r.request.method == "GET")
    assert(r.ok)
    assert(r.status_code == 200)
    assert(r.json() == expected)


test_success()
test_incorrect_use_fail()
test_end_earlier_fail()
test_success_with_x()
test_incorrect_location_fail()
test_incorrect_key_term_fail()
test_multiple_terms_success()
test_ambiguous_success()
test_all_x()
test_start_year_higher()
test_start_time_higher()
test_success_by_few_hours()
test_success_year_only()
test_same_date_fail()
test_same_year_success()
