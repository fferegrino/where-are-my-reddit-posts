class Submission(object):
    
    def __init__(self, sub_id, title, url):
        self.id = sub_id
        self.title = title
        self.url = url
        self.comments = []