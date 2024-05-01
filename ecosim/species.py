from math import ceil as ceiling
from random import choice as get_random_choice, randint as get_random_integer

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

        self.members = [int(info_dictionary["count"])]

    def feed(self, species_list):
        target_morsel_intake = int(self.get_number() * self.morsel_intake)
        morsel_intake = 0
        while morsel_intake < target_morsel_intake:
            species = self._get_random_species_to_eat(species_list)
            if species is None:
                # nothing to eat, creatures starve
                break
            morsel_intake += species.morsel_value
            species.kill()

        if morsel_intake < target_morsel_intake:
            number_to_kill = int(
                (target_morsel_intake - morsel_intake) / self.morsel_intake
            )
            self.kill(number_to_kill)

    def get_number(self):
        return sum(self.members)

    def increase_age(self):
        self.members.insert(0, 0)
        if len(self.members) > self.days_as_adult:
            self.members.pop()

    def kill(self, number_to_kill=1):
        age_options = [age for age, _ in enumerate(self.members)]
        for _ in range(number_to_kill):
            found_member_to_kill = False
            while not found_member_to_kill:
                random_age = get_random_choice(age_options)
                if self.members[random_age] > 0:
                    found_member_to_kill = True
                else:
                    age_options.remove(random_age)
                    if len(age_options) == 0:
                        # no more members left to kill
                        return
            self.members[random_age] -= 1

    def reproduce(self):
        if len(self.members) > self.days_between_births:
            for index, member in enumerate(self.members, self.days_between_births):
                if index % self.days_between_births == 0:
                    self.members[0] += int(member * self.new_creatures_per_birth)

    def _get_random_species_to_eat(self, species_list):
        if len(self.diet) == 0:
            return None

        random_index = get_random_integer(0, len(self.diet) - 1)
        species_to_eat = species_list[self.diet[random_index]]
        if species_to_eat.get_number() != 0:
            return species_to_eat
        else:
            # a species has gone extinct, remove from diet and try again
            self.diet.pop(random_index)
            return self._get_random_species_to_eat(species_list)
