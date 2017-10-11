import praw
import datetime 
import time
import csv

client_id = ""
client_secret = ""
password = ""
username = ""

start_date = datetime.date(2017, 10, 12) # Un dia más de lo deseado
end_date = datetime.date(2017, 10, 9)
time_delay = datetime.timedelta(days=1)

reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     password=password,
                     user_agent='praw_playground by /u/' + username,
                     username=username)

rbitcoin = reddit.subreddit('worldnews');

with open('reddit-posts.csv', 'w', encoding='utf-8') as reddit_posts_csv:
    submwriter = csv.writer(reddit_posts_csv, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
    
    submwriter.writerow(["id", "created_utc", "score","title","url","permalink","comments"])
    while start_date > end_date:
        temp_date = start_date - time_delay
        start_timestamp = int(time.mktime(temp_date.timetuple()))
        end_timestamp = int(time.mktime(start_date.timetuple()))

        print("From ", start_date , "to", temp_date)

        q = "(and timestamp:{}..{})".format(start_timestamp, end_timestamp)
        relevant_posts = rbitcoin.search(q, syntax='cloudsearch', limit=20)
        for submission in relevant_posts:
            submwriter.writerow([submission.id,
                                int(submission.created_utc),
                                int(submission.score),
                                submission.title,
                                submission.url,
                                submission.permalink,
                                int(submission.num_comments)])

        start_date = start_date - time_delay
        time.sleep(5)