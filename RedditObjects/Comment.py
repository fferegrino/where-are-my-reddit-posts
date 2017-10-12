class Comment(object):
    
    def __init__(self, id, in_reply_to, body, comment_level, created_utc, ups, downs, score):
        self.id = id
        self.ups = ups
        self.downs = downs
        self.score = score
        self.body = body
        self.created_utc = created_utc
        self.in_reply_to = in_reply_to
        self.comment_level = comment_level