part_of_the_speech = {
        "CC": "coordinating conjunction",
        "CD": "cardinal number",
        "DT": "determiner",
        "EX": "existential there",
        "FW": "foreign word",
        "IN": "preposition/subordinating conjunction",
        "JJ": "adjective",
        "JJR": "adjective, comparative",
        "JJS": "adjective, superlative",
        "LS": "list marker",
        "MD": "modal",
        "NN": "noun, singular or mass",
        "NNS": "noun plural",
        "NNP": "proper noun, singular",
        "NNPS": "proper noun, plural",
        "PDT": "predeterminer",
        "POS": "possessive ending",
        "PRP": "personal pronoun",
        "PRP$": "possessive pronoun",
        "RB": "adverb",
        "RBR": "adverb, comparative",
        "RBS": "adverb, superlative",
        "RP": "particle",
        "TO": "to",
        "UH": "interjection",
        "VB": "verb, base form",
        "VBD": "verb, past tense",
        "VBG": "verb, gerund/present participle",
        "VBN": "verb, past participle",
        "VBP": "verb, sing. present, non-3d",
        "VBZ": "verb, 3rd person sing. present",
        "WDT": "wh-determiner",
        "WP": "wh-pronoun",
        "WP$": "possessive wh-pronoun",
        "WRB": "wh-abverb"
    }

def translate_pos(pos:str):
    if pos not in part_of_the_speech:
        return "Unknown"
    return part_of_the_speech[pos]