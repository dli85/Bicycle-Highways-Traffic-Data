class StreetData:
    def __init__(self, street_name):
        self.street_name = street_name
        self.id_to_from = {}
        self.edge_ids_list = []
        self.car_edges = []

    def add_to_id_to_from(self, edge_id, edge_to, edge_from, car_edge):
        self.id_to_from[edge_id] = (edge_to, edge_from)
        self.edge_ids_list.append(edge_id)
        if car_edge:
            self.car_edges.append(edge_id)

