import json

class SimpleEncoder(json.JSONEncoder):
    def default(self, obj):
        return obj.__dict__