import sys

import os
from os import listdir
import os.path
from os.path import isfile, join

import json

import numpy as np

from analizers.entities.polarity import Polarity
from processor.simple_encoder import SimpleEncoder
from analizers.vader import vader_sentiment
from analizers.sentiwordnet import naive_sentiment, super_naive_sentiment


def main(args=None):
    """The main routine."""
    if args is None:
        args = sys.argv[1:]

    analyzers = [vader_sentiment,
                 naive_sentiment,
                 super_naive_sentiment]
    analizers_names = ["vader", "naive", "super_naive"]

    input_data_folder = r""

    for a in zip(analyzers, analizers_names):
        analiser = a[0]
        analiser_name = a[1]

        output_data_folder = join(r"", analiser_name)

        if not os.path.exists(output_data_folder):
            os.makedirs(output_data_folder)

        files = [f for f in listdir(input_data_folder) if isfile(join(input_data_folder, f))]

        for json_file in files[0:4]:
            print("Processing", json_file)
            with open(join(input_data_folder,json_file)) as data_file:
                data = json.load(data_file)

            polarity_output = Polarity()

            polarity_output.actual_title_polarity = analiser(data["actual_title"])
            polarity_output.title_polarity = analiser(data["title"])
            polarity_output.news_text_polarity = analiser(data["news_text"])

            for i,comment in enumerate(data["comments"]):
                polarity_output.comment_polarities.append( [ i, analiser(comment["body"])])

            comment_polarities = np.array(polarity_output.comment_polarities)

            polarity_output.comment_polarities_mean = np.mean(comment_polarities[:,1])

            with open(join(output_data_folder, json_file), 'w') as output_file:
                output_file.write(json.dumps(polarity_output, indent=4, sort_keys=True, cls=SimpleEncoder))


if __name__ == "__main__":
    main()