from IoDevice import IO
from CharacterFactory import CHAR_FACTORY
from Action import Action


class InitiateBattleDefinition(Action):
    description_id = "DESCRIPTION:PROCEED-TOWARDS-BATTLE"

    def enact(self, game_graph):
        # Change the scene to the scene hosting the battle.
        target_battle = self.stored_kwargs["target_battle_id"]
        battle_scene = game_graph.scene_map[target_battle]
        game_graph.current_scene = battle_scene

        # Construct all predefined characters and apply to the scene.
        scene_characters = []
        for char_outline in self.stored_kwargs["characters"]:
            id = char_outline["id"]
            level = char_outline["level"]
            overrides = char_outline.get("char_overrides", {})
            new_char = CHAR_FACTORY.build(id, level, char_overrides=overrides)
            scene_characters.append(new_char)
        battle_scene.attributes["other_characters"] = scene_characters

        # Determine Initiative.
        all_chars = game_graph.playable_characters + scene_characters
        battle_scene.attributes["initiative"] = all_chars


class AttackDefinition(Action):
    description_id = "DESCRIPTION:ACTION-ATTACK"
    def enact(self, game_graph):
        pass


class CreatePlayableCharacterDefinition(Action):
    def enact(self, game_graph):
        name = IO.input("REQUEST_CHARACTER_NAME")
        race = IO.input("REQUEST_CHARACTER_RACE")

        overrides = {"playable": True, "name": name}
        new_char = CHAR_FACTORY.build(race.upper(), char_overrides=overrides)
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
            character.current_stats["hp"] = character.stats["hp"]
