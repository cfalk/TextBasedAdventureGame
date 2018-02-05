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

    def determine_bias(self, other, game_graph):
            # Determine if the other character directly hates this character.
            bias_vals = []
            bias_vals.append(other.alliances.get(self, 0))

            for alliance, personal_bias in self.alliances.items():
                alliance_biases = game_graph.alliance_map.get(alliance, {})

                for other_alliance, other_bias in other.alliances.items():
                    if other_alliance in alliance_biases:
                        alliance_bias = alliance_biases[other_alliance]
                        bias = personal_bias * other_bias * alliance_bias
                        bias_vals.append(bias)

            # Average all biases to determine overall character bias.
            bias_calc = sum(bias_vals) / len(bias_vals) if bias_vals else 0
            return bias_calc
