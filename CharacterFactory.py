import json

from Character import Character
from glob import glob
from os import path

CHAR_TEMPLATE_DIR = "character_templates"
CHAR_TEMPLATE_REGEX = "*.json"


class CharacterFactory():
    def __init__(self):
        self.character_map = {}
        file_matcher = path.join(CHAR_TEMPLATE_DIR, CHAR_TEMPLATE_REGEX)
        for file_path in glob(file_matcher):
            with open(file_path) as template_file:
                map_portion = json.load(template_file)
                self.character_map.update(map_portion)

    def build(self, character_id, level=1, char_overrides={}):
        # Generate a new character.
        template = self.character_map[character_id]
        character = Character(template)

        for stat, value in char_overrides.items():
            setattr(character, stat, value)

        # Level up the character.
        for i in range(character.level, level):
            character.level_up()

        return character


CHAR_FACTORY = CharacterFactory()
