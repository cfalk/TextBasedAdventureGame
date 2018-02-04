import os.path

from Game import Game
from IoDevice import IO

TEMPLATE_DIR = "game_templates"
GAME_TEMPLATE = "test-game.json"

SAVE_EXTENSION = "gamefile"
SAVE_DIR = "games"


def run():
    # Determine a save location.
    save_name = IO.input("GAME_GREETING")
    save_file = "{}.{}".format(save_name, SAVE_EXTENSION)
    save_path = os.path.join(SAVE_DIR, save_file)

    # Determine the game template location.
    game_path = os.path.join(TEMPLATE_DIR, GAME_TEMPLATE)

    game = Game(game_path, save_path)

    while (game.can_proceed()):
        game.proceed()
        game.save()
    game.terminate()


if __name__ == "__main__":
    run()