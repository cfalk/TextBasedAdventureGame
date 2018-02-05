from IoDevice import IO


class Scene:
    def __init__(self, scene_json, action_map):
        self.scene_id = scene_json.get("Id")
        self.pre_scene_actions = [action_map[a_id].build(**a_args) for (a_id, a_args) in scene_json.get("PreSceneActions")]
        self.actions = [action_map[a_id].build(**a_args) for (a_id, a_args) in scene_json.get("Actions")]
        self.attributes = scene_json.get("SceneAttributes", {})

    def proceed(self, game_graph):
        # Perform any forced actions
        for action in self.pre_scene_actions:
            action.enact(game_graph)

        # Provide Description for this Scene
        IO.out(self.get_id())

        # Reveal Action Choices
        description_ids = [a.description_id for a in self.actions]
        kwarg_list = [a.stored_kwargs for a in self.actions]
        chosen_index = IO.choose_option(description_ids, kwarg_list=kwarg_list)
        self.actions[chosen_index - 1].enact(game_graph)

    def get_id(self):
        return self.scene_id
