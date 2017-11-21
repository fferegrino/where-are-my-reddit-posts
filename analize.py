import json
import csv
import argparse
from analizers.entities.polarity import Polarity
from os import listdir
from os.path import isfile, join, isdir
from utils.dates import find_boundaries

from analizers.vader import vader_sentiment

parser = argparse.ArgumentParser(description='Analyze the sentiments of a bunch of News and their Reddit coments')
parser.add_argument('input_folder', type=str,
                    help='the file folder with the .json files to process')
parser.add_argument("-o", "--output_file", action="store",
                    help="the file where I should save the results")

def main(args=None):

    args = parser.parse_args()
    input_folder = args.input_folder
    output_file = args.output_file
    if output_file is None:
        output_file = "sentiment-analysis.csv"
    rows = []

    json_files_to_analyze = [f for f in listdir(input_folder) if
                             isfile(join(input_folder, f)) and f.endswith(".json")]

    for json_file in json_files_to_analyze:
        current_file = join(input_folder, json_file)

        with open(current_file) as data_file:
            data = json.load(data_file)

        news_text = data["news_text"]
        if news_text is None:
            continue

        sentiments = vader_sentiment(news_text)

        news_row = Polarity(1, data["created_utc"],
                       sentiments["pos"],
                       sentiments["neg"],
                       sentiments["neu"],
                       sentiments["compound"])

        news_date = data["created_utc"]

        lower, upper = find_boundaries(news_date)

        rows.append(news_row)
        for i, comment in enumerate(data["comments"]):
            comment_date =  comment["created_utc"]
            if lower <= comment_date <= upper:
                body = comment["body"]
                comment_sentiments = vader_sentiment(body)

                comment_row = Polarity(2, comment["created_utc"],
                                  comment_sentiments["pos"],
                                  comment_sentiments["neg"],
                                  comment_sentiments["neu"],
                                  comment_sentiments["compound"])

                rows.append(comment_row)

    with open(output_file, 'w', encoding='utf8', newline='') as results_csv:
        submwriter = csv.writer(results_csv, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in rows:
            submwriter.writerow((row.type,
                                 row.timestamp,
                                 row.positive,
                                 row.negative,
                                 row.neutral,
                                 row.compound))

if __name__ == "__main__":
    main()
