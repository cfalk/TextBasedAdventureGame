from random import random
from math import floor
from copy import deepcopy


class Character:
    def __init__(self, template):
        self.playable = False
        self.level = 1
        self.experience = 0
        self.alliances = deepcopy(template.get("alliances", {}))

        self.growth_rates = deepcopy(template["growth_rates"])
        self.stats = deepcopy(template["base_stats"])
        self.current_stats = deepcopy(template["base_stats"])

    def level_up(self):
        for stat, rate in self.growth_rates.items():
            change = floor(rate)
            if (random() > (rate - change)):
                change += 1
            self.stats[stat] += change
            self.current_stats[stat] += change

        self.level += 1
        self.experience = 0
