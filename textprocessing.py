import json
import csv
import numpy as np
from os import listdir
from os.path import isfile, join, isdir
from utils.dates import find_boundaries

from analizers.vader import vader_sentiment

class Row():
    def __init__(self, type, timestamp, positive, negative, neutral, compound):
        self.type = type
        self.timestamp = timestamp
        self.positive = positive
        self.negative= negative
        self.neutral = neutral
        self.compound = compound

years = ["2011","2012","2013","2014","2015","2016","2017"]

x = []
values = np.linspace(-1, 1, 21)
for a, b in zip(values[:-1], values[1:]):
    x.append([a, b, (a+b) / 2])
x = np.array(x)


def get_categorical_value(value):
    return value

for year in years:
    input_data_folder = r"/Users/fferegrino/Downloads/"+year
    output_data_folder = "/Users/fferegrino/Downloads/results"
    folders = [d for d in listdir(input_data_folder) if isdir(join(input_data_folder,d))]
    rows = []

    for folder in folders:
        current_folder = join(input_data_folder,folder)
        json_files_to_analyze = [f for f in listdir(current_folder) if
                                 isfile(join(current_folder, f)) and f.endswith(".json")]

        for json_file in json_files_to_analyze:
            current_file = join(current_folder, json_file)

            with open(current_file) as data_file:
                data = json.load(data_file)


            news_text = data["news_text"]

            sentiments = vader_sentiment(data["news_text"])

            news_row = Row(1, data["created_utc"],
                           get_categorical_value(sentiments["pos"]),
                           get_categorical_value(sentiments["neg"]),
                           get_categorical_value(sentiments["neu"]),
                           get_categorical_value(sentiments["compound"]))

            news_date = data["created_utc"]

            lower, upper = find_boundaries(news_date)

            rows.append(news_row)
            for i, comment in enumerate(data["comments"]):
                comment_date =  comment["created_utc"]
                if lower <= comment_date <= upper:
                    body = comment["body"]
                    comment_sentiments = vader_sentiment(body)

                    comment_row = Row(2, comment["created_utc"],
                                      get_categorical_value(comment_sentiments["pos"]),
                                      get_categorical_value(comment_sentiments["neg"]),
                                      get_categorical_value(comment_sentiments["neu"]),
                                      get_categorical_value(comment_sentiments["compound"]))

                    rows.append(comment_row)

    with open("r" + year + ".csv", 'w', encoding='utf8', newline='') as results_csv:
        submwriter = csv.writer(results_csv, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in rows:
            submwriter.writerow((row.type,
                                 row.timestamp,
                                 row.positive,
                                 row.negative,
                                 row.neutral,
                                 row.compound))

