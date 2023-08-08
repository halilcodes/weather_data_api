from flask import Flask, render_template
import pandas as pd
import requests
import datetime as dt
import numpy as np

app = Flask(__name__)

variable = "Helloo Python Community!"

stations = pd.read_csv("data_small/stations.txt", skiprows=17)
stations = stations[["STAID", 'STANAME                                 ']]


@app.route("/")
def home():
    return render_template("home.html", data=stations.to_html())


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


@app.route("/api/v1/<station>")
def all_data(station):
    df = pd.read_csv(f"data_small/TG_STAID" + str(station).zfill(6) + ".txt", skiprows=20, parse_dates=['    DATE'])
    result = df.to_dict(orient="records")
    return result


@app.route("/api/v1/annual/<station>/<year>")
def all_year(station, year):
    df = pd.read_csv(f"data_small/TG_STAID" + str(station).zfill(6) + ".txt", skiprows=20)
    df['    DATE'] = df['    DATE'].astype(str)
    df = df[df['    DATE'].str.startswith(str(year))]
    # df['    DATE'] = pd.to_datetime(df['    DATE'], format="%Y%m%d")  # also works
    df['    DATE'] = df['    DATE'].apply(pd.to_datetime)
    result = df.to_dict(orient="records")
    return result


@app.route("/api/v2/<word>")
def dictionary(word):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(url)
    if response:
        content = response.json()
        definitions = content[0]['meanings'][0]['definitions']
        result = ""
        n = 1
        if len(definitions) >= 1:
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


@app.route("/api/v3/<word>")
def dictionary_v2(word):
    df = pd.read_csv("dictionary.csv")
    definition = df.loc[df["word"] == word]['definition']
    if bool(definition.any()):
        print(definition.squeeze())
        return {"definition": str(definition.squeeze()),
                "word": str(word).capitalize()}
    else:
        return {"definition": "meaningless word",
                "word": str(word)}


if __name__ == "__main__":
    app.run(debug=True)
    # app.run(debug=True, port=5001)
