import sys

import os
from os import listdir
import os.path
from os.path import isfile, join

import json
import csv

import numpy as np

from analizers.entities.polarity import Polarity
from analizers.vader import vader_sentiment
from analizers.sentiwordnet import naive_sentiment, super_naive_sentiment

# args
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("input_folder", help="input folder for your text files")
parser.add_argument("-o", "--output_file", action="store",
                    help="the folder to store the analyzer results")
parser.add_argument("-v", "--verbose", help="should i tell you everything im doing?", action="store_true", default=False)


def main(args=None):

    args = parser.parse_args()

    input_data_folder = args.input_folder
    output_file = args.output_file
    if output_file == None:
        output_file = "sentiment-results.csv"

    if args.verbose:
        print("Input folder:", input_data_folder)
        print("Output:", output_file)
        print("Analyzers to run: vader")

    json_files_to_analyze = [f for f in listdir(input_data_folder) if isfile(join(input_data_folder, f)) and f.endswith(".json")]
    analiser = vader_sentiment

    with open(output_file, 'w', encoding='utf-8') as results_csv:
        results_writer = csv.writer(results_csv, delimiter=',',
                                    quotechar='"', quoting=csv.QUOTE_MINIMAL)
        results_writer.writerow(
            ["time", "news_polarity", "comment_polarity_mean", "positive_comment_polarity",
             "negative_comment_polarity"])

        for json_file in json_files_to_analyze:
            if args.verbose:
                print("Processing", json_file)
            with open(join(input_data_folder, json_file)) as data_file:
                data = json.load(data_file)

            if data["news_text"] is None:
                continue

            polarity_output = Polarity()

            news_polarity = analiser(data["news_text"])

            polarity_output.news_text_polarity = news_polarity

            mean_positive = np.nan
            mean_negative = np.nan
            comment_polarities_mean = np.nan

            if len(data["comments"]) > 0:
                for i, comment in enumerate(data["comments"]):
                    polarity_output.comment_polarities.append([i, analiser(comment["body"])])

                comment_polarities = np.array(polarity_output.comment_polarities)

                all_comments = comment_polarities[:, 1]
                all_positive = all_comments[all_comments > 0]
                all_negative = all_comments[all_comments < 0]

                comment_polarities_mean = np.mean(all_comments)
                mean_positive = np.mean(all_positive)
                mean_negative = np.mean(all_negative)


            results_writer.writerow([data["created_utc"],
                                     polarity_output.news_text_polarity,
                                     comment_polarities_mean,
                                     mean_positive,
                                     mean_negative])


if __name__ == "__main__":
    main()