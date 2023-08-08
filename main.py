from flask import Flask, render_template
import pandas as pd
import requests
import datetime as dt
import numpy as np

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/api/v1/<station>/<date>")
def about(station, date):
    df = pd.read_csv(f"data_small/TG_STAID" + str(station).zfill(6) + ".txt", skiprows=20, parse_dates=['    DATE'])
    date_formatted = dt.datetime.strptime(date, "%Y-%m-%d")
    data_quality = df.loc[df['    DATE'] == date_formatted][' Q_TG'].squeeze()
    if data_quality != 9:
        temperature = df.loc[df['    DATE'] == date_formatted]['   TG'].squeeze() / 10
    else:
        temperature = np.nan
    # temperature = 23
    return {"station": station,
            "date": dt.datetime.strftime(date_formatted, "%Y-%m-%d"),
            "temperature": temperature}


@app.route("/api/v2/<word>")
def dictionary(word):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(url)
    if response:
        content = response.json()
        definitions = content[0]['meanings'][0]['definitions']
        result = ""
        n = 1
        if len(definitions) >= 2:
            for definition in definitions[:2]:
                result += str(n) + ". " + definition['definition'] + "\n"
                n += 1
        else:
            result += definitions['definition']

        return {"definition": str(result),
                "word": str(word)}
    else:
        return {"definition": "meaningless word",
                "word": str(word)}


if __name__ == "__main__":
    app.run(debug=True)
    # app.run(debug=True, port=5001)
