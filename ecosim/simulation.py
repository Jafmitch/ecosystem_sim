from os import mkdir as create_directory
from pathlib import Path
from shutil import rmtree as remove_directory_and_contents
from yaml import (
    dump as object_to_yaml_string,
    load as yaml_string_to_object,
    BaseLoader,
)

from constants import DAYS_PER_MONTH
from creature import Creature
from species import Species


class Simulation:
    def __init__(self, start_file_path):
        self.creature_list = []
        self.day = 1
        self.month = 1
        self.month_info = {"month": self.month, "days": []}
        self.name = "simulation"
        self.next_creature_id = 0
        self.species_list = []

        with open(start_file_path, mode="r") as start_file:
            for species_info in yaml_string_to_object(start_file.read(), BaseLoader):
                new_species = Species(len(self.species_list), species_info)
                for _ in range(int(species_info.get("count", 0))):
                    self.add_creature(new_species)

                self.species_list.append(new_species)

    def add_creature(self, species):
        self.creature_list.append(Creature(self.next_creature_id, species))
        self.next_creature_id += 1

    def finish(self):
        if self.day > 1:
            self.log_current_month()
        print("Simulation finished!")

    def next_day(self):
        self._resolve_day()
        self._record_day()

        if self.day == DAYS_PER_MONTH:
            self.log_current_month()
            self.day = 1
            self.month += 1
            self.month_info = {"month": self.month, "days": []}
        else:
            self.day += 1

    def log_current_month(self):
        with open(Path(self.name) / f"month_{self.month}.yml", "w") as log_file:
            log_file.write(object_to_yaml_string(self.month_info))

    def start(self):
        print("Starting simulation")
        directory = Path(self.name)

        if directory.exists():
            remove_directory_and_contents(directory)

        create_directory(directory)

    def _record_day(self):
        day_info = {"day": self.day, "species": {}}
        for creature in self.creature_list:
            if creature.status != "alive":
                pass
            elif day_info["species"].get(creature.species.id) is None:
                day_info["species"][creature.species.id] = {
                    "name": creature.species.name,
                    "count": 1,
                }
            else:
                day_info["species"][creature.species.id]["count"] += 1
        self.month_info["days"].append(day_info)

    def _resolve_day(self):
        for creature in self.creature_list:
            if creature.status == "alive":
                creature.increase_age()

        for creature in self.creature_list:
            if creature.status == "alive":
                creature.feed(self.creature_list)

        for creature in self.creature_list:
            if creature.status == "alive":
                number_born = creature.reproduce()
                for _ in range(number_born):
                    self.add_creature(creature.species)

        # remove the dead
        index = 0
        while index < len(self.creature_list):
            creature = self.creature_list[index]
            if creature.status == "consumed" or creature.status == "dead":
                self.creature_list.pop(index)
            else:
                index += 1
