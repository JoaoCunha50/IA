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

    def add_road(self, origin, destination, weight, suplements):      
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
        blocked = random.random() < 0.5

        # Adiciona a estrada ao grafo com o valor de blocked
        road = Road(origin_place.getName(), destination_place.getName(), weight, blocked)
        self.roads.append(road)

        if not self.directed:
            # Adiciona a estrada reversa com o mesmo valor de blocked
            reverse_road = Road(destination_place.getName(), origin_place.getName(), weight, blocked)
            self.roads.append(reverse_road)

    def getNeighbours(self, node_name):
        neighbours = []
        for road in self.roads:
            if road.origin == node_name:
                neighbours.append((road.destination, road.weight))
        return neighbours

    def calcula_custo(self, caminho, vehicle):
        custo = 0
        for i in range(len(caminho) - 1):
            origem, destino = caminho[i], caminho[i + 1]
            for road in self.roads:
                if road.origin == origem and road.destination == destino:
                    custo += (road.weight / vehicle.getSpeed())*3600;
                    break
        return custo

    def procura_DFS(self, start, end, vehicle, path=None, visited=None):
        """
        Procura um caminho usando DFS entre start e end, considerando o veículo.
        """

        # Garantir que path e visited sejam inicializados corretamente
        if path is None:
            path = []
        elif not isinstance(path, list):
            path = list(path)

        if visited is None:
            visited = set()
        elif not isinstance(visited, set):
            visited = set(visited)

        # Adicionar o nó inicial ao caminho e ao conjunto de visitados
        path.append(start)
        visited.add(start)

        # Verificar se o nó inicial é o nó final
        if start == end:
            custoT = self.calcula_custo(path, vehicle)
            return path, custoT, visited, vehicle

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
                continue

            # Chamar recursivamente para o nó adjacente
            if adjacente not in visited:
                resultado, custo, visitados_atualizados, vehicle = self.procura_DFS(adjacente, end, vehicle, path, visited)
                if resultado is not None:
                    return resultado, custo, visitados_atualizados, vehicle

        # Se não houver solução, remover o nó atual do caminho
        path.pop()
        return None, None, None, vehicle
   

    def dfs_multiple_dest(self, initial_node, destinations, vehicles):
        """
        Executa DFS para múltiplos destinos considerando veículos diferentes.

        Args:
            initial_node: Nó inicial
            destinations: Lista de nós destino
            vehicles: Lista de veículos

        Returns:
            Dicionário com destino como chave e tupla (caminho, custo, ordem_expansão) como valor
        """
        results = {}
        for dest in destinations:
            # Inicializar com um valor padrão (None para caminho e custo infinito)
            results[dest] = (None, float('inf'), None, None)

            for vehicle in vehicles:
                # Executa DFS para cada veículo e destino
                path, cost, visited, vehicle = self.procura_DFS(initial_node, dest, vehicle)

                # Atualiza o resultado se o custo for menor que o já registrado
                if path is not None and cost < results[dest][1]:
                    results[dest] = (path, cost, visited, vehicle)

        return results

    
    def procura_BFS(self, start, end, vehicle):
        # Inicializar a fila e as estruturas auxiliares
        queue = deque([(start, [start])])  # Cada elemento é (nó_atual, caminho_até_agora)
        visited = set()  # Conjunto para rastrear os nós visitados

        while queue:
            current_node, path = queue.popleft()  # Retira o primeiro elemento da fila

            # Verificar se chegamos ao destino
            if current_node == end:
                custoT = self.calcula_custo(path, vehicle)  # Calcular o custo do caminho encontrado
                return path, custoT, visited, vehicle

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
        return None, 0, visited, vehicle

    def bfs_multiple_dest(self, initial_node, destinations, vehicles):
        """
        Executa BFS para múltiplos destinos considerando veículos diferentes.

        Args:
            initial_node: Nó inicial
            destinations: Lista de nós destino
            vehicles: Lista de veículos

        Returns:
            Dicionário com destino como chave e tupla (caminho, custo, ordem_expansão, veículo) como valor
        """
        results = {}

        for dest in destinations:
            # Inicializar com um valor padrão
            results[dest] = (None, float('inf'), None, None)

            for vehicle in vehicles:
                # Executa BFS para cada veículo e destino
                path, cost, visited, vehicle = self.procura_BFS(initial_node, dest, vehicle)

                # Atualiza o resultado se o custo for menor que o já registrado
                if path is not None and cost < results[dest][1]:
                    results[dest] = (path, cost, visited, vehicle)

        return results


    

    def uniform_cost_search(self, initial_node, goal, vehicle):
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
                custo_total = self.calcula_custo(reconst_path, vehicle)
                return reconst_path, round(custo_total, 2), expansion_order, vehicle  # Retorna o caminho, custo total e ordem de expansão

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

        return None, 0, expansion_order, vehicle  # Retorna None se o objetivo não for encontrado, além da ordem de expansão

    def ucs_multiple_dest(self, initial_node, destinations, vehicles):
        """
        Executa UCS para múltiplos destinos considerando veículos diferentes.
        
        Args:
            initial_node: Nó inicial
            destinations: Lista de nós destino
            vehicles: Lista de veículos

        Returns:
            Dicionário com destino como chave e tupla (caminho, custo, ordem_expansão, veículo) como valor
        """
        results = {}

        for dest in destinations:
            # Inicializar com um valor padrão
            results[dest] = (None, float('inf'), None, None)

            for vehicle in vehicles:
                # Executa UCS para cada veículo e destino
                path, cost, expansion, vehicle = self.uniform_cost_search(initial_node, dest, vehicle)

                # Atualiza o resultado se o custo for menor que o já registrado
                if path is not None and cost < results[dest][1]:
                    results[dest] = (path, cost, expansion, vehicle)

        return results



        
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
    
    def procura_aStar(self, start, end, vehicle):
        open_list = {start}
        closed_list = set([])
        g = {start: 0}
        parents = {start: start}
        n = None

        while len(open_list) > 0:
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

            if n == end:
                reconst_path = []
                while parents[n] != n:
                    reconst_path.append(n)
                    n = parents[n]
                reconst_path.append(start)
                reconst_path.reverse()
                open_list.update(closed_list)
                custoT = self.calcula_custo(reconst_path, vehicle)
                return (reconst_path, custoT, open_list, vehicle)

            for road in self.roads:
                if (road.origin == n or road.destination == n) and not road.blocked:
                    m = road.destination if road.origin == n else road.origin
                    weight = road.weight

                    if m not in open_list and m not in closed_list:
                        open_list.add(m)
                        parents[m] = n
                        g[m] = g[n] + weight
                    else:
                        if g[m] > g[n] + weight:
                            g[m] = g[n] + weight
                            parents[m] = n

                            if m in closed_list:
                                closed_list.remove(m)
                                open_list.add(m)

            open_list.remove(n)
            closed_list.add(n)

        print('Path does not exist!')
        return (None, 0, open_list, vehicle)


    def aStar_multiple_dest(self, initial_node, destinations, vehicles):
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
            results[dest] = (None, float('inf'), None, None)

            for vehicle in vehicles:
                path, cost, expansion, vehicle = self.procura_aStar(initial_node, dest, vehicle)
                if path is not None and cost < results[dest][1]:
                    results[dest] = (path, cost, expansion, vehicle)

        return results


    def procura_gulosa(self, start, end, vehicle):
        open_list = {start}
        closed_list = set([])
        parents = {start: start}
        n = None

        while len(open_list) > 0:
            calc_heurist = {}
            for v in open_list:
                calc_heurist[v] = self.heuristics.getHeuristic(v, end)
            n = min(calc_heurist, key=calc_heurist.get)

            if n is None:
                print('Path does not exist!')
                return (None, 0, open_list, vehicle)

            if n == end:
                reconst_path = []
                while parents[n] != n:
                    reconst_path.append(n)
                    n = parents[n]
                reconst_path.append(start)
                reconst_path.reverse()
                custoT = self.calcula_custo(reconst_path, vehicle)
                return (reconst_path, custoT, open_list, vehicle)

            for road in self.roads:
                if (road.origin == n or road.destination == n) and not road.blocked:
                    m = road.destination if road.origin == n else road.origin
                    if m not in open_list and m not in closed_list:
                        open_list.add(m)
                        parents[m] = n

            open_list.remove(n)
            closed_list.add(n)

        print('Path does not exist!')
        return (None, 0, open_list, vehicle)


    def greedy_multiple_dest(self, initial_node, destinations, vehicles):
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
            results[dest] = (None, float('inf'), None, None)

            for vehicle in vehicles:
                path, cost, expansion, vehicle = self.procura_gulosa(initial_node, dest, vehicle)
                if path is not None and cost < results[dest][1]:
                    results[dest] = (path, cost, expansion, vehicle)

        return results

    
    def procura_hill_climbing(self, start, end, vehicle):
        current_node = start
        closed_list = {start}
        parents = {start: start}

        while current_node != end:
            neighbors = []
            for road in self.roads:
                if (road.origin == current_node or road.destination == current_node) and not road.blocked:
                    neighbors.append(road.destination if road.origin == current_node else road.origin)

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
                return (None, 0, closed_list, vehicle)

            parents[next_node] = current_node
            closed_list.add(next_node)
            current_node = next_node

        reconst_path = []
        while parents[current_node] != current_node:
            reconst_path.append(current_node)
            current_node = parents[current_node]
        reconst_path.append(start)
        reconst_path.reverse()
        custoT = self.calcula_custo(reconst_path, vehicle)
        return (reconst_path, custoT, closed_list, vehicle)


    def hillClimbing_multiple_dest(self, initial_node, destinations, vehicles):
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
            results[dest] = (None, float('inf'), None, None)

            for vehicle in vehicles:
                path, cost, expansion, vehicle = self.procura_hill_climbing(initial_node, dest, vehicle)
                if path is not None and cost < results[dest][1]:
                    results[dest] = (path, cost, expansion, vehicle)

        return results

    
    def desenha(self):
        g = nx.Graph()

        # Dicionário de cores para cada tipo de bloqueio
        blockage_colors = {
            "Cheias": "#4169E1",          # Azul Royal
            "Árvore Caída": "#228B22",    # Verde Floresta
            "Construção": "#FF8C00",      # Laranja Escuro
            "Acidente": "#DC143C",        # Vermelho Crimson
            "Pequenos detritos": "#BA55D3",# Roxo Orquídea
            "Tempestade": "#4B0082"       # Índigo
        }

        # Cor padrão para estradas não bloqueadas
        NORMAL_ROAD_COLOR = "#808080"  # Cinza

        # Adiciona os nós
        for place in self.places:
            g.add_node(place.getName(), urgency_level=place.urgency_level)

        # Adiciona as arestas com cor como atributo
        for road in self.roads:
            if road.getBlocked():
                color = blockage_colors[road.getBlockageType()]
            else:
                color = NORMAL_ROAD_COLOR

            # Imprime para debug
            print(f"Origem: {road.origin}, Destino: {road.destination}, Bloqueada: {road.getBlocked()}, Tipo: {road.getBlockageType() if road.getBlocked() else 'Normal'}, Cor: {color}")

            # Adiciona a aresta com atributos personalizados
            g.add_edge(road.origin, road.destination, weight=road.weight, color=color)

        # Usando o Kamada-Kawai layout com maior espaçamento
        pos = nx.kamada_kawai_layout(g, scale=4)

        # Gradiente de cores para níveis de urgência
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
            urgency = place.urgency_level if place.urgency_level is not None else 0
            node_colors.append(urgency_colors.get(urgency, "#E0B0FF"))

        # Configurações de estilo
        node_size = 1000
        font_size = 12
        font_color = 'black'
        edge_width = 3
        edge_colors = list(nx.get_edge_attributes(g, 'color').values())
        edge_labels = nx.get_edge_attributes(g, 'weight')
        edge_label_font_size = 12

        # Desenhando a rede
        plt.figure(figsize=(16, 16))
        nx.draw_networkx(g, pos, with_labels=True, node_size=node_size, font_weight='bold',
                        node_color=node_colors, font_size=font_size, font_color=font_color,
                        edge_color=edge_colors, width=edge_width)

        # Desenhando os rótulos das arestas (pesos)
        nx.draw_networkx_edge_labels(g, pos, edge_labels=edge_labels, font_size=edge_label_font_size, font_color='#B95CF4')

        # Criando duas legendas separadas

        # Legenda para níveis de urgência
        urgency_legend_labels = ["Urgência 0", "Urgência 1", "Urgência 2", "Urgência 3", "Urgência 4", "Urgência 5"]
        urgency_legend_colors = [urgency_colors[i] for i in range(6)]
        urgency_patches = [plt.Line2D([0], [0], color=color, marker='o', markersize=15, linestyle='', label=label)
                          for color, label in zip(urgency_legend_colors, urgency_legend_labels)]

        # Legenda para tipos de bloqueio
        blockage_legend_labels = list(blockage_colors.keys()) + ["Normal"]
        blockage_legend_colors = list(blockage_colors.values()) + [NORMAL_ROAD_COLOR]
        blockage_patches = [plt.Line2D([0], [0], color=color, linewidth=3, label=label)
                           for color, label in zip(blockage_legend_colors, blockage_legend_labels)]

        # Adicionando as duas legendas em posições diferentes
        # Legenda de urgência na parte inferior
        first_legend = plt.legend(handles=urgency_patches, 
                                 loc='lower center',
                                 bbox_to_anchor=(0.5, -0.15),  # Ajustado para baixo
                                 ncol=6, 
                                 fontsize=12,
                                 frameon=True)

        # Ajusta o título da legenda
        first_legend.set_title("Níveis de Urgência", prop={'size': 12})
        title = first_legend.get_title()
        title.set_position((-0, 1.1))  # Move o título para cima

        # Legenda de bloqueios no lado direito
        plt.legend(handles=blockage_patches, loc='center left', 
                  bbox_to_anchor=(1.0, 0.5), fontsize=12, 
                  title="Tipos de Bloqueio", title_fontsize=12, frameon=True)

        # Adiciona a primeira legenda de volta (necessário quando usando múltiplas legendas)
        plt.gca().add_artist(first_legend)

        # Melhorando o layout visual
        plt.title("PathFinder", fontsize=16, fontweight='bold', color='#7D0DC3')
        plt.axis('on')

        # Ajustando as margens para acomodar a legenda
        plt.subplots_adjust(right=0.85)

        # Exibe o gráfico
        plt.show()