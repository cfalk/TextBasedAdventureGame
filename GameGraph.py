from Scene import Scene
from Action import ActionBuilder


class GameGraph():
    def __init__(self, game_json):
        self.scene_map = {}

        # Load Actions
        action_builder_map = {}
        for action_json in game_json.get("Actions"):
            a_builder = ActionBuilder(action_json)
            assert_id_not_present(a_builder.get_id(), action_builder_map)
            action_builder_map[a_builder.get_id()] = a_builder

        # Load Scenes
        for scene_json in game_json.get("Scenes"):
            scene = Scene(scene_json, action_builder_map)
            assert_id_not_present(scene.get_id(), self.scene_map)
            self.scene_map[scene.get_id()] = scene

        # Load the Alliance Traits.
        self.alliance_map = game_json.get("Alliances", {})

        # Set the Starting Location
        current_scene_id = game_json.get("InitialScene")
        self.current_scene = self.scene_map[current_scene_id]
        self.playable_characters = []

    def proceed(self):
        self.current_scene.proceed(self)


def assert_id_not_present(id_to_check, dictionary):
    if id_to_check in dictionary:
        error = "VerificationFailed: ID '{}' already used!".format(id_to_check)
        raise Exception(error)