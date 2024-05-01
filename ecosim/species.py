from math import ceil as ceiling
from constants import DAYS_PER_MONTH, DAYS_PER_YEAR


class Species:
    def __init__(self, identifier, info_dictionary):
        self.days_as_adult = int(info_dictionary["days_as_adult"])
        self.id = identifier
        self.morsel_intake = float(info_dictionary["morsel_intake"])
        self.morsel_value = float(info_dictionary["morsel_value"])
        self.name = info_dictionary["name"]

        self.diet = []
        for id in info_dictionary["diet"]:
            self.diet.append(int(id))

        birthrate = int(info_dictionary["birthrate"])
        if info_dictionary["birthrate_unit"] == "year":
            self.new_creatures_per_birth = 1
            self.days_between_births = int(ceiling(DAYS_PER_YEAR / birthrate))
        elif info_dictionary["birthrate_unit"] == "month":
            self.new_creatures_per_birth = 1
            self.days_between_births = int(ceiling(DAYS_PER_MONTH / birthrate))
        else:
            self.new_creatures_per_birth = birthrate
            self.days_between_births = 1

        print(
            f"{self.name}: {self.new_creatures_per_birth} | {self.days_between_births}"
        )
