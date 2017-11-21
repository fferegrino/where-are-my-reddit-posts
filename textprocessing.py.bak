import json
from os import listdir
from os.path import isfile, join

from processor.simple_encoder import SimpleEncoder
from taggers.stanford import StanfordTagger

java_path = r"\java.exe"
model = r"\english-caseless-left3words-distsim.tagger"
jar = r"\stanford-postagger.jar"

input_data_folder = ""
output_data_folder = ""
json_files_to_analyze = [f for f in listdir(input_data_folder) if
                         isfile(join(input_data_folder, f)) and f.endswith(".json")]

for json_file in json_files_to_analyze:
    print("Processing", json_file)
    with open(join(input_data_folder, json_file)) as data_file:
        data = json.load(data_file)

    pos_tagger = StanfordTagger(jar, model, java_path)

    text = pos_tagger.tag("What's the airspeed of an unladen swallow ?")
    print(text)

    # sentiments = sentiment_analysis(data["news_text"][:80000])
    tags = pos_tagger.tag(data["news_text"][:2000])

    processed = {
        # "identified_as": sentiments["label"],
        # "sentiments" : sentiments["probability"],
        "tagged_text": tags["text"],
        "actual_text": data["news_text"]
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
        # comment_sentiments = sentiment_analysis(comment["body"][:80000])
        # comment_analysis = {
        #    "identified_as": comment_sentiments["label"],
        #    "sentiments" : comment_sentiments["probability"],
        #    "text": comment["body"]
        # }
        # comments.append(comment_analysis)
    processed["comments"] = comments

    with open(output_data_folder + json_file, 'w', encoding='utf-8') as submission_file:
        submission_file.write(json.dumps(processed, indent=4, cls=SimpleEncoder))
