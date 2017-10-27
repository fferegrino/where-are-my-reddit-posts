from rake_nltk import Rake

r = Rake()


def keyphrases_extractor(text,number_keyphrases):
    keyphrases = []
    r.extract_keywords_from_text(text) #We give the tool our text
    for i in range(number_keyphrases):
        try:
            keyphrases.append(r.get_ranked_phrases_with_scores()[i][1])
        except IndexError:
            keyphrases.append("")


    returnedString = ""
    for i in range(number_keyphrases):
        if i == number_keyphrases - 1:  # if we are adding the last keyphrase we do not add "|"
            returnedString = returnedString + keyphrases[i]
        else:
            returnedString = returnedString + keyphrases[i] + "|"

    return returnedString
