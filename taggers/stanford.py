import os.path
from nltk.tag import StanfordPOSTagger
from nltk import word_tokenize


class StanfordTagger:
    def __init__(self, jar: str, model:str, java_path: str = None):
        if java_path != None:
            os.environ['JAVAHOME'] = java_path
        self.pos_tagger =  StanfordPOSTagger(model, jar, encoding = "utf8")

    def tag(self, text:str):
        """
        Takes a text and returns a list of tagged text
        :param text:
        :return:
        """
        return self.pos_tagger.tag(word_tokenize(text))
