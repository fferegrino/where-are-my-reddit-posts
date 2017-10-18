import praw
import datetime 
import time
import csv

class SubCrawler:

    def __init__(self, client_id, client_secret, password, username):
        self.time_delay = datetime.timedelta(days=1)
        self.reddit = praw.Reddit(client_id=client_id,
                                  client_secret=client_secret,
                                  password=password,
                                  username=username,
                                  user_agent="praw_crawler by /u/" + username)

    def crawl(self, subreddit_name, start_date, end_date, sleep_time = 5):
        subreddit = self.reddit.subreddit(subreddit_name)
        submissions = []
        while start_date > end_date:
            temp_date = start_date - self.time_delay
            start_timestamp = int(time.mktime(temp_date.timetuple()))
            end_timestamp = int(time.mktime(start_date.timetuple()))

            q = "(and timestamp:{}..{})".format(start_timestamp, end_timestamp)
            relevant_posts = subreddit.search(q, syntax="cloudsearch", limit=20)
            for submission in relevant_posts:
                q = submission.url.find("?")
                url = submission.url
                query_string = ""
                if q >= 0:
                    url = submission.url[:q]
                    query_string = submission.url[q + 1:]
                sub = {
                    "id" : submission.id,
                    "created_utc": int(submission.created_utc),
                    "score": int(submission.score),
                    "comments": int(submission.num_comments),
                    "title": submission.title,
                    "url": url,
                    "query_string": query_string,
                    "permalink": submission.permalink
                    }
                submissions.append(sub)
            start_date = start_date - self.time_delay
            time.sleep(sleep_time)
        return submissions