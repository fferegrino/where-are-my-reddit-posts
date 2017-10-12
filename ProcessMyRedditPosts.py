import praw
import csv
import json
import unicodedata 
import datetime
from RedditObjects.Submission import Submission
from RedditObjects.Comment import Comment
from newsplease import NewsPlease

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
            tab_queue.append(tab+1)
    return sub

number_of_rows = 1000

with open('data/reddit-posts-2017-10-12-2011-12-31-fixed.csv', 'r', encoding='utf-8') as csvfile:
    i = 0
    post_reader = csv.reader(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
    wrong_posts = []
    next(post_reader)
    for row in post_reader:
        i = i + 1
        if i > number_of_rows:
            break
        try:
            sub = process_submission(row[0])
            article = NewsPlease.from_url(row[4])
            sub.actual_title = unicodedata.normalize("NFKD", article.title)
            sub.news_text = unicodedata.normalize("NFKD", article.text)
            date = datetime.datetime.fromtimestamp(sub.created_utc).strftime('%Y-%m-%d')
            f = open("data/submissions/"+ date + "-" + row[0] + ".json", 'w')
            f.write(json.dumps(sub, cls=MyEncoder))
        except:
            print("Something went wrong: ", row[0])
            wrong_posts.append(row[0])
    fwrong = open("data/wrong.json", 'w')
    fwrong.write(json.dumps(wrong_posts))