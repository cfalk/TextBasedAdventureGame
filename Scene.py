from IoDevice import IO


class Scene:
    def __init__(self, scene_json, action_map):
        self.scene_id = scene_json.get("Id")
        self.pre_scene_actions = [action_map[a_id].build(**a_args) for (a_id, a_args) in scene_json.get("PreSceneActions")]
        self.actions = [action_map[a_id].build(**a_args) for (a_id, a_args) in scene_json.get("Actions")]

    def proceed(self, game_graph):
        # Perform any forced actions
        for action in self.pre_scene_actions:
            action.enact(game_graph)

        # Provide Description for this Scene
        IO.out(self.get_id())

        # Reveal Action Choices
        IO.out("PROMPT_CHOICES")
        for option_num, action in enumerate(self.actions):
            prefix = "{}.) ".format(option_num + 1)
            IO.out(action.description_id, prefix=prefix, kwargs_to_translate=action.stored_kwargs)

        # Choose a Choice.
        while(True):
            chosen_index = IO.input(force_type=int)
            if 1 <= chosen_index <= len(self.actions):
                break
            else:
                IO.out("INVALID_INPUT_WARNING")

        self.actions[chosen_index - 1].enact(game_graph)

    def get_id(self):
        return self.scene_id
