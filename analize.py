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
parser.add_argument("-o", "--output_folder", action="store",
                    help="the folder to store the analyzer results")
parser.add_argument("-a", "--all_analyzers", help="should i run every analyzer?", action="store_true", default=False)
parser.add_argument("-v", "--verbose", help="should i tell you everything im doing?", action="store_true", default=False)


def main(args=None):
    """The main routine."""
    if args is None:
        args = sys.argv[1:]

    args = parser.parse_args()

    input_data_folder = args.input_folder
    output_data_folder_path = args.output_folder
    if output_data_folder_path == None:
        output_data_folder_path = join(input_data_folder, "results")

    analyzers = [vader_sentiment]
    analizers_names = ["vader"]

    if args.all_analyzers:
        analyzers.append(naive_sentiment)
        analizers_names.append("naive_sentiment")

        analyzers.append(super_naive_sentiment)
        analizers_names.append("super_naive_sentiment")

    if args.verbose:
        print("Input:", input_data_folder)
        print("Output:", output_data_folder_path)
        print("Analyzers to run: ", analizers_names)

    json_files_to_analyze = [f for f in listdir(input_data_folder) if isfile(join(input_data_folder, f)) and f.endswith(".json")]
    for an in zip(analyzers, analizers_names):
        analiser = an[0]
        analiser_name = an[1]

        if not os.path.exists(output_data_folder_path):
            os.makedirs(output_data_folder_path)

        with open(join(output_data_folder_path, "results-" + analiser_name + ".csv"), 'w', encoding='utf-8') as results_csv:
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

                polarity_output = Polarity()

                news_polarity = analiser(data["news_text"])

                polarity_output.news_text_polarity = news_polarity

                for i, comment in enumerate(data["comments"]):
                    polarity_output.comment_polarities.append([i, analiser(comment["body"])])

                comment_polarities = np.array(polarity_output.comment_polarities)

                all_comments = comment_polarities[:, 1]
                all_positive = all_comments[all_comments > 0]
                all_negative = all_comments[all_comments < 0]

                polarity_output.comment_polarities_mean = np.mean(all_comments)

                results_writer.writerow([data["created_utc"],
                                         polarity_output.news_text_polarity,
                                         polarity_output.comment_polarities_mean,
                                         np.mean(all_positive),
                                         np.mean(all_negative)])


if __name__ == "__main__":
    main()