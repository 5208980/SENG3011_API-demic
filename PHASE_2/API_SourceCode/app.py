from flask import Flask, render_template
from covid19 import *
import re
from datetime import datetime
import json

app = Flask(__name__)

@app.route("/")
def home():
    # response = requests.get("http://127.0.0.1:5000/v1.1/articles?start_date=2020-01-01T12:00:00&end_date=2020-02-01T10:00:00&location=australia&key_term=coronavirus")
    # print(response.json())
    # Fetch API will be called in JAVASCRIPT NOT PYTHON LIKE ABOVE

    return render_template("index.html")

@app.route("/covid19")
def covid19():
    # https://api.covid19api.com/
    data = json.dumps(generate_data())

    s = str(data)
    s = re.sub('\'', '\"', s)
    s = re.sub('[a-zA-Z]\,', '', s)
    s = re.sub('[a-zA-Z]\"[a-zA-Z]', '', s)

    return render_template("covid.html", data=s)

@app.route("/news")
def latest_news():
    data = json.dumps(head_generate_data())
    total = generate_total()

    data_str = json_to_string(data)
    total_str = json_to_string(total)

    x = datetime.now()
    
    END = x.strftime("%Y") + "-" + x.strftime("%m") + "-" + x.strftime("%d") + "T" + x.strftime("%T")

    START = ""
    if int(x.strftime("%m")) == 1:
        START = str(int(x.strftime("%Y")) - 1) + "-12-" + x.strftime("%d") + "T" + x.strftime("%T")
    elif int(x.strftime("%m")) < 11:
        START = x.strftime("%Y") + "-0" + str(int(x.strftime("%m")) - 1) + "-" + x.strftime("%d") + "T" + x.strftime("%T")
    else:
        START = x.strftime("%Y") + "-" + str(int(x.strftime("%m")) - 1) + "-" + x.strftime("%d") + "T" + x.strftime("%T")

    return render_template("news.html", data=data_str, total=total_str, start = START, end = END) # Render News on covid this week

@app.route("/news/<date>")
def date_news(date):
    if not validate_date(date):
        return render_template("about.html")

    data = json.dumps(head_generate_data())
    data_str = json_to_string(data)

    return render_template("news.html", start_date=date+"T00:00:01", end_date=date+"T23:59:59", data=data_str)

@app.route("/info")
def info():

    data = json.dumps(head_generate_data())
    data_str = json_to_string(data)
    return render_template("infography.html", data=data_str)

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True, port=8000)
