import os
import pickle
import json

from GameGraph import GameGraph


class Game():
    def __init__(self, game_template, save_file_path):
        self.save_file_path = save_file_path

        if os.path.isfile(self.save_file_path):
            # Start a new game if a save exists.
            with open(self.save_file_path, "rb") as save_file:
                self.game_graph = pickle.load(save_file)
        else:
            # Start a brand new game.
            with open(game_template) as game_file:
                self.game_graph = GameGraph(json.load(game_file))
                self.save()

    def proceed(self):
        self.game_graph.proceed()

    def save(self):
        with open(self.save_file_path, "wb") as game_file:
            pickle.dump(self.game_graph, game_file)

    def can_proceed(self):
        return True