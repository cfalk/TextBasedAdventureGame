import json
import random
import os.path

LANGUAGE_DIR = "languages"
LANGUAGE = "english"

UNKNOWN_RESPONSE = "???"


class Lexicon:
    def __init__(self):
        file_name = "{}.json".format(LANGUAGE)
        language_file_path = os.path.join(LANGUAGE_DIR, file_name)

        with open(language_file_path) as language_file:
            self.lex_dictionary = json.load(language_file)

    def get(self, key):
        try:
            blurb = self.lex_dictionary.get(key)
            return random.choice(blurb) if type(blurb) == list else blurb
        except Exception:
            return UNKNOWN_RESPONSE