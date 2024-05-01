class Creature:
    def __init__(self, identifier, species):
        self.days_until_death = species.days_as_adult
        self.days_until_reproduction = species.days_between_births
        self.id = identifier
        self.species = species
        self.status = "alive"

    def feed(self, meal_list):
        morsels_remaining = self.species.morsel_intake
        for meal in meal_list:
            if morsels_remaining <= 0:
                return

            if (
                meal.id != self.id
                and meal.species.id in self.species.diet
                and meal.status == "alive"
            ):
                meal.status = "consumed"
                morsels_remaining -= meal.species.morsel_value
        # Died of starvation
        self.status = "dead"

    def increase_age(self):
        if self.days_until_death <= 0:
            # Died of old age
            self.status = "dead"
        self.days_until_death -= 1

    def reproduce(self):
        if self.days_until_reproduction <= 0:
            self.days_until_reproduction = self.species.days_between_births
            return self.species.new_creatures_per_birth

        self.days_until_reproduction -= 1
        return 0
