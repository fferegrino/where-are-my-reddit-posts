class Submission(object):
    
    def __init__(self, sub_id, title, url, created_utc, ups, downs, score):
        self.id = sub_id
        self.title = title
        self.news_text = None
        self.actual_title = None
        self.created_utc = created_utc
        self.ups = ups
        self.downs = downs
        self.score = score
        self.url = url
        self.comments = []