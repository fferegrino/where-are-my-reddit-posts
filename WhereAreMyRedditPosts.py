import praw
import datetime 
import time

client_id = ""
client_secret = ""
password = ""
username = ""

start_date = datetime.date.today()
end_date = datetime.date(2017, 10, 5)
time_delay = datetime.timedelta(days=1)

reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     password=password,
                     user_agent='praw_playground by /u/' + username,
                     username=username)

rbitcoin = reddit.subreddit('bitcoin');

while start_date > end_date:
    temp_date = start_date - time_delay
    start_timestamp = int(time.mktime(temp_date.timetuple()))
    end_timestamp = int(time.mktime(start_date.timetuple()))

    q = "(and timestamp:{}..{})".format(start_timestamp, end_timestamp)
    relevant_bitcoin_posts = rbitcoin.search(q, syntax='cloudsearch', limit=10)
    for submission in relevant_bitcoin_posts:
        created_utc = datetime.datetime.utcfromtimestamp(int(submission.created_utc))
        print(created_utc, submission.title)

    start_date = start_date - time_delay
    time.sleep(5)
