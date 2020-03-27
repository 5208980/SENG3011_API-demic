import pytest
import requests
import json
import time

from version import *

# performance for one day
def test_api_one_day():
    start_date = "2020-02-01T23:59:59"
    end_date = "2020-02-02T23:59:59"
    location = "Australia"
    key_term = "coronavirus"

    start = time.perf_counter()
    r = requests.get('{}?start_date={}&end_date={}&location={}&key_term={}'.format(URL, start_date, end_date, location, key_term))
    end = time.perf_counter()

    assert(end-start <= 0.15)
    assert(r.request.method == "GET")
    assert(len(r.json()['articles']) == 1)
    assert(r.ok)
    assert(r.status_code == 200)

# performance for one week
def test_api_one_week():
    start_date = "2020-02-01T23:59:59"
    end_date = "2020-02-08T23:59:59"
    location = "Australia"
    key_term = "coronavirus"

    start = time.perf_counter()
    r = requests.get('{}?start_date={}&end_date={}&location={}&key_term={}'.format(URL, start_date, end_date, location, key_term))
    end = time.perf_counter()

    assert(end-start <= 0.15)
    assert(r.request.method == "GET")
    assert(len(r.json()['articles']) == 6)
    assert(r.ok)
    assert(r.status_code == 200)

# performance for one month
def test_api_one_month():
    start_date = "2020-01-01T23:59:59"
    end_date = "2020-02-01T23:59:59"
    location = "Australia"
    key_term = "coronavirus"

    start = time.perf_counter()
    r = requests.get('{}?start_date={}&end_date={}&location={}&key_term={}'.format(URL, start_date, end_date, location, key_term))
    end = time.perf_counter()

    assert(end-start <= 0.15)
    assert(r.request.method == "GET")
    assert(len(r.json()['articles']) == 6)
    assert(r.ok)
    assert(r.status_code == 200)


# test_api_one_day()
# test_api_one_week()
# test_api_one_month()
