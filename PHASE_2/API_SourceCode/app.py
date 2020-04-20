from flask import Flask, render_template
from covid19 import *
import re
from datetime import datetime
import json

app = Flask(__name__)

@app.route("/")
def home():
    total_str = json_to_string(generate_total())

    return render_template("index.html", total=total_str)

@app.route("/dashboard")
def dashboard():

    return render_template("dashboard.html")

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

@app.route("/au")
def au():
    nsw, nsw_latest_cases = nsw_positive_cases()
    nsw = json_to_string(nsw)
    nsw_latest_cases = json_to_string(nsw_latest_cases)

    wa = wa_positive_cases()
    wa = json_to_string(wa)

    vic = vic_positive_cases()
    vic = json_to_string(vic)

    qld = qld_positive_cases()
    qld = json_to_string(qld)

    au, sources = australia_latest()
    au = json_to_string(au)
    sources = json_to_string(sources)

    return render_template("au.html", sources=sources, nsw_latest_cases=nsw_latest_cases, au=au, nsw=nsw, wa=wa, vic=vic, qld=qld)

@app.route("/wa")
def wa():
    data = wa_positive_cases()
    data_str = json_to_string(data)

    return render_template("wa.html", data=data_str)

if __name__ == "__main__":
    app.run(debug=True, port=8000)
