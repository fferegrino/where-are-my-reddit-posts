import argparse
import csv
import os
from datetime import datetime

from crawler.crawler import SubCrawler

parser = argparse.ArgumentParser(description='Crawl posts from a subreddit given a pair of dates')
parser.add_argument('subreddit', type=str,
                    help='the subreddit to crawl')
parser.add_argument('from_date', type=str,
                    help='ending date (yyyy-MM-dd)')
parser.add_argument('to_date', type=str,
                    help='starting date (yyyy-MM-dd)')
parser.add_argument("-o", "--output_file", action="store",
                    help="the file where I should save the results")


def main(args=None):
    args = parser.parse_args()
    to_date = datetime.strptime(args.to_date, '%Y-%m-%d')
    from_date = datetime.strptime(args.from_date, '%Y-%m-%d')
    subreddit = args.subreddit

    keys = {
        'client_id': os.getenv('CLIENT_ID'),
        'client_secret': os.getenv('CLIENT_SECRET'),
        'username': os.getenv('USERNAME'),
        'password': os.getenv('PASSWORD'),
    }

    crawler = SubCrawler(keys["client_id"], keys["client_secret"], keys["password"], keys["username"])
    subbmissions = crawler.crawl(subreddit, from_date, to_date)

    output_file = args.output_file
    if output_file is None:
        output_file = subreddit + ".csv"
    with open(output_file, 'w', encoding='utf-8') as reddit_posts_csv:
        submwriter = csv.writer(reddit_posts_csv, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
        submwriter.writerow(["id", "created_utc", "score", "comments", "title", "url",
                             "querystring", "permalink"])

    with open(output_file, 'a', encoding='utf-8') as reddit_posts_csv:
        submwriter = csv.writer(reddit_posts_csv, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for lst in subbmissions:
            for s in lst:
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
