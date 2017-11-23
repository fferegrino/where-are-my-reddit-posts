class Comment(object):
    
    def __init__(self, id: str, in_reply_to: str, body: str,
                 comment_level: int, created_utc: int, ups: int,
                 downs: int, score:int):
        self.id = id
        self.ups = ups
        self.downs = downs
        self.score = score
        self.body = body
        self.created_utc = created_utc
        self.in_reply_to = in_reply_to
        self.comment_level = comment_level