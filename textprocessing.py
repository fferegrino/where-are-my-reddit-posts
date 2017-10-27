import json
import csv
from os import listdir
from os.path import isfile, join

from processor.simple_encoder import SimpleEncoder
from analizers.vader import vader_sentiment
from taggers.keyphrase import keyphrases_extractor

class Row():
    def __init__(self, type, timestamp, positive, negative, neutral, compound, keyphrases):
        self.type = type
        self.timestamp = timestamp
        self.positive = positive
        self.negative= negative
        self.neutral = neutral
        self.compound = compound
        self.keyphrases = keyphrases

input_data_folder = "data"
output_data_folder = ""
json_files_to_analyze = [f for f in listdir(input_data_folder) if
                         isfile(join(input_data_folder, f)) and f.endswith(".json")]

rows = []
for json_file in json_files_to_analyze:
    print("Processing", json_file)
    with open(join(input_data_folder, json_file)) as data_file:
        data = json.load(data_file)

    news_text = data["news_text"]

    sentiments = vader_sentiment(data["news_text"])

    # Mario stuff goes here (pass news_text to the keyphrase extractor):
    keyphrases = keyphrases_extractor(data["news_text"])

    news_row = Row(1, data["created_utc"], sentiments["pos"], sentiments["neg"], sentiments["neu"],
                   sentiments["compound"], keyphrases)

    rows.append(news_row)
    for i, comment in enumerate(data["comments"]):
        body = comment["body"]
        comment_sentiments = vader_sentiment(body)

        # Mario stuff goes here (pass body to the keyphrase extractor):
        keyphrases = keyphrases_extractor(body)

        comment_row = Row(2, comment["created_utc"], comment_sentiments["pos"], comment_sentiments["neg"],
                          comment_sentiments["neu"], sentiments["compound"], keyphrases)

        rows.append(comment_row)

with open("results.csv", 'w', encoding='utf8', newline='') as results_csv:
    submwriter = csv.writer(results_csv, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for row in rows:
        submwriter.writerow((row.type,
                             row.timestamp,
                             row.positive,
                             row.negative,
                             row.neutral,
                             row.compound,
                             row.keyphrases))


