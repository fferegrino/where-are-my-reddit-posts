from nltk.sentiment import vader

sia = vader.SentimentIntensityAnalyzer()

def vader_sentiment(text:str) -> dict:
    """
    Calculates polarity scores from the given text using VADER's sentiment intensity analyzer
    :param text: the text to analise
    :return: a dictionary containing 4 values: pos, neg, neu, and compound
    """
    return sia.polarity_scores(text)