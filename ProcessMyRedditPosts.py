import praw
import csv

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

t = None

def process_submission(submission_id):
    submission = reddit.submission(id=submission_id)
    for top_level_comment in submission.comments:
        t = top_level_comment

with open('reddit-posts.csv', 'r', encoding='utf-8') as csvfile:
    i = 0
    post_reader = csv.reader(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for row in post_reader:
        if i > number_of_rows:
            break
        i = i + 1
        process_submission(row[0])
