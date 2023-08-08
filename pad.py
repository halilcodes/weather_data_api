import pprint

import pandas as pd
import requests

# df = pd.read_csv("dictionary.csv")
# # print(df.head())
# print(df.tail())
# print(df.columns)
# print("*" * 50)
#
# word = "happy"
#
# print(df.loc[df["word"] == word]['definition'].squeeze())
# print(df.loc[df["word"] == word]['definition'].any())
#
# url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
# response = requests.get(url)
# content = response.json()
# pprint.pprint(content)

stations = pd.read_csv("data_small/stations.txt", skiprows=17)
print(stations.columns)