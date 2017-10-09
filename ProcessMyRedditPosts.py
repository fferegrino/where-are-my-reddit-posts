import praw
import csv
import json
from RedditObjects.Submission import Submission
from RedditObjects.Comment import Comment

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
    sub = Submission(submission_id, submission.title, submission.url)
    for s in submission.comments:
        comment_queue.append(s)
        tab_queue.append(0)
    while comment_queue:
        comment = comment_queue.pop()
        tab = tab_queue.pop()
        com = Comment(
                      comment.id, 
                      comment.parent_id, 
                      comment.ups,
                      comment.body,
                      tab)
        sub.comments.append(com)
        # print("\t" * tab,tab,comment.body.encode('utf-8'))
        for reply in comment.replies:
            comment_queue.append(reply)
            tab_queue.append(tab+1)
    return sub

number_of_rows = 1
submissions = []

with open('reddit-posts.csv', 'r', encoding='utf-8') as csvfile:
    i = 0
    post_reader = csv.reader(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for row in post_reader:
        if i > number_of_rows:
            break
        i = i + 1
        submissions.append(process_submission(row[0]))

#print(json.dumps(submissions, cls=MyEncoder))

