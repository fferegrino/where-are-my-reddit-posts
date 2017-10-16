import csv
import datetime
import json
import os
import os.path
import time
import unicodedata

import praw
from newsplease import NewsPlease

from RedditObjects.Comment import Comment
from RedditObjects.Submission import Submission

client_id = ""
client_secret = ""
password = ""
username = ""

reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     password=password,
                     user_agent='praw_playground by /u/' + username,
                     username=username)


# https://praw.readthedocs.io/en/latest/tutorials/comments.html

class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        return obj.__dict__


def process_submission(submission_id):
    submission = reddit.submission(id=submission_id)
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
        if tab > 4:
            continue
        for reply in comment.replies:
            comment_queue.append(reply)
            tab_queue.append(tab + 1)
    return sub


posts_file = '2015-top-5'

with open('data/yearly_submissions/' + posts_file + '.csv', 'r', encoding='utf-8') as csvfile:
    post_reader = csv.reader(csvfile, delimiter=',',
                             quotechar='"', quoting=csv.QUOTE_MINIMAL)
    wrong_posts = []
    next(post_reader)
    for row in post_reader:
        id = row[0]
        url = row[5]
        created_utc = int(row[1])
        try:
            date = datetime.datetime.fromtimestamp(created_utc).strftime('%Y-%m-%d')
            short_date = datetime.datetime.fromtimestamp(created_utc).strftime('%Y-%m')
            directory = "data/submissions/" + short_date

            if not os.path.exists(directory):
                os.makedirs(directory)
            submission_file = directory + "/" + date + "-" + id + ".json"

            if os.path.isfile(submission_file):
                if os.path.getsize(submission_file) > 100:
                    print("I have it", submission_file)
                    continue

            sub = process_submission(id)
            article = NewsPlease.from_url(url)
            sub.actual_title = unicodedata.normalize("NFKD", article.title)
            sub.news_text = unicodedata.normalize("NFKD", article.text)

            f = open(submission_file, 'w')
            f.write(json.dumps(sub, cls=MyEncoder))
        except:
            print("Something went wrong: ", id)
            wrong_posts.append(id)
        time.sleep(5)
    fwrong = open("data/" + posts_file + "-wrong.json", 'w')
    fwrong.write(json.dumps(wrong_posts))
