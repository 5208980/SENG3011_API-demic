from flask import Flask, render_template
from covid19 import generate_data
import re
# import requests

app = Flask(__name__)

@app.route("/")
def home():

    # response = requests.get("http://127.0.0.1:5000/v1.1/articles?start_date=2020-01-01T12:00:00&end_date=2020-02-01T10:00:00&location=australia&key_term=coronavirus")
    # print(response.json())
    # Fetch API will be called in JAVASCRIPT NOT PYTHON LIKE ABOVE

    return render_template("index.html")

@app.route("/article")
def article():
    return render_template("article.html")

@app.route("/covid19")
def covid19():
    # https://api.covid19api.com/
    data = generate_data()

    # validates json
    s = str(data)
    s = re.sub('\'', '\"', s)
    s = re.sub('[a-zA-Z]\,', '', s)
    s = re.sub('[a-zA-Z]\"[a-zA-Z]', '', s)

    return render_template("covid.html", data=s)

if __name__ == "__main__":
    app.run(debug=True, port=8000)
