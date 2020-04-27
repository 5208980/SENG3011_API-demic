# SENG3011 API-demic Project Overview

This repository is a SENG3011 project. The aim is to collect data about health related articles from different sources to help others analyse and track epidemics. There is also the source code for Covid-Scout, a interactive web application that focuses in helping everyone worldwide with the latest statistics and news about the coronavirus.

## Team Members
- **Aaron** (z5208530)
- **Kevin** (z5214693)
- **Logann** (z5294830)
- **Peter** (z5208980)

## Folders
- **Phase 1**
> Contains the API implementation, Scraper, Database and API Testscripts.
- **Phase 2**
> Contains Webpage.
- **Reports**
> Contains Design Details, Management Information Report, Testing Report and Final Report

## Links

- **API-demic API** ([Docs](http://api-demic.herokuapp.com/)) ([Github](https://github.com/z5208980/SENG3011_API-demic/tree/master/PHASE_1/API_SourceCode)) - An API that extracts new sources from H5N1 and trending health terms
- **Covid-Scout** ([Github](https://github.com/z5208980/SENG3011_API-demic/tree/master/PHASE_2/API_SourceCode)) ([Website](https://covid-scout.herokuapp.com/)) - Responsive web application detailing latest statistics and news on Covid-19 globally and for Australians

## API-demics  API Endpoints
These are API-demics latest versions and endpoints
### GET
[/v1.1/articles?](#GET /v1.1/articles)
[/v1.1/articles/latest?](#GET /v1.1/articles/latest)
[/v1.1/trending](#GET /v1.1/trending)

___

### GET /v1.1/articles
Find articles according to query parameters

**Parameters**

Parameter  | Required | Type | Description
------------- | ------------- | ------------- | -------------
`start_date`  | Required | String (YY-MM-DDTHH&colon;MM&colon;SS) | Start date for query
`end_date`  | Required | String (YY-MM-DDTHH&colon;MM&colon;SS) | End date for query
`location`  | Optional | String | Location that articles will focus on
`key_term`  | Optional | List | List of string with seperator as ,
`limit`  | Optional | Int |  number of new articles to return

**Response**

200
```
{
  "articles": [
    {
      "url": "string",
      "date_of_publication": "string",
      "header": "string",
      "main_text": "string",
      "reports": [
        {
          "event_date": "string",
          "locations": [
            {
              "country": "string",
              "location": "string"
            }
          ],
          "diseases": [
            "string"
          ],
          "syndromes": [
            "string"
          ]
        }
      ]
    }
  ],
  "log": {
    "provider_name": "API-demic",
    "accessed_time": "string",
    "amount_of_articles": "string",
    "response_time": "string"
  }
}
```

400
```
{
  "status": 400,
  "message": "Invalid Query Parameters (Date)"
}
```

404
```
{
  "status": 404,
  "message": "No result for query"
}
```

### GET /v1.1/articles/latest
Find the latest articles on certain topics

**Parameters**

Parameter  | Required | Type | Description
------------- | ------------- | ------------- | -------------
`on`  | Required | List | List of string to search on, seperator as ,

**Response**

200
```
{
  "articles": [
    {
      "url": "string",
      "date_of_publication": "string",
      "header": "string",
      "main_text": "string",
      "reports": [
        {
          "event_date": "string",
          "locations": [
            {
              "country": "string",
              "location": "string"
            }
          ],
          "diseases": [
            "string"
          ],
          "syndromes": [
            "string"
          ]
        }
      ]
    }
  ],
  "log": {
    "provider_name": "API-demic",
    "accessed_time": "string",
    "amount_of_articles": "string",
    "response_time": "string"
  }
}
```

400
```
{
  "status": 400,
  "message": "Invalid Query Search Term: On Args",
  "search_list": [
    {
      "term": "string"
    },
  ]
}
```

404
```
{
  "status": 404,
  "message": "No result for query",
  "search_list": [
    {
      "term": "string"
    },
  ]
}
```

### GET /v1.1/trending
Find search phrases most used by others

**Response**

200

```
{
  "trending_terms": [
    "string"
  ],
  "log": {
    "provider_name": "API-demic",
    "accessed_time": "string",
    "amount_of_articles": "string",
    "response_time": "string"
  }
}
```

## Running the Covid-Scout locally
If you want to host the site for viewing, then you need
- Python
- Pip
- Virtualenv

```
   $ git clone https://github.com/z5208980/SENG3011_API-demic.git
   $ cd PHASE_2/API_SourceCode
   $ source venv/bin/activate
   $ pip3 install -r requirements.txt
   $ python3 app.py
```
http://localhost:8000/

### APIs and Dataset
- ([API-demic](http://api-demic.herokuapp.com/)) - Main source for new articles (Our API)
- ([Sixtyhww](http://api.sixtyhww.com:3000/)) - SENG3011 Team API for news articles
- ([Thevirustracker](https://api.thevirustracker.com/free-api?global=stats)) - Covid-19 latest updates (Used as widget)


- ([CSSEGISandData](https://github.com/CSSEGISandData/COVID-19)) - Dataset for Covid-19 globally
- ([Data.NSW](https://data.nsw.gov.au/)) - Dataset for latest Covid-19 positive in NSW
- ([The Guardian](https://interactive.guim.co.uk/docsdata/1q5gdePANXci8enuiS4oHUJxcxC13d6bjMRSicakychE.json)) - Dataset for Australia Covid-19 statistics by states
- ([Pomber](https://pomber.github.io/covid19/timeseries.json)) - Dataset for latest Covid-19 cases by country in timeseries
