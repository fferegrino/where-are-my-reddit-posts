from nltk.sentiment import vader

sia = vader.SentimentIntensityAnalyzer()

def vader_sentiment(text):
    return sia.polarity_scores(text)

    """
    https://github.com/cjhutto/vaderSentiment#about-the-scoring
    The compound score is computed by summing the valence scores of each word in the lexicon,
    adjusted according to the rules, and then normalized to be between -1 (most extreme negative) and +1 (most extreme positive).
    This is the most useful metric if you want a single unidimensional measure of sentiment for a given sentence.
    Calling it a 'normalized, weighted composite score' is accurate.
    """