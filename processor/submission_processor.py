import json
import sys
import unicodedata

import praw

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

    def process_submission(self, submission_id, max_comment_level = 5):
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

