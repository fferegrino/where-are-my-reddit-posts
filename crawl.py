import sys
import argparse
import csv
from datetime import datetime

from crawler.crawler import SubCrawler

parser = argparse.ArgumentParser(description='Gather some posts from [r]eddit')
parser.add_argument('subreddit', metavar='sub', type=str,
                    help='the subreddit to crawl')
parser.add_argument('startdate', metavar='start', type=str,
                    help='starting date yyyy-MM-dd')
parser.add_argument('enddate', metavar='end', type=str,
                    help='ending date yyyy-MM-dd')

# receive this as arguments
client_id = ""
client_secret = ""
password = ""
username = ""


def main(args=None):
    """The main routine."""
    if args is None:
        args = sys.argv[1:]

    args = parser.parse_args()
    start = datetime.strptime(args.startdate, '%Y-%m-%d')
    end = datetime.strptime(args.enddate, '%Y-%m-%d')
    subreddit = args.subreddit

    print("Crawling", subreddit, "from", start, "to", end)
    crawler = SubCrawler(client_id, client_secret, password, username)
    subbmissions = crawler.crawl(subreddit, start, end)
    with open(subreddit + '-posts.csv', 'w', encoding='utf-8') as reddit_posts_csv:
        submwriter = csv.writer(reddit_posts_csv, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
        submwriter.writerow(["id", "created_utc", "score", "comments", "title", "url", "querystring", "permalink"])
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