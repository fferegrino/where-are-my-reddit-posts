import requests # http://docs.python-requests.org/en/master/user/quickstart/#make-a-request
import json

import sys

import os
from os import listdir
import os.path
from os.path import isfile, join

from processor.simple_encoder import SimpleEncoder

import json

from nltk.tag import StanfordPOSTagger
from nltk import word_tokenize
os.environ['STANFORD_MODELS'] = '/stanford/stanford-ner-2017-06-09/classifiers'

input_data_folder= ""
output_data_folder =""
#json_files_to_analyze = [f for f in listdir(input_data_folder) if isfile(join(input_data_folder, f)) and f.endswith(".json")]

# Add the jar and model via their path (instead of setting environment variables):
jar = '/stanford/stanford-ner-2017-06-09/stanford-ner-3.8.0.jar'
model = 'english.conll.4class.distsim.crf.ser.gz'

pos_tagger = StanfordPOSTagger(model, jar, encoding='utf8')

text = pos_tagger.tag(word_tokenize("What's the airspeed of an unladen swallow ?"))
print(text)

"""
for json_file in json_files_to_analyze:
    print("Processing", json_file)
    with open(join(input_data_folder, json_file)) as data_file:
        data = json.load(data_file)

    # Add the jar and model via their path (instead of setting environment variables):
    jar = 'your_path/stanford-postagger-full-2016-10-31/stanford-postagger.jar'
    model = 'your_path/stanford-postagger-full-2016-10-31/models/english-left3words-distsim.tagger'

    pos_tagger = StanfordPOSTagger(model, jar, encoding='utf8')

    text = pos_tagger.tag(word_tokenize("What's the airspeed of an unladen swallow ?"))
    print(text)

    
    #sentiments = sentiment_analysis(data["news_text"][:80000])
    tags = tagging(data["news_text"][:2000])

    processed = {
        #"identified_as": sentiments["label"],
        #"sentiments" : sentiments["probability"],
        "tagged_text" : tags["text"],
        "actual_text" : data["news_text"]
    }

    comments = []
    max_comment_count = 20
    ii = 0
    for i, comment in enumerate(data["comments"]):
        if ii > max_comment_count:
            break
        if len(comment["body"]) < 40:
            continue

        ii = ii + 1
        #comment_sentiments = sentiment_analysis(comment["body"][:80000])
        #comment_analysis = {
        #    "identified_as": comment_sentiments["label"],
        #    "sentiments" : comment_sentiments["probability"],
        #    "text": comment["body"]
        #}
        #comments.append(comment_analysis)
    processed["comments"] = comments

    with open(output_data_folder + json_file, 'w', encoding='utf-8') as submission_file:
        submission_file.write(json.dumps(processed, indent=4, cls=SimpleEncoder))
        
['/usr/bin/java', '-mx1000m', '-cp', '/Users/fferegrino/Documents/GitHub/where-are-my-reddit-posts/stanford/stanford-ner-2017-06-09/stanford-ner.jar', 'edu.stanford.nlp.tagger.maxent.MaxentTagger', '-model', '/Users/fferegrino/Documents/GitHub/where-are-my-reddit-posts/stanford/stanford-ner-2017-06-09/classifiers/english.conll.4class.distsim.crf.ser.gz', '-textFile', '/var/folders/vh/y10fw2hs3rndgglx4l92vxkm0000gn/T/tmp6fkzzsw2', '-tokenize', 'false', '-outputFormatOptions', 'keepEmptySentences', '-encoding', 'utf8']
"""