import datetime 
import time
import csv

current_file = ""

with open('data/reddit.csv', 'r', encoding='utf-8') as csvfile:
    i = 0
    post_reader = csv.reader(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
    next(post_reader)
    f = None
    writer = None
    for row in post_reader:
        
        date = datetime.datetime.fromtimestamp(int(row[1])).strftime('%Y-%m')
        if current_file != date:
            current_file = date
            print(i, current_file)
            if f != None:
                f.close()
            f = open("data/monthly_submissions/" + date + '-posts.csv', 'w', encoding='utf-8')
            writer = csv.writer(f, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(row)
        i = i + 1