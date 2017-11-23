class Submission(object):
    
    def __init__(self, sub_id: str, title: str, url: str,
                 created_utc: int, ups: int, downs: int, score: int):
        self.id = sub_id
        self.title = title
        self.news_text = None
        self.selftext = None
        self.is_self = False
        self.actual_title = None
        self.created_utc = created_utc
        self.ups = ups
        self.downs = downs
        self.score = score
        self.url = url
        self.comments = []