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
        # Faz uma busca pelo nome no grafo, comparando de forma consistente
        name = name.lower()
        for place in self.places:
            if place.getName() == name:
                return place
        return None

    def add_place(self, name, sup=None):
        # Garante que o nome é comparado de forma consistente
        place = self.get_node_by_name(name)
        if not place:
            # Se não existir, cria um novo nó
            place = Place(name, sup)
            place.setId(len(self.places))  # Define um ID sequencial para o nó
            self.places.append(place)
        else:
            # Se o lugar já existir, atualiza o suplemento (se fornecido)
            if sup:
                place.setSupply(sup)
        return place

    def add_road(self, origin, destination, weight, allowed, suplements):      
        origin_suplement = None
        destination_suplement = None  

        # Verifica suplementos se forem fornecidos
        if suplements:
            origin_suplement = next((sup for sup in suplements if sup.getLocation() == origin), None)
            destination_suplement = next((sup for sup in suplements if sup.getLocation() == destination), None)

            # Remove os suplementos encontrados da lista
            if origin_suplement:
                suplements.remove(origin_suplement)
            if destination_suplement:
                suplements.remove(destination_suplement)

        # Adiciona ou recupera os lugares existentes
        origin_place = self.add_place(origin, origin_suplement)
        destination_place = self.add_place(destination, destination_suplement)

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
            current_nodeObj = self.get_node_by_name(current_node)
            request = current_nodeObj.getQuantity()
            supVehicle = vehicle.getQuantitySup()
            if request is not None and supVehicle is not None:
                if request <= supVehicle:
                    print(f"Entreguei tudo o que a freguesia de {current_node} precisava")
                    current_nodeObj.setQuantity(0)
                    if supVehicle - request <= 0:
                        vehicle.setQuantity(0)
                    else: vehicle.setQuantitySup(supVehicle - request)
                else: 
                    print(f"A freguesia de {current_node} precisa de mais!")
                    vehicle.setQuantitySup(0)
                    current_nodeObj.setQuantity(request - supVehicle)

                path_found = True
            else: # ver isto melhor
            # Tratar caso em que request ou supVehicle sejam None
                print(f"Erro: Request ou Supply do veículo não definidos para o nó {current_node}.")
                path_found = True  # Sinaliza que não é possível continuar
            
         else:
             for neighbour, _ in self.getNeighbours(current_node):
                 if neighbour not in visited and neighbour not in fila:  # Evitar duplicados na fila
                     can_pass = False
                     tempo = 0  # Tempo padrão para calcular o tempo entre os nós

                     for road in self.roads:
                         if road.origin == current_node and road.destination == neighbour:
                             if not road.blocked and road.canVehiclePass(vehicle_type):
                                 can_pass = True
                                 tempo = self.calculaTempo(vehicle, road)  # Calcula o tempo usando a função fornecida
                                 break

                     if can_pass:
                         fila.append(neighbour)
                         parent[neighbour] = current_node
                         tempo_total[neighbour] = tempo_total[current_node] + tempo  # Soma o tempo cumulativo

     # Reconstruir o caminho
     path = []
     if path_found:
         current = goal
         while current is not None:
             path.append(current)
             current = parent[current]
         path.reverse()
         return path, tempo_total[goal], visited  # Retorna o caminho, o tempo total e os nós visitados

     return None, 0, visited



    

    def dfs_search(self, start, goal, vehicle):
        stack = [(start, [start], 0)]  # Pilha que armazena o nó atual, o caminho e o tempo total
        visited = set()  # Conjunto de nós visitados
        vehicle_type = vehicle.getType()  # Tipo do veículo

        # Processo de busca em profundidade
        while stack:
            current_node, path, tempo_total = stack.pop()

            print(f"A explorar nodo: {current_node}")

            if current_node == goal:
                current_nodeObj = self.get_node_by_name(current_node)
                request = current_nodeObj.getQuantity()  # A quantidade necessária no destino
                supVehicle = vehicle.getQuantitySup()  # A quantidade disponível no veículo

                # Verifica se o veículo tem capacidade para atender a demanda
                if request <= supVehicle:
                    print(f"Entreguei tudo o que a freguesia de {current_node} precisava")
                    current_nodeObj.setQuantity(0)  # Atualiza a quantidade no destino para 0
                    if supVehicle - request <= 0:
                        vehicle.setQuantity(0)  # O veículo agora tem 0 de capacidade
                    else:
                        vehicle.setQuantitySup(supVehicle - request)  # Atualiza a quantidade restante no veículo
                else: 
                    print(f"A freguesia de {current_node} precisa de mais!")
                    vehicle.setQuantitySup(0)  # O veículo fica sem capacidade
                    current_nodeObj.setQuantity(request - supVehicle)  # Atualiza a quantidade restante no destino

                visited.add(current_node)  # Marca o goal como visitado
                return path, tempo_total, visited  # Retorna o caminho e o tempo total percorrido até o destino

            # Se o nó não for o destino, exploramos os vizinhos
            if current_node not in visited:
                visited.add(current_node)  # Marca o nó atual como visitado

                for neighbour, _ in self.getNeighbours(current_node):
                    if neighbour not in visited:
                        can_pass = False
                        tempo = 0  # Inicializa o tempo padrão

                        for road in self.roads:
                            if road.origin == current_node and road.destination == neighbour:
                                if not road.blocked and road.canVehiclePass(vehicle_type):
                                    can_pass = True  # Se a estrada não está bloqueada e o veículo pode passar
                                    tempo = self.calculaTempo(vehicle, road)  # Calcula o tempo necessário para percorrer a estrada
                                    break

                        if can_pass:
                            stack.append((neighbour, path + [neighbour], tempo_total + tempo))  # Empilha o vizinho com o caminho e tempo atualizado

        # Se o loop terminar sem encontrar o caminho
        return None, 0, visited

    
    def dfs_search_for_all_vehicles(self, start, goal, vehicles):
        best_path = None
        best_time = float('inf')  # Inicializa o tempo com infinito
        best_vehicle = None

        # Realiza a busca DFS para todos os veículos
        for vehicle in vehicles:
            path, time, visited = self.dfs_search(start, goal, vehicle)
            if path and time < best_time:
                best_path = path
                best_time = time
                best_vehicle = vehicle
                best_visited = visited

        return best_path, best_time, best_vehicle, best_visited

    def bfs_search_for_all_vehicles(self, start, goal, vehicles):
        best_path = None
        best_time = float('inf')  # Inicializa o tempo com infinito
        best_vehicle = None

        # Realiza a busca BFS para todos os veículos
        for vehicle in vehicles:
            path, time, visited = self.bfs_search(start, goal, vehicle)
            if path and time < best_time:
                best_path = path
                best_time = time
                best_vehicle = vehicle
                best_visited = visited

        return best_path, best_time, best_vehicle, best_visited


    def calculaTempo(self, vehicle, road):
        # Obtém o peso (distância) da estrada
        distancia = road.getWeight()
        origem = road.getOrigin()
        dest = road.getDestination()

        # Obtém a capacidade do veículo (não usada no cálculo de tempo em minutos)
        capacidade = vehicle.getCapacity()

        # Obtém a velocidade média do veículo
        velocidade_media = vehicle.getSpeed()

        # Cálculo do tempo em horas e conversão para minutos
        tempo_em_horas = distancia / velocidade_media
        tempo_em_minutos = tempo_em_horas * 60  # Converte o tempo de horas para minutos

        # Arredonda o tempo para 1 casa decimal
        tempo_arredondado = round(tempo_em_minutos, 1)

        return tempo_arredondado



    def desenha(self):
        g = nx.Graph()

        # Adiciona os nós
        for place in self.places:
            g.add_node(place.getName(), urgency_level=place.urgency_level)

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

        # Gradiente de cores (tons de roxo e azul: mais escuro para maior urgência)
        urgency_colors = {
            0: "#E0B0FF",  # Lilás muito claro
            1: "#CDA1FF",  # Lilás claro
            2: "#B48CFF",  # Roxo mais vivo
            3: "#9B77FF",  # Roxo médio
            4: "#814CFF",  # Roxo escuro
            5: "#4B0082",  # Índigo profundo
        }

        # Determina as cores dos nós com base nos níveis de urgência
        node_colors = []
        for place in self.places:
            urgency = place.urgency_level if place.urgency_level is not None else 0  # Default para 0 se não definido
            node_colors.append(urgency_colors.get(urgency, "#E0B0FF"))  # Default para lilás claro se o nível for inválido

        # Estilo para nós
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
        plt.figure(figsize=(16, 16))  # Aumentando ainda mais o tamanho da figura
        nx.draw_networkx(g, pos, with_labels=True, node_size=node_size, font_weight='bold', 
                         node_color=node_colors, font_size=font_size, font_color=font_color, 
                         edge_color=edge_colors, width=edge_width)  # Usando as cores das arestas recuperadas

        # Desenhando os rótulos das arestas (pesos)
        nx.draw_networkx_edge_labels(g, pos, edge_labels=edge_labels, font_size=edge_label_font_size, font_color='#B95CF4')

        # Adicionando legenda para os níveis de urgência
        legend_labels = ["Urgência 0", "Urgência 1", "Urgência 2", "Urgência 3", "Urgência 4", "Urgência 5"]
        legend_colors = [urgency_colors[i] for i in range(6)]

        # Cria os elementos da legenda
        legend_patches = [plt.Line2D([0], [0], color=color, marker='o', markersize=15, linestyle='', label=label) 
                          for color, label in zip(legend_colors, legend_labels)]

        # Adiciona a legenda ao gráfico
        plt.legend(handles=legend_patches, loc='lower center', bbox_to_anchor=(0.5, -0.1), ncol=6, fontsize=12, frameon=False)

        # Melhorando o layout visual
        plt.title("PathFinder", fontsize=16, fontweight='bold', color='#7D0DC3')
        plt.axis('on')  # Desativa o eixo para uma visualização mais limpa

        # Exibe o gráfico
        plt.show()



    

