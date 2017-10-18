import json
import sys
import unicodedata

import praw

from newsplease import NewsPlease

from processor.reddit_objects.submission import Submission
from processor.reddit_objects.comment import Comment


# https://praw.readthedocs.io/en/latest/tutorials/comments.html
class SubmissionProcessor:
    def __init__(self, client_id, client_secret, password, username):
        self.reddit = praw.Reddit(client_id=client_id,
                                  client_secret=client_secret,
                                  password=password,
                                  username=username,
                                  user_agent="praw_crawler by /u/" + username)


    def process_submission(self, submission_id, max_comment_level =  5):
        sub = self.get_from_reddit(submission_id, max_comment_level)
        try:
            article = NewsPlease.from_url(sub.url)
            sub.actual_title = unicodedata.normalize("NFKD", article.title)
            sub.news_text = unicodedata.normalize("NFKD", article.text)
        except Exception as e:
            sub.actual_title = str(e)
        return sub


    def get_from_reddit(self, submission_id, max_comment_level):
        if max_comment_level == -1:
            max_comment_level = sys.maxsize

        submission = self.reddit.submission(id=submission_id)
        submission.comments.replace_more(limit=0)
        comment_queue = []
        tab_queue = []
        sub = Submission(submission_id,
                         unicodedata.normalize("NFKD", submission.title),
                         submission.url,
                         int(submission.created_utc),
                         submission.ups,
                         submission.downs,
                         submission.score)
        sub.selftext = submission.selftext
        sub.is_self = submission.is_self
        for s in submission.comments:
            comment_queue.append(s)
            tab_queue.append(0)
        while comment_queue:
            comment = comment_queue.pop()
            tab = tab_queue.pop()
            com = Comment(
                comment.id,
                comment.parent_id,
                unicodedata.normalize("NFKD", comment.body),
                tab,
                int(comment.created_utc),
                comment.ups,
                comment.downs,
                comment.score)
            sub.comments.append(com)
            if tab > max_comment_level:
                continue
            for reply in comment.replies:
                comment_queue.append(reply)
                tab_queue.append(tab + 1)
        return sub

