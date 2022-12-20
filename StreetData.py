class StreetData:
    def __init__(self, street_name):
        self.street_name = street_name
        self.id_to_from = {}

    def add_to_id_to_from(self, id, edge_to, edge_from):
        self.id_to_from[id] = (edge_to, edge_from)