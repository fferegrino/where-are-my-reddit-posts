class Comment(object):
    
    def __init__(self, id, in_reply_to, ups, body, comment_level):
        self.id = id
        self.ups = ups
        self.body = body
        self.in_reply_to = in_reply_to
        self.comment_level = comment_level