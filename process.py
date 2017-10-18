import sys
import json

from processor.submission_processor import SubmissionProcessor
from processor.simple_encoder import SimpleEncoder

# receive this as arguments
client_id = ""
client_secret = ""
password = ""
username = ""

def main(args=None):
    """The main routine."""
    if args is None:
        args = sys.argv[1:]
    # https://www.reddit.com/r/conlangs/comments/5f8rzw/a_serious_emoji_conlang/
    # https://www.reddit.com/r/emojilang/
    submission_id = "5f8rzw"

    processor = SubmissionProcessor(client_id, client_secret, password, username)

    sub = processor.process_submission(submission_id, 10)
    with open("data/"+ submission_id + ".json", 'w', encoding='utf-8') as submission_file:
        submission_file.write(json.dumps(sub, cls=SimpleEncoder))

if __name__ == "__main__":
    main()