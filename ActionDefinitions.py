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

        def get_least_aligned(character, others, game_graph):
            # Default to the first character.
            least_aligned_char = None
            least_aligned = float("infinity")

            for other in others:
                bias_calc = character.determine_bias(other, game_graph)
                if least_aligned > bias_calc:
                    least_aligned = bias_calc
                    least_aligned_char = other

            return least_aligned_char

        battle_scene = game_graph.current_scene
        combatants = battle_scene.attributes["initiative"]

        for character in combatants:
            if not character.can_take_action():
                continue

            other_combatants = [c for c in combatants if c is not character]
            # TODO: Ask playable characters for target.
            target = get_least_aligned(character, other_combatants, game_graph)
            character.attack(target)


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
