from flask import Flask, render_template
import pandas as pd
import requests

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/api/v1/<station>/<date>")
def about(station, date):
    # df = pd.read_csv()
    # temperature = df.station(date)
    temperature = 23
    return {"station": station,
            "date": date,
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
