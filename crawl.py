import sys
import argparse
import csv
from datetime import datetime
from utils.keys import read_keys

from crawler.crawler import SubCrawler

parser = argparse.ArgumentParser(description='Crawl posts from a subreddit given a pair of dates')
parser.add_argument('subreddit', type=str,
                    help='the subreddit to crawl')
parser.add_argument('from_date', type=str,
                    help='ending date (yyyy-MM-dd)')
parser.add_argument('to_date',  type=str,
                    help='starting date (yyyy-MM-dd)')
parser.add_argument('keys_file', type=str,
                    help='route to the file containing the keys for reddit')
parser.add_argument("-o", "--output_file", action="store",
                    help="the file where I should save the results")

def main(args=None):

    args = parser.parse_args()
    to_date = datetime.strptime(args.to_date, '%Y-%m-%d')
    from_date = datetime.strptime(args.from_date, '%Y-%m-%d')
    subreddit = args.subreddit

    keys = read_keys(args.keys_file)

    crawler = SubCrawler(keys["client_id"], keys["client_secret"], keys["password"], keys["username"])
    subbmissions = crawler.crawl(subreddit, to_date, from_date)

    output_file = args.output_file
    if output_file is None:
        output_file = subreddit + ".csv"
    with open(output_file, 'w', encoding='utf-8') as reddit_posts_csv:
        submwriter = csv.writer(reddit_posts_csv, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
        submwriter.writerow(["id", "created_utc", "score", "comments", "title", "url",
                             "querystring", "permalink"])
        for s in subbmissions:
            submwriter.writerow([s["id"],
                                 s["created_utc"],
                                 s["score"],
                                 s["comments"],
                                 s["title"],
                                 s["url"],
                                 s["query_string"],
                                 s["permalink"]])

if __name__ == "__main__":
    main()