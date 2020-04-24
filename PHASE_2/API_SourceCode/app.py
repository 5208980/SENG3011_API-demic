from flask import Flask, render_template, request
from covid19 import *
import re
from datetime import datetime
import json

app = Flask(__name__)

@app.route("/")
def home():
    advices = generateSafetyAdvices()
    advices = json_to_string(advices)

    return render_template("index.html", advices=advices)

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

@app.route("/news", methods=['GET'])
def latest_news():
    # data = json.dumps(head_generate_data())
    # total = generate_total()
    #
    # data_str = json_to_string(data)
    # total_str = json_to_string(total)


    TODAY = datetime.now()
    LASTWEEK = TODAY - timedelta(days=30)

    start_date = "{}-{:02d}-{:02d}T00:00:00".format(LASTWEEK.year, LASTWEEK.month, LASTWEEK.day)
    end_date = "{}-{:02d}-{:02d}T00:00:00".format(TODAY.year, TODAY.month, TODAY.day)

    if(request.args.get('start_date')):
        start_date = "{}T00:00:00".format(request.args.get('start_date'))
    if(request.args.get('end_date')):
        end_date = "{}T00:00:00".format(request.args.get('end_date'))

    print("s {}".format(start_date))
    print("e {}".format(end_date))

    articles = getNewArticles(start_date, end_date)

    trends = get_trending_searches()

    return render_template("news.html", start=start_date, end=end_date, articles=articles, trends=trends) # Render News on covid this week

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
if __name__ == "__main__":
    app.run(debug=True, port=8000)
