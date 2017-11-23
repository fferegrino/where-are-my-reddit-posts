import praw
import datetime 
import time

class SubCrawler:

    def __init__(self, client_id: str, client_secret: str, password: str, username: str):
        """

        :param client_id:
        :param client_secret:
        :param password:
        :param username:
        """
        self.time_delay = datetime.timedelta(days=1)
        self.reddit = praw.Reddit(client_id=client_id,
                                  client_secret=client_secret,
                                  password=password,
                                  username=username,
                                  user_agent="praw_crawler by /u/" + username)

    def crawl(self, subreddit_name: str, start_date: datetime,
              end_date:datetime, sleep_time: int=5) -> list:
        """
        Crawls the specified Subreddit to gather submissions made within the specified dates
        :param subreddit_name: the name of the subreddit to crawl
        :param start_date:
        :param end_date:
        :param sleep_time: the time to wait between subsequent calls to the reddit endpoint
        :return: a list of submissions where each submission contains:
            - Submission identifier
            - Date created in UT
            - Score
            - Number of comments
            - Title
            - Submitted URL
            - The query string of the submitted URL
            - Permalink to the submission
        """
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