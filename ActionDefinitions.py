from IoDevice import IO
from Character import Character
from Action import Action


class BattleDefinition(Action):
    description_id = "DESCRIPTION:PROCEED-TOWARDS-BATTLE"

    def enact(self, game_graph):
        IO.out("INITIATE_COMBAT")


class CreatePlayableCharacterDefinition(Action):
    def enact(self, game_graph):
        name = IO.input("REQUEST_CHARACTER_NAME")
        new_char = Character(name)
        game_graph.playable_characters.append(new_char)
        IO.out("GOOD_TO_MEET_YOU", raw_kwargs={"character_name": name})


class ChangeSceneDefinition(Action):
    description_id = "DESCRIPTION:ACTION-CHANGE-SCENE"

    def enact(self, game_graph):
        IO.out("TRAVELING")
        target_scene = self.stored_kwargs["target_scene_id"]
        game_graph.current_scene = game_graph.scene_map[target_scene]


class HealCharactersDefinition(Action):
    def enact(self, game_graph):
        for character in game_graph.playable_characters:
            character.current_health = character.max_health
