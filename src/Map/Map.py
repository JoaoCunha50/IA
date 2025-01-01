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

    """def add_heuristica(self, node_name, estima):
        self.heuristics[node_name] = estima

    def getH(self, node_name):
        return self.heuristics.get(node_name, math.inf)"""

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
    
    def bfs_search(self, start, goal, vehicle):
        # Se goal for um objeto, obtém o nome (string), caso contrário, assume que já é uma string
        if isinstance(goal, str):
            goal_name = goal
        else:
            goal_name = goal.getName()

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

            # Só adicionamos aos visitados quando realmente exploramos o nodo
            visited.add(current_node)

            # Modificado para garantir que estamos comparando corretamente com o nome do goal
            if current_node == goal_name:
                # Marcamos que o caminho foi encontrado, mas a entrega será realizada posteriormente
                path_found = True

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
            current = goal_name
            while current is not None:
                path.append(current)
                current = parent[current]
            path.reverse()

            # Retorna o caminho, o tempo total e os nós visitados
            return path, tempo_total[goal_name], visited

        return None, 0, visited
    

    def bfs_search_for_all_vehicles(self, start, goal, vehicles):
        best_path = None
        best_time = float('inf')  # Inicializa o tempo com infinito
        best_vehicle = None
        best_visited = None

        if isinstance(goal, str):
            goal_name = goal
        else:
            goal_name = goal.getName()  # Obtém o nome se for um objeto 'Place'

        # Realiza a busca BFS apenas para veículos com suprimentos
        vehicles_com_suprimentos = [v for v in vehicles if v.getQuantitySup() > 0]

        for vehicle in vehicles_com_suprimentos:
            path, time, visited = self.bfs_search(start, goal_name, vehicle)

            if path and time < best_time:
                best_path = path
                best_time = time
                best_vehicle = vehicle
                best_visited = visited

        # Realiza a entrega no melhor veículo
        if best_path and best_vehicle:
            current_nodeObj = self.get_node_by_name(goal_name)
            request = current_nodeObj.getQuantity()
            supVehicle = best_vehicle.getQuantitySup()

            if request is not None and supVehicle is not None:
                if request <= supVehicle:
                    print(f"Entreguei tudo o que a freguesia de {goal_name} precisava")
                    current_nodeObj.setQuantity(0)
                    best_vehicle.setQuantitySup(supVehicle - request)
                else:
                    print(f"A freguesia de {goal_name} precisa de mais!")
                    current_nodeObj.setQuantity(request - supVehicle)
                    best_vehicle.setQuantitySup(0)

        return best_path, best_time, best_vehicle, best_visited



    def bfs_search_for_all_vehicles(self, start, goal, vehicles):
        best_path = None
        best_time = float('inf')  # Inicializa o tempo com infinito
        best_vehicle = None
        best_visited = None

        if isinstance(goal, str):
            goal_name = goal
        else:
            goal_name = goal.getName()  # Obtém o nome se for um objeto 'Place'

        # Realiza a busca BFS para todos os veículos
        for vehicle in sorted(vehicles, key=lambda v: v.getSpeed()):  # Ordena os veículos pela velocidade
            if vehicle.getQuantitySup() > 0:  # Apenas considera veículos com carga disponível
                path, time, visited = self.bfs_search(start, goal_name, vehicle)
                if path and time < best_time:
                    best_path = path
                    best_time = time
                    best_vehicle = vehicle
                    best_visited = visited

        # Apenas retorna o melhor caminho e veículo; entrega será feita em bfs_search_multiple
        return best_path, best_time, best_vehicle, best_visited


    def bfs_search_multiple(self, start, caminho, vehicles):
        resultado_por_nodo = []  # Lista para armazenar o resultado para cada nó no caminho
        ponto_atual = start  # O ponto de partida atual
        custo_total = 0  # Variável para acumular o custo total
        node_names = [node.getName() for node in caminho]  # Obtém os nomes dos nós no caminho
        entregas = 0
        
        while node_names:  # Enquanto houver nós a visitar
            destino = node_names[0]  # Primeiro destino da lista
    
            # Realiza a busca BFS para todos os veículos para o destino atual
            path, time, vehicle, visited = self.bfs_search_for_all_vehicles(ponto_atual, destino, vehicles)
    
            if path:
                custo_total += time  # Acumula o tempo/custo total
                
                # Atualiza o tempo restante para todos os nós
                for node in caminho:
                    if hasattr(node, "time_remaining") and node.time_remaining is not None:
                        node.time_remaining -= time  # Subtrai o custo do tempo restante
    
                        # Verifica se o tempo restante ficou <= 0
                        if node.time_remaining <= 0:
                            print(f"Atenção: O tempo para o nó {node.getName()} expirou ou está muito próximo de 0!")
                
                # Processa os nós intermediários no caminho
                for intermediate_node in path[1:]:  # Exclui o ponto de partida
                    current_nodeObj = self.get_node_by_name(intermediate_node)
                    request = current_nodeObj.getQuantity()
    
                    if request and request > 0:  # Há uma entrega pendente neste nó
                        supVehicle = vehicle.getQuantitySup()
    
                        if request <= supVehicle:
                            print(f"Entreguei tudo o que a freguesia de {intermediate_node} precisava")
                            current_nodeObj.setQuantity(0)
                            vehicle.setQuantitySup(supVehicle - request)
                        else:
                            print(f"A freguesia de {intermediate_node} precisa de mais!")
                            current_nodeObj.setQuantity(request - supVehicle)
                            vehicle.setQuantitySup(0)
    
                        # Remove o nó da lista de destinos se a entrega foi completada
                        if current_nodeObj.getQuantity() == 0 and intermediate_node in node_names:
                            node_names.remove(intermediate_node)
    
                resultado_por_nodo.append({
                    "start": ponto_atual,            # O ponto inicial
                    "destino": destino,              # O ponto final (nó atual do caminho)
                    "path": path,                    # Caminho encontrado
                    "vehicle": vehicle,              # Veículo utilizado
                    "visited": visited               # Nós visitados
                })
                ponto_atual = destino  # Atualiza o ponto atual para o próximo destino
                node_names.pop(0)  # Remove o destino atual da lista de caminhos
    
            else:
                print(f"Não foi possível encontrar caminho para o destino {destino}.")
                break
            
        return resultado_por_nodo, custo_total
    
    

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
