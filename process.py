import sys
import json
import argparse
import csv
from os.path import join
from utils.keys import read_keys

from pathlib import Path

from processor.submission_processor import SubmissionProcessor
from processor.simple_encoder import SimpleEncoder

parser = argparse.ArgumentParser(description='Get the news and the comments from some Reddit submissions')
parser.add_argument('input_file', metavar='sub', type=str,
                    help='the file to process')
parser.add_argument('keys_file', metavar='sub', type=str,
                    help='route to the file containing the keys for reddit')
parser.add_argument("-o", "--output_folder", action="store",
                    help="the file where I should save the results")

def main(args=None):

    args = parser.parse_args()
    input_file = args.input_file
    output_folder = args.output_folder
    if output_folder is None:
        output_folder = "./"

    keys = read_keys(args.keys_file)

    with open(input_file, "r") as submissions_file:
        reader = csv.reader(submissions_file)
        next(reader)
        for row in reader:
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
                submission_file.write(json.dumps(sub, indent=4, cls=SimpleEncoder))

if __name__ == "__main__":
    main()