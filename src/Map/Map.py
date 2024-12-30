import math
import networkx as nx
import matplotlib.pyplot as plt
from Map.Place import Place
from Map.Road import Road
from collections import deque
import random

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

    def add_road(self, origin, destination, weight, allowed):
        origin_place = self.add_place(origin)
        destination_place = self.add_place(destination)

        # Gera o valor de blocked aleatoriamente
        blocked = random.random() < 0.15

        # Adiciona a estrada ao grafo com o valor de blocked
        road = Road(origin_place.getName(), destination_place.getName(), weight, allowed, blocked)
        self.roads.append(road)

        if not self.directed:
            # Adiciona a estrada reversa com o mesmo valor de blocked
            reverse_road = Road(destination_place.getName(), origin_place.getName(), weight, allowed, blocked)
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


    def bfs_search(self, start, goal, vehicle):
        visited = set()
        fila = deque()
        parent = dict()
        tempo_total = dict()
    
        # Configuração inicial
        fila.append(start)
        parent[start] = None
        tempo_total[start] = 0
        vehicle_type = vehicle.getType()
        path_found = False
    
        # Processo de busca
        while fila and not path_found:
            current_node = fila.popleft()
            print(f"A explorar nodo: {current_node}")
    
            # Só adicionamos aos visitados quando realmente exploramos o nodo
            visited.add(current_node)
    
            if current_node == goal:
                path_found = True
            else:
                for neighbour, _ in self.getNeighbours(current_node):
                    if neighbour not in visited and neighbour not in fila:  # Change here
                        can_pass = False
                        for road in self.roads:
                            if road.origin == current_node and road.destination == neighbour:
                                if not road.blocked and road.canVehiclePass(vehicle_type):
                                    can_pass = True
                                    tempo = self.calculaTempo(vehicle, road)
                                    break
                                
                        if can_pass:
                            fila.append(neighbour)
                            parent[neighbour] = current_node
                            tempo_total[neighbour] = tempo_total[current_node] + tempo
    
        # Reconstruir o caminho
        path = []
        if path_found:
            current = goal
            while current is not None:
                path.append(current)
                current = parent[current]
            path.reverse()
            return path, tempo_total[goal], visited
    
        return None, 0, visited
    

    def dfs_search(self, start, goal, vehicle):
        stack = [(start, [start], 0)]
        visited = set()
        vehicle_type = vehicle.getType()

        while stack:
            currentNode, path, tempo_total = stack.pop()

            if currentNode == goal:
                return path, tempo_total

            if currentNode not in visited:
                visited.add(currentNode)
                for neighbour, _ in self.getNeighbours(currentNode):
                    if neighbour not in visited:
                        for road in self.roads:
                            if road.origin == currentNode and road.destination == neighbour:
                                if road.blocked or not road.canVehiclePass(vehicle_type):
                                    break
                        else:
                            for road in self.roads:
                                if road.origin == currentNode and road.destination == neighbour:
                                    tempo = self.calculaTempo(vehicle, road)
                                    stack.append((neighbour, path + [neighbour], tempo_total + tempo))

        return None, 0



    def calculaTempo(self, vehicle, road):
        # Obtém o peso (distância) da estrada
        distancia = road.getWeight()
        origem = road.getOrigin()
        dest = road.getDestination()

        # Obtém a capacidade do veículo (não usada no cálculo de tempo em minutos)
        capacidade = vehicle.getCapacity()

        # Obtém a velocidade média do veículo
        velocidade_media = vehicle.getSpeed()

        # Exibe os valores para debug
        print()
        print(f"Origem da estrada: {origem}")
        print(f"Destino da estrada: {dest}")
        print(f"Distância da estrada: {distancia} km")
        print(f"Capacidade do veículo: {capacidade} unidades (não utilizada no cálculo de tempo)")
        print(f"Velocidade média do veículo: {velocidade_media} km/h")

        # Cálculo do tempo em horas e conversão para minutos
        tempo_em_horas = distancia / velocidade_media
        tempo_em_minutos = tempo_em_horas * 60  # Converte o tempo de horas para minutos

        # Exibe o resultado do cálculo
        print(f"Tempo calculado: {tempo_em_minutos} minutos")
        print()

        return tempo_em_minutos


    def desenha(self):
        g = nx.Graph()
        
        # Adiciona os nós
        for place in self.places:
            g.add_node(place.getName())
        
        # Adiciona as arestas com cor como atributo
        for road in self.roads:
            # Determina a cor com base no estado de bloqueio
            color = 'red' if road.getBlocked() else 'gray'
            
            # Imprime para debug
            print(f"Origem: {road.origin}, Destino: {road.destination}, Bloqueada: {road.getBlocked()}, Cor: {color}")
            
            # Adiciona a aresta com atributos personalizados
            g.add_edge(road.origin, road.destination, weight=road.weight, color=color)
        
        # Usando o Kamada-Kawai layout com maior espaçamento
        pos = nx.kamada_kawai_layout(g, scale=4)  # Aumentando o 'scale' para maior espaçamento entre os nós
        
        # Estilo para nós
        node_color = '#7D0DC3'  # Cor dos nós
        node_size = 1000  # Tamanho dos nós
        font_size = 12  # Tamanho da fonte nos nós
        font_color = 'black'  # Cor da fonte nos nós
        
        # Estilo para arestas
        edge_width = 3  # Largura maior das arestas (distâncias)
        
        # Recupera as cores das arestas a partir dos atributos
        edge_colors = list(nx.get_edge_attributes(g, 'color').values())
        
        # Estilo para rótulos de arestas (distância/peso)
        edge_labels = nx.get_edge_attributes(g, 'weight')
        edge_label_font_size = 12  # Tamanho da fonte dos rótulos das arestas
        
        # Desenhando a rede
        plt.figure(figsize=(16, 14))  # Aumentando ainda mais o tamanho da figura
        nx.draw_networkx(g, pos, with_labels=True, node_size=node_size, font_weight='bold', 
                         node_color=node_color, font_size=font_size, font_color=font_color, 
                         edge_color=edge_colors, width=edge_width)  # Usando as cores das arestas recuperadas
        
        # Desenhando os rótulos das arestas (pesos)
        nx.draw_networkx_edge_labels(g, pos, edge_labels=edge_labels, font_size=edge_label_font_size, font_color='#B95CF4')
        
        # Melhorando o layout visual
        plt.title("PathFinder", fontsize=16, fontweight='bold', color='#7D0DC3')
        plt.axis('on')  # Desativa o eixo para uma visualização mais limpa
        
        # Exibe o gráfico
        plt.show()

    

