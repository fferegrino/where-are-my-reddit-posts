import sys

import os
from os import listdir
import os.path
from os.path import isfile, join

import json
import csv

import numpy as np

from analizers.entities.polarity import Polarity
from processor.simple_encoder import SimpleEncoder
from analizers.vader import vader_sentiment
from analizers.sentiwordnet import naive_sentiment, super_naive_sentiment
from cleaners.cleaners import tweet_clean, no_cleaning


def main(args=None):
    """The main routine."""
    if args is None:
        args = sys.argv[1:]

    analyzers = [vader_sentiment,
                 naive_sentiment,
                 super_naive_sentiment]
    analizers_names = ["vader", "naive", "super_naive"]

    cleaners =[tweet_clean, no_cleaning]
    cleaners_names = ["twitter", "no"]

    input_data_folder = r""
    files = [f for f in listdir(input_data_folder) if isfile(join(input_data_folder, f))]
    for an in zip(analyzers, analizers_names):
        analiser = an[0]
        analiser_name = an[1]
        for cl in zip(cleaners, cleaners_names):
            cleaner = cl[0]
            cleaner_name = cl[1]

            output_data_folder = join(r"", analiser_name, cleaner_name)

            if not os.path.exists(output_data_folder):
                os.makedirs(output_data_folder)

            with open(join(output_data_folder, "data") + '-posts.csv', 'w', encoding='utf-8') as reddit_posts_csv:
                submwriter = csv.writer(reddit_posts_csv, delimiter=',',
                                        quotechar='"', quoting=csv.QUOTE_MINIMAL)
                submwriter.writerow(
                    ["time", "news_polarity", "comment_polarity_mean", "positive_comment_polarity", "negative_comment_polarity"])

                for json_file in files:
                    if(json_file == ".DS_Store"):
                        continue
                    print("Processing", json_file)
                    with open(join(input_data_folder, json_file)) as data_file:
                        data = json.load(data_file)

                    polarity_output = Polarity()

                    value1 = analiser(cleaner(data["news_text"]))

                    #polarity_output.actual_title_polarity = { "polarity":analiser(cleaner(data["actual_title"])), "text": data["actual_title"] }
                    #polarity_output.title_polarity = { "polarity": analiser(cleaner(data["title"])) ,"text": data["title"]}
                    polarity_output.news_text_polarity =  value1

                    for i,comment in enumerate(data["comments"]):
                        polarity_output.comment_polarities.append( [ i, analiser(cleaner(comment["body"]))])

                    comment_polarities = np.array(polarity_output.comment_polarities)

                    all_comments = comment_polarities[:,1]
                    all_positive = all_comments[all_comments > 0]
                    all_negative = all_comments[all_comments < 0]

                    polarity_output.comment_polarities_mean = np.mean(all_comments)

                    #with open(join(output_data_folder, json_file), 'w') as output_file:
                    #    output_file.write(json.dumps(polarity_output, indent=4, sort_keys=True, cls=SimpleEncoder))
                    submwriter.writerow([data["created_utc"],
                                         polarity_output.news_text_polarity,
                                         polarity_output.comment_polarities_mean,
                                         np.mean(all_positive),
                                         np.mean(all_negative)])




if __name__ == "__main__":
    main()
