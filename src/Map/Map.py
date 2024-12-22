import math
import networkx as nx
import matplotlib.pyplot as plt
from Map.Place import Place
from Map.Road import Road

class Map:
    def __init__(self, directed=False):
        self.places: list[Place] = []  # Lista de nós (Places)
        self.roads: list[Road] = []    # Lista de estradas (Roads)
        self.directed = directed
        self.heuristics = {}           # Heurísticas para algoritmos de busca

    def __str__(self):
        out = "Estradas:\n"
        for road in self.roads:
            out += str(road) + "\n"
        return out

    def get_node_by_name(self, name):
        for place in self.places:
            if place.getName() == name:
                return place
        return None

    def add_place(self, name):
        place = self.get_node_by_name(name)
        if not place:
            place = Place(name)
            place.setId(len(self.places))  # Define um ID sequencial para o nó
            self.places.append(place)
        return place

    def add_road(self, origin, destination, weight):
        origin_place = self.add_place(origin)
        destination_place = self.add_place(destination)

        # Adiciona a estrada ao grafo
        road = Road(origin_place.getName(), destination_place.getName(), weight)
        self.roads.append(road)

        if not self.directed:
            # Adiciona a estrada reversa para grafos não direcionados
            reverse_road = Road(destination_place.getName(), origin_place.getName(), weight)
            self.roads.append(reverse_road)

    def getNeighbours(self, node_name):
        neighbours = []
        for road in self.roads:
            if road.origin == node_name:
                neighbours.append((road.destination, road.weight))
        return neighbours

    def calcula_custo(self, caminho):
        custo = 0
        for i in range(len(caminho) - 1):
            origem, destino = caminho[i], caminho[i + 1]
            for road in self.roads:
                if road.origin == origem and road.destination == destino:
                    custo += road.weight
                    break
        return custo

    def add_heuristica(self, node_name, estima):
        self.heuristics[node_name] = estima

    def getH(self, node_name):
        return self.heuristics.get(node_name, math.inf)

    def desenha(self):
        g = nx.Graph()

        # Adiciona os nós
        for place in self.places:
            g.add_node(place.getName())

        # Adiciona as arestas
        for road in self.roads:
            g.add_edge(road.origin, road.destination, weight=road.weight)

        pos = nx.spring_layout(g)
        nx.draw_networkx(g, pos, with_labels=True, font_weight='bold')
        labels = nx.get_edge_attributes(g, 'weight')
        nx.draw_networkx_edge_labels(g, pos, edge_labels=labels)
        plt.show()