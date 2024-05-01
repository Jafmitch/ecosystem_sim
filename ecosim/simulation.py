from os import mkdir as create_directory
from pathlib import Path
from shutil import rmtree as remove_directory_and_contents
from yaml import (
    dump as object_to_yaml_string,
    load as yaml_string_to_object,
    BaseLoader,
)

from constants import DAYS_PER_MONTH
from species import Species


class Simulation:
    def __init__(self, start_file_path):
        self.day = 1
        self.month = 1
        self.month_info = {"month": self.month, "days": []}
        self.name = "simulation"
        self.species_list = []

        with open(start_file_path, mode="r") as start_file:
            for species_info in yaml_string_to_object(start_file.read(), BaseLoader):
                new_species = Species(len(self.species_list), species_info)
                self.species_list.append(new_species)

    def add_creature(self, species):
        pass

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

        for species in self.species_list:
            day_info["species"][species.id] = {
                "name": species.name,
                "count": species.get_number(),
            }

        self.month_info["days"].append(day_info)

    def _resolve_day(self):
        # increase age
        for species in self.species_list:
            species.increase_age()

        # feed
        for species in self.species_list:
            species.feed(self.species_list)

        # reproduce
        for species in self.species_list:
            species.reproduce()
