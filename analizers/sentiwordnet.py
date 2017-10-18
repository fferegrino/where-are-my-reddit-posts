from nltk.corpus import sentiwordnet as swn
from string import punctuation
from nltk.corpus import stopwords

def super_naive_sentiment(review):
	# from pluralsight
    review_polarity = 0.0
    num_exceptions = 0
    considered_words = 0
    for word in review.lower().split(): # no capitalization!
        weight = 0.0
        try:
            meanings = list(swn.senti_synsets(word))
            common_meaning = meanings[0] # Just one meaning
            if common_meaning.pos_score()>common_meaning.neg_score():
                weight = weight + common_meaning.pos_score()
            elif common_meaning.pos_score()<common_meaning.neg_score():
                weight = weight - common_meaning.neg_score()
            considered_words = considered_words + 1
        except: # the world noes not exist in the sentiworld dictionary
            num_exceptions = num_exceptions + 1
        review_polarity = review_polarity + weight
    if considered_words > 0:
        return review_polarity / considered_words
    return 0


stopwords = set(stopwords.words('english') + list (punctuation))

def naive_sentiment(review):
	# from pluralsight
    review_polarity = 0.0
    num_exceptions = 0
    considered_words = 0
    for word in review.lower().split():
        num_meanings = 0
        if word in stopwords: # ignore stopwords
            continue
        weight = 0.0
        try:
            for meaning in swn.senti_synsets(word): # analyze all meanings
                if meaning.pos_score() > meaning.neg_score():
                    weight = weight + (meaning.pos_score() - meaning.neg_score())
                    num_meanings = num_meanings + 1
                elif meaning.pos_score() < meaning.neg_score():
                    weight = weight - (meaning.neg_score() - meaning.pos_score())
                    num_meanings = num_meanings + 1
                considered_words = considered_words + 1
        except:
            num_exceptions = num_exceptions + 1
        if num_meanings > 0:
            review_polarity = review_polarity + (weight/num_meanings)
    if considered_words > 0:
        return review_polarity / considered_words
    return 0