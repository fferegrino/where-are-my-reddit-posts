import preprocessor as pp

def no_cleaning(text):
    return text

def tweet_clean(text):
    pp.set_options(pp.OPT.EMOJI)
    return pp.clean(text)