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

 #   print (r.request == "GET")
    assert(r.json() == expected)
    assert(r.ok)
    assert(r.status_code == 200)

def test_incorrect_use_fail():
    # Test incorrect use of input parameters
    start_date = "20-01-01T12:00:00"
    end_date = "2020-02-01T12:00:00"
    location = "Australia"
    key_term = "coronavirus"
    r = requests.get('{}/{}/articles?start_date={}&end_date={}&location={}&key_term={}'.format(LOCAL_HOST, VERSION, start_date, end_date, location, key_term))

    with open('output/test_incorrect_use_fail_output.json') as f:
        expected = json.load(f)

#    print (r.request == "GET")
    assert(r.json() == expected)
  #  assert(r.notok)
    assert(r.status_code == 400)

def test_end_earlier_fail():
    # end_date earlier than start_date
    start_date = "2020-02-01T12:00:00"
    end_date = "2020-01-01T12:00:00"
    location = "Australia"
    key_term = "coronavirus"
    r = requests.get('{}/{}/articles?start_date={}&end_date={}&location={}&key_term={}'.format(LOCAL_HOST, VERSION, start_date, end_date, location, key_term))

    with open('output/test_end_earlier_fail_output.json') as f:
        expected = json.load(f)

 #   print (r.request == "GET")
    assert(r.json() == expected)
 #   assert(r.ok)
    assert(r.status_code == 400)


def test_success_with_x():
    # Test correct use of input parameters
    start_date = "2020-01-xxTxx:xx:xx"
    end_date = "2020-02-xxTxx:xx:xx"
    location = "Australia"
    key_term = "coronavirus"
    r = requests.get('{}/{}/articles?start_date={}&end_date={}&location={}&key_term={}'.format(LOCAL_HOST, VERSION, start_date, end_date, location, key_term))

    with open('output/test_success_with_x_output.json') as f:
        expected = json.load(f)

#    print (r.request == "GET")
    assert(r.json() == expected)
    assert(r.ok)
    assert(r.status_code == 200)


def test_incorrect_location_fail():
    # Test correct use of input parameters
    start_date = "2020-01-xxTxx:xx:xx"
    end_date = "2020-02-xxTxx:xx:xx"
    location = "zoo"
    key_term = "coronavirus"
    r = requests.get('{}/{}/articles?start_date={}&end_date={}&location={}&key_term={}'.format(LOCAL_HOST, VERSION, start_date, end_date, location, key_term))

    with open('output/test_incorrect_location_fail_output.json') as f:
        expected = json.load(f)

#    print (r.request == "GET")
    assert(r.json() == expected)
#    assert(r.ok)
    assert(r.status_code == 404)

def test_incorrect_key_term_fail():
    # Test correct use of input parameters
    start_date = "2020-01-xxTxx:xx:xx"
    end_date = "2020-02-xxTxx:xx:xx"
    location = "Australia"
    key_term = "cooties"
    r = requests.get('{}/{}/articles?start_date={}&end_date={}&location={}&key_term={}'.format(LOCAL_HOST, VERSION, start_date, end_date, location, key_term))

    with open('output/test_incorrect_key_term_fail_output.json') as f:
        expected = json.load(f)

#    print (r.request == "GET")
    assert(r.json() == expected)
#    assert(r.ok)
    assert(r.status_code == 404)

def test_multiple_terms_success():
    # Test correct use of input parameters
    start_date = "2020-01-xxTxx:xx:xx"
    end_date = "2020-02-xxTxx:xx:xx"
    location = "Australia"
    key_term = "Anthrax,Zika"
    r = requests.get('{}/{}/articles?start_date={}&end_date={}&location={}&key_term={}'.format(LOCAL_HOST, VERSION, start_date, end_date, location, key_term))

#    with open('output/test_success_with_x_output.json') as f:
#        expected = json.load(f)

#    print (r.request == "GET")
#    assert(r.json() == expected)
#    assert(r.ok)
#    assert(r.status_code == 200)


def test_ambiguous_success():
    # Test correct use of input parameters
    start_date = "2020-01-03Txx:xx:xx"
    end_date = "2020-01-xxTxx:xx:xx"
    location = "Australia"
    key_term = "Coronavirus"
    r = requests.get('{}/{}/articles?start_date={}&end_date={}&location={}&key_term={}'.format(LOCAL_HOST, VERSION, start_date, end_date, location, key_term))

    with open('output/test_ambiguous_success_output.json') as f:
        expected = json.load(f)

#    print (r.request == "GET")
    assert(r.json() == expected)
    assert(r.ok)
    assert(r.status_code == 200)


test_success()
test_incorrect_use_fail()
test_end_earlier_fail()
test_success_with_x()
test_incorrect_location_fail()
test_incorrect_key_term_fail()
test_multiple_terms_success()