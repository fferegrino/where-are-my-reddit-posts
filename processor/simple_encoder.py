import json

class SimpleEncoder(json.JSONEncoder):
    """
    Auxiliary class that helps when serializing objects to a JSON format
    """
    def default(self, obj):
        return obj.__dict__