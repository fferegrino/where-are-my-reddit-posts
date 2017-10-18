import sys
import argparse
from datetime import datetime
from dateutil.parser import parse

parser = argparse.ArgumentParser(description='Gather some posts from [r]eddit')
parser.add_argument('subreddit', metavar='sub', type=str,
                    help='the subreddit to crawl')
parser.add_argument('startdate', metavar='start', type=str,
                    help='starting date yyyy-MM-dd')
parser.add_argument('enddate', metavar='end', type=str,
                    help='ending date yyyy-MM-dd')


def main(args=None):
    """The main routine."""
    if args is None:
        args = sys.argv[1:]

    args = parser.parse_args()
    start = datetime.strptime(args.startdate, '%Y-%m-%d')
    end = datetime.strptime(args.enddate, '%Y-%m-%d')
    print("Crawling", args.subreddit, "from", start, "to", end)


if __name__ == "__main__":
    main()