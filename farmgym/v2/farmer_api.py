class Farmer_API:
    def __init__(self):
        self.name = "Farmer"
        self.fields = {}

    def assign_field(self, field):
        self.fields[field.name] = field

    def perform_action(self, fi_key, entity_key, action, params):
        observations = []
        return observations

    def perform_observation(self, fi_key, entity, variable_key, path):
        observations = []
        return observations

    def update_to_next_day(self):
        ()

    def __str__(self):
        s = self.name
        return s
