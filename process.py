import argparse
import csv
import json
import os
from os.path import join
from pathlib import Path

from processor.simple_encoder import SimpleEncoder
from processor.submission_processor import SubmissionProcessor

parser = argparse.ArgumentParser(description='Get the news and the comments from a set of given reddit submissions')
parser.add_argument('input_file', type=str,
                    help='the file to process')
parser.add_argument("-o", "--output_folder", action="store",
                    help="the file where I should save the results")


def main(args=None):
    args = parser.parse_args()
    input_file = args.input_file
    output_folder = args.output_folder
    if output_folder is None:
        output_folder = "./"

    keys = {
        'client_id': os.getenv('CLIENT_ID'),
        'client_secret': os.getenv('CLIENT_SECRET'),
        'username': os.getenv('USERNAME'),
        'password': os.getenv('PASSWORD'),
    }

    with open(input_file, "r", encoding='utf8') as submissions_file:
        reader = csv.reader(submissions_file)
        next(reader)
        for row in reader:
            if not row:
                continue
            submission_id = row[0]
            processor = SubmissionProcessor(keys["client_id"],
                                            keys["client_secret"],
                                            keys["password"],
                                            keys["username"])

            file_ = join(output_folder, submission_id + ".json")
            if Path(file_).exists():
                continue

            sub = processor.process_submission(submission_id, 10)

            with open(file_, 'w', encoding='utf-8') as submission_file:
                submission_file.write(json.dumps(sub, cls=SimpleEncoder))


if __name__ == "__main__":
    main()
