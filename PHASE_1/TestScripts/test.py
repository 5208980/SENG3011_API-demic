# import pytest

import requests

LOCAL_HOST = "http://127.0.0.1:5000/"           # TEST in terminal
HEROKU = "https://api-demic.herokuapp.com/"     # TeST on web


# Test correct use of input parameters
start_date = "2020-01-01 12:00:00"
end_date = "2020-02-01 12:00:00"
r = requests.get('{}articles?start_date={}&end_date={}&location=australia&key_term=coronavirus.'.format(LOCAL_HOST, start_date, end_date))
assert(r.status_code == 200)
# print(r.json())

for j in r.json()['articles']:
    print("$#%%#$%#")
    print(j['date_of_publication'])


# Test incorrect use of date format in Start date
start_date = "202-01-01 12:00:00"
end_date = "2020-02-01 12:00:00"
r = requests.get('{}/articles?start_date={}&end_date={}&location=australia&key_term=coronavirus.'.format(LOCAL_HOST,  start_date, end_date))
assert(r.status_code == 400)

# Test correct use of date format with day and time not filled in
start_date = "2020-01-xx xx:xx:xx"
end_date = "2020-02-xx xx:xx:xx"
r = requests.get('{}/articles?start_date={}&end_date={}&location=australia&key_term=coronavirus.'.format(LOCAL_HOST,  start_date, end_date))
assert(r.status_code == 200)

# Test correct use of date format with day and time not filled in for start date but end date day filled in
start_date = "2020-01-xx xx:xx:xx"
end_date = "2020-02-01 xx:xx:xx"
r = requests.get('{}/articles?start_date={}&end_date={}&location=australia&key_term=coronavirus.'.format(LOCAL_HOST,  start_date, end_date))
assert(r.status_code == 200)

# Test correct use of date format with day and time not filled in for end date but start date day filled in
start_date = "2020-01-01 xx:xx:xx"
end_date = "2020-02-xx xx:xx:xx"
r = requests.get('{}/articles?start_date={}&end_date={}&location=australia&key_term=coronavirus.'.format(LOCAL_HOST,  start_date, end_date))
assert(r.status_code == 200)

# Test incorrect correct use of date format with day and time not filled in for start date but end date having month not filled in as well
start_date = "2020-01-xx xx:xx:xx"
end_date = "2020-xx-xx xx:xx:xx"
r = requests.get('{}/articles?start_date={}&end_date={}&location=australia&key_term=coronavirus.'.format(LOCAL_HOST,  start_date, end_date))
assert(r.status_code == 400)

# Test Start date year more than end date yer
start_date = "2021-01-xx xx:xx:xx"
end_date = "2020-01-xx xx:xx:xx"
r = requests.get('{}/articles?start_date={}&end_date={}&location=australia&key_term=coronavirus.'.format(LOCAL_HOST,  start_date, end_date))
assert(r.status_code == 400)

# Test Start date year more than end date yer
start_date = "2021-01-xx xx:xx:xx"
end_date = "2021-xx-xx xx:xx:xx"
r = requests.get('{}/articles?start_date={}&end_date={}&location=australia&key_term=coronavirus.'.format(LOCAL_HOST,  start_date, end_date))
assert(r.status_code == 400)

# Test Start date year more than end date yer
start_date = "2021-01-xx xx:xx:xx"
end_date = "2021-01-xx xx:xx:xx"
r = requests.get('{}/articles?start_date={}&end_date={}&location=australia&key_term=coronavirus.'.format(LOCAL_HOST,  start_date, end_date))
assert(r.status_code == 400)