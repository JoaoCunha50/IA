import math
import networkx as nx
import matplotlib.pyplot as plt
from Map.Place import Place
from Map.Road import Road
from Map.Heuristic import Heuristic
from collections import deque
import random
import heapq


class Map:
    def __init__(self, heuristics, directed=False):
        self.places: list[Place] = []  # Lista de nós (Places)
        self.roads: list[Road] = []    # Lista de estradas (Roads)
        self.directed = directed
        self.heuristics = heuristics           # Heurísticas para algoritmos de busca

    def __str__(self):
        out = "Estradas:\n"
        for road in self.roads:
            out += str(road) + "\n"
        return out
    
    def getPlaces(self):
        return self.places

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

    def procura_DFS(self, start, end, path=None, visited=None):
        # Inicializar as variáveis path e visited apenas na primeira chamada
        if path is None:
            path = []
        if visited is None:
            visited = set()

        # Adicionar o nó inicial ao caminho e ao conjunto de visitados
        path.append(start)
        visited.add(start)

        # Verificar se o nó inicial é o nó final
        if start == end:
            # Calcular o custo do caminho usando a função calcula_custo
            custoT = self.calcula_custo(path)
            return (path, custoT, visited)

        # Iterar sobre as estradas conectadas ao nó atual
        for road in self.roads:
            if road.origin == start:
                adjacente = road.destination
            elif not self.directed and road.destination == start:
                adjacente = road.origin
            else:
                continue

            # Verificar se a estrada está bloqueada
            if road.blocked:
                continue  # Pula esta estrada se estiver bloqueada

            if adjacente not in visited:
                # Chamada recursiva para o nó adjacente
                resultado, custo, visitados_atualizados = self.procura_DFS(adjacente, end, path, visited)
                if resultado is not None:
                    return resultado, custo, visitados_atualizados

        # Remover o nó atual do caminho se não levar a uma solução
        path.pop()
        return None, None, None       

    def dfs_multiple_dest(self, initial_node, destinations):
        """
        Executa DFS para múltiplos destinos.
        
        Args:
            initial_node: Nó inicial
            destinations: Lista de nós destino
            
        Returns:
            Dictionary com destino como chave e tupla (caminho, custo, ordem_expansão) como valor
        """
        results = {}
        
        for dest in destinations:
            # Executa UCS para cada destino
            path, cost, visited = self.procura_DFS(initial_node, dest)
            
            # Guarda os resultados num dicionário
            results[dest] = (path, cost, visited)
        
        return results
    
    def procura_BFS(self, start, end):
        # Inicializar a fila e as estruturas auxiliares
        queue = deque([(start, [start])])  # Cada elemento é (nó_atual, caminho_até_agora)
        visited = set()  # Conjunto para rastrear os nós visitados

        while queue:
            current_node, path = queue.popleft()  # Retira o primeiro elemento da fila

            # Verificar se chegamos ao destino
            if current_node == end:
                custoT = self.calcula_custo(path)  # Calcular o custo do caminho encontrado
                return path, custoT, visited

            # Marcar o nó atual como visitado
            visited.add(current_node)

            # Explorar os vizinhos do nó atual
            for road in self.roads:
                if road.origin == current_node:
                    adjacente = road.destination
                elif not self.directed and road.destination == current_node:
                    adjacente = road.origin
                else:
                    continue

                # Verificar se a estrada está bloqueada
                if road.blocked:
                    continue  # Pula esta estrada se estiver bloqueada

                # Adicionar o vizinho à fila se ainda não foi visitado
                if adjacente not in visited:
                    queue.append((adjacente, path + [adjacente]))

        # Retornar None se nenhum caminho for encontrado
        return None, 0, visited
    
    def bfs_multiple_dest(self, initial_node, destinations):
        """
        Executa BFS para múltiplos destinos.

        Args:
            initial_node: Nó inicial
            destinations: Lista de nós destino

        Returns:
            Dictionary com destino como chave e tupla (caminho, custo, ordem_expansão) como valor
        """
        results = {}

        for dest in destinations:
            # Executa BFS para cada destino
            path, cost, visited = self.procura_BFS(initial_node, dest)

            # Guarda os resultados num dicionário
            results[dest] = (path, cost, visited)

        return results

    

    def ucs_multiple_dest(self, initial_node, destinations):
        """
        Executa UCS para múltiplos destinos.
        
        Args:
            initial_node: Nó inicial
            destinations: Lista de nós destino
            
        Returns:
            Dictionary com destino como chave e tupla (caminho, custo, ordem_expansão) como valor
        """
        results = {}
        
        for dest in destinations:
            # Executa UCS para cada destino
            path, cost, expansion = self.uniform_cost_search(initial_node, dest)
            
            # Guarda os resultados num dicionário
            results[dest] = (path, cost, expansion)
        
        return results
        

    def uniform_cost_search(self, initial_node, goal):
        open_list = []
        heapq.heappush(open_list, (0, initial_node))  # Lista de prioridade
        closed_list = set()  # Conjunto de nós já visitados
        parents = {}  # Para reconstruir o caminho
        g = {initial_node: 0}  # Dicionário com o custo acumulado para cada nó
        expansion_order = []  # Lista para armazenar a ordem de expansão dos nós

        while open_list:
            cost, current_node = heapq.heappop(open_list)  # Extraímos o nó com o menor custo

            if current_node in closed_list:
                continue
            
            closed_list.add(current_node)  # Marcamos o nó como visitado
            expansion_order.append(current_node)  # Adiciona o nó à ordem de expansão

            if current_node == goal:  # Se encontramos o objetivo
                reconst_path = []
                while current_node != initial_node:
                    reconst_path.append(current_node)
                    current_node = parents[current_node]
                reconst_path.append(initial_node)
                reconst_path.reverse()
                return reconst_path, round(g[goal], 2), expansion_order  # Retorna o caminho, custo total e ordem de expansão

            for neighbour, weight in self.getNeighbours(current_node):
                can_pass = True  # Assume-se que a estrada está livre, até que se prove o contrário

                # Verifica se a estrada está bloqueada
                for road in self.roads:
                    if road.origin == current_node and road.destination == neighbour:
                        if road.blocked:
                            can_pass = False  # Se a estrada estiver bloqueada, não podemos seguir esse vizinho
                        break  # Não precisa verificar mais estradas para esse par origem-destino
                    
                # Se a estrada não está bloqueada, podemos considerar o vizinho
                if can_pass:
                    new_cost = g[current_node] + weight  # Cálculo do novo custo
                    if neighbour not in closed_list and (neighbour not in g or new_cost < g[neighbour]):
                        g[neighbour] = new_cost  # Atualiza o custo total até o vizinho
                        heapq.heappush(open_list, (new_cost, neighbour))  # Adiciona o vizinho à lista de prioridade
                        parents[neighbour] = current_node  # Marca o nó atual como pai do vizinho

        return None, 0, expansion_order  # Retorna None se o objetivo não for encontrado, além da ordem de expansão


        
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

    ######################################
    #          Procura Informada         #
    ######################################
    
    def calcula_est(self, estima):
        l = list(estima.keys())
        min_estima = estima[l[0]]
        node = l[0]
        for k, v in estima.items():
            if v < min_estima:
                min_estima = v
                node = k
        return node
    
    def procura_aStar(self, start, end):
        # open_list is a list of nodes which have been visited, but whose neighbors
        # haven't all been inspected; starts off with the start node
        open_list = {start}
        closed_list = set([])

        # g contains current distances from start_node to all other nodes
        # the default value (if it's not found in the map) is +infinity
        g = {}
        g[start] = 0

        # parents contains an adjacency map of all nodes
        parents = {}
        parents[start] = start
        n = None

        while len(open_list) > 0:
            # Find a node with the lowest value of f() - evaluation function
            calc_heurist = {}
            flag = 0
            for v in open_list:
                if n is None:
                    n = v
                else:
                    flag = 1
                    calc_heurist[v] = g[v] + self.heuristics.getHeuristic(v, end)
            if flag == 1:
                min_estima = self.calcula_est(calc_heurist)
                n = min_estima
            if n is None:
                print('Path does not exist!')
                return None

            # If the current node is the stop_node
            # then we begin reconstructing the path from it to the start_node
            if n == end:
                reconst_path = []
                while parents[n] != n:
                    reconst_path.append(n)
                    n = parents[n]
                reconst_path.append(start)
                reconst_path.reverse()
                open_list.update(closed_list)

                return (reconst_path, self.calcula_custo(reconst_path), open_list)

            # For all neighbors of the current node
            for road in self.roads:
                # Check if the road is relevant (connected to `n`) and not blocked
                if (road.origin == n or road.destination == n) and not road.blocked:
                    m = road.destination if road.origin == n else road.origin
                    weight = road.weight

                    # If the current node isn't in both open_list and closed_list
                    # add it to open_list and note `n` as its parent
                    if m not in open_list and m not in closed_list:
                        open_list.add(m)
                        parents[m] = n
                        g[m] = g[n] + weight

                    # Otherwise, check if it's quicker to first visit `n`, then `m`
                    # and if it is, update parent data and g data
                    # and if the node was in the closed_list, move it to open_list
                    else:
                        if g[m] > g[n] + weight:
                            g[m] = g[n] + weight
                            parents[m] = n

                            if m in closed_list:
                                closed_list.remove(m)
                                open_list.add(m)

            # Remove `n` from the open_list, and add it to closed_list
            # because all of its neighbors were inspected
            open_list.remove(n)
            closed_list.add(n)

        print('Path does not exist!')
        return (None,0,open_list)


    def aStar_multiple_dest(self, initial_node, destinations):
        """
        Executa A* para múltiplos destinos.

        Args:
            initial_node: Nó inicial
            destinations: Lista de nós destino

        Returns:
            Dicionário com destino como chave e tupla (caminho, custo, ordem_expansão) como valor
        """
        results = {}

        for dest in destinations:
            # Executa A* para cada destino
            path, cost, expansion = self.procura_aStar(initial_node, dest)

            # Guarda os resultados num dicionário
            results[dest] = (path, cost, expansion)

        return results

    def procura_gulosa(self, start, end):
        # open_list is a list of nodes which have been visited, but whose neighbors haven't all been inspected
        open_list = {start}
        closed_list = set([])

        # parents contains an adjacency map of all nodes
        parents = {}
        parents[start] = start
        n = None

        while len(open_list) > 0:
            # Find a node with the lowest heuristic value
            calc_heurist = {}
            for v in open_list:
                calc_heurist[v] = self.heuristics.getHeuristic(v, end)
            n = min(calc_heurist, key=calc_heurist.get)

            if n is None:
                print('Path does not exist!')
                return (None, 0, open_list)

            # If the current node is the stop_node
            # then we begin reconstructing the path from it to the start_node
            if n == end:
                reconst_path = []
                while parents[n] != n:
                    reconst_path.append(n)
                    n = parents[n]
                reconst_path.append(start)
                reconst_path.reverse()
                open_list.update(closed_list)
                return (reconst_path, self.calcula_custo(reconst_path), open_list)

            # For all neighbors of the current node
            for road in self.roads:
                # Check if the road is relevant (connected to `n`) and not blocked
                if (road.origin == n or road.destination == n) and not road.blocked:
                    m = road.destination if road.origin == n else road.origin

                    # If the current node isn't in both open_list and closed_list
                    # add it to open_list and note `n` as its parent
                    if m not in open_list and m not in closed_list:
                        open_list.add(m)
                        parents[m] = n

            # Remove `n` from the open_list, and add it to closed_list
            open_list.remove(n)
            closed_list.add(n)

        print('Path does not exist!')
        return (None, 0, open_list)

    def greedy_multiple_dest(self, initial_node, destinations):
        """
        Executa Greedy para múltiplos destinos.

        Args:
            initial_node: Nó inicial
            destinations: Lista de nós destino

        Returns:
            Dicionário com destino como chave e tupla (caminho, custo, ordem_expansão) como valor
        """
        results = {}

        for dest in destinations:
            # Executa A* para cada destino
            path, cost, expansion = self.procura_gulosa(initial_node, dest)

            # Guarda os resultados num dicionário
            results[dest] = (path, cost, expansion)

        return results
    
    def procura_hill_climbing(self, start, end):
        current_node = start
        closed_list = {start}

        # parents contains an adjacency map of all nodes
        parents = {}
        parents[start] = start

        while current_node != end:
            neighbors = []
            for road in self.roads:
                if (road.origin == current_node or road.destination == current_node) and not road.blocked:
                    neighbors.append(road.destination if road.origin == current_node else road.origin)

            # Find the neighbor with the lowest heuristic value
            next_node = None
            lowest_heuristic = float('inf')
            for neighbor in neighbors:
                if neighbor not in closed_list:
                    heuristic_value = self.heuristics.getHeuristic(neighbor, end)
                    if heuristic_value < lowest_heuristic:
                        lowest_heuristic = heuristic_value
                        next_node = neighbor

            if next_node is None:
                print('Path does not exist!')
                return (None, 0, closed_list)

            parents[next_node] = current_node
            closed_list.add(next_node)
            current_node = next_node

        # Reconstruct the path
        reconst_path = []
        while parents[current_node] != current_node:
            reconst_path.append(current_node)
            current_node = parents[current_node]
        reconst_path.append(start)
        reconst_path.reverse()

        return (reconst_path, self.calcula_custo(reconst_path), closed_list)

    def hillClimbing_multiple_dest(self, initial_node, destinations):
        """
        Executa Hill Climbing para múltiplos destinos.

        Args:
            initial_node: Nó inicial
            destinations: Lista de nós destino

        Returns:
            Dicionário com destino como chave e tupla (caminho, custo, ordem_expansão) como valor
        """
        results = {}

        for dest in destinations:
            # Executa A* para cada destino
            path, cost, expansion = self.procura_hill_climbing(initial_node, dest)

            # Guarda os resultados num dicionário
            results[dest] = (path, cost, expansion)

        return results
    
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
