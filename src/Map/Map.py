
from colorama import Fore, Back, Style, init
import networkx as nx
import matplotlib
matplotlib.use('gtk3agg')

import matplotlib.pyplot as plt

from Map.Place import Place
from Map.Road import Road
from Map.Heuristic import Heuristic
from collections import deque
import random
from colorama import *


class Map:
    def __init__(self, heuristics, directed=False):
        self.places: list[Place] = []  # Lista de nós (Places)
        self.roads: list[Road] = []    # Lista de estradas (Roads)
        self.directed = directed
        self.heuristics = heuristics # Heurísticas para algoritmos de busca
        self.tempo = 0
        self.valor_base_tempo = 0

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
            if place.getName().lower() == name:
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
        blocked = random.random() < 0.10

        # Adiciona a estrada ao grafo com o valor de blocked
        road = Road(origin_place.getName(), destination_place.getName(), weight, blocked)
        self.roads.append(road)

        if not self.directed:
            # Adiciona a estrada reversa com o mesmo valor de blocked
            reverse_road = Road(destination_place.getName(), origin_place.getName(), weight, blocked,road.blockage_type)
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

    def update_road_blockages(self, probability=0.02):
        """
        Atualiza o estado de bloqueio das estradas com base em uma probabilidade.

        Args:
            probability (float): Probabilidade de uma estrada mudar seu estado de bloqueio (0.0 a 1.0)
            Padrão é 0.02 (0.02% de chance)
        """
        if not 0 <= probability <= 1:
            raise ValueError("Probability must be between 0 and 1")

        for road in self.roads:
            # Para cada estrada, gera um número aleatório entre 0 e 1
            if random.random() < probability:
                # Inverte o estado de bloqueio
                road.blocked = not road.blocked

                # Se a estrada ficou bloqueada, atribui um tipo de bloqueio aleatório
                if road.blocked:
                    road.blockage_type = random.choice(list(road.VALID_BLOCKAGE_TYPES.keys()))
                else:
                    road.blockage_type = None

                # Exibe informações da estrada atualizada
                print(f"{Fore.WHITE}{'='*40}")
                print(f"{Fore.BLUE}Road Updated:")
                print(f"  {Fore.CYAN}Origin       : {Fore.WHITE}{road.origin}")
                print(f"  {Fore.CYAN}Destination  : {Fore.WHITE}{road.destination}")
                print(f"  {Fore.CYAN}Blocked      : {Fore.RED if road.blocked else Fore.GREEN}{road.blocked}")
                print(f"  {Fore.CYAN}Blockage Type: {Fore.WHITE}{road.blockage_type}")
                print(f"{Fore.WHITE}{'='*40}\n")

                # Se o grafo não é direcionado, atualiza a estrada reversa também
                if not self.directed:
                    for reverse_road in self.roads:
                        if (reverse_road.origin == road.destination and 
                            reverse_road.destination == road.origin):
                            reverse_road.blocked = road.blocked
                            reverse_road.blockage_type = road.blockage_type

    
    def simula_entrega(self, vehicle, place):
        vehicleQuantity = vehicle.getQuantitySup()
        placeQuantity = place.getQuantity()

        entregue = min(vehicleQuantity, placeQuantity)
        
        updatedQuantity = max(0, vehicleQuantity - entregue)
            
        vehicle.setQuantitySup(updatedQuantity)
        place.obtained += entregue
        

    def encontra_ponto_reabastecimento(self, current_location):
        return next((place.getName() for place in self.places if place.ponto_reabastecimento), None)


    def simulaTempo(self, vehicle, path):
        
        # Obtém a velocidade média do veículo
        velocidade_media = vehicle.getSpeed()

        places = []
        
        for i in range(len(path) - 1):
            origem, destino = path[i], path[i + 1]
            
            for road in self.roads:
                if road.origin == origem and road.destination == destino:
                    # Obtém o peso (distância) da estrada
                    distancia = road.getWeight()

                    # Cálculo do tempo em horas e conversão para segundos
                    tempo_em_horas = distancia / velocidade_media
                    tempo_em_segundos = tempo_em_horas * 3600  # Converte o tempo de horas para segundos

                    # Arredonda o tempo para 1 casa decimal
                    tempo_arredondado = round(tempo_em_segundos, 2)
                    
                    self.tempo += tempo_arredondado
                    break


        for place in self.places:
            if not place.ponto_reabastecimento:
                timeRemaining = place.getTimeRemaining() - self.tempo
                if timeRemaining <= 0:
                    places.append(place)

        return places
    
    
    def procura_DFS(self, start, end, vehicle, path=None, visited=None):
        if path is None:
            path = []
        if visited is None:
            visited = set()
            
        path.append(start)
        visited.add(start)
            
        if self.get_node_by_name(start).ponto_reabastecimento:
            vehicle.setQuantitySup(vehicle.getCapacity())

        if start == end:
            custo_total = self.calcula_custo(path, vehicle)
            
            if not self.get_node_by_name(start).ponto_reabastecimento:  # Só faz entrega se não for viagem de reabastecimento
                self.simula_entrega(vehicle, self.get_node_by_name(end))
                
                # Se ainda precisa entregar mais
                while self.get_node_by_name(end).obtained < self.get_node_by_name(end).getQuantity():
                    ponto_reabastecimento = self.encontra_ponto_reabastecimento(start)
                    if ponto_reabastecimento is None:
                        print("Erro: Não há pontos de reabastecimento disponíveis.")
                        return None, None, visited, vehicle

                    # Limpa o estado para a nova busca
                    novo_path = []
                    novo_visited = set()
                    
                    # Vai para reabastecimento
                    caminho_reabastecimento, custo_reabastecimento, _, vehicle = self.procura_DFS(
                        start, ponto_reabastecimento, vehicle, novo_path, novo_visited
                    )
                    if caminho_reabastecimento is None:
                        return None, None, visited, vehicle
                    
                    path.extend(caminho_reabastecimento[1:] + list(reversed(caminho_reabastecimento))[1:])
                    custo_total += custo_reabastecimento*2
                    self.simula_entrega(vehicle, self.get_node_by_name(end))

                vehicle.setQuantitySup(vehicle.getCapacity())
                self.get_node_by_name(end).resetQuantity()
            return path, round(custo_total, 2), visited, vehicle

        for road in self.roads:
            if road.origin == start:
                adjacente = road.destination
            elif not self.directed and road.destination == start:
                adjacente = road.origin
            else:
                continue

            # Verifica se a estrada está bloqueada e se o veículo pode passar
            if road.blocked and not road.canVehiclePass(vehicle.getType()):
                continue  # Pula este vizinho se a estrada não for transitável pelo veículo

            # Chamar recursivamente para o nó adjacente
            if adjacente not in visited:
                
                resultado, custo, visitados_atualizados, vehicle = self.procura_DFS(
                    adjacente, end, vehicle, path, visited
                )
                if resultado is not None:
                    vehicle.setQuantitySup(vehicle.getCapacity())
                    self.get_node_by_name(end).resetQuantity()
                    return resultado, round(custo, 2), visitados_atualizados, vehicle

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
            Dicionário com destino como chave e tupla (caminho, custo, ordem_expansão, veículo) como valor.
            Lista consolidada de todos os nós em que o tempo se esgotou.
        """
        results = {}
        consolidated_places_timed_out = []  # Lista consolidada de lugares com tempo esgotado

        for dest in destinations:
            # Inicializar com valores padrão
            results[dest] = (None, float('inf'), None, None)  # (caminho, custo, visitados, veículo)
            best_vehicle_cost = float('inf')  # Armazena o menor custo para o destino atual
            best_vehicle_path = None  # Caminho do melhor veículo para o destino
            best_vehicle_visited = None  # Conjunto de nós visitados pelo melhor veículo
            best_vehicle = None  # Veículo que obteve o melhor resultado

            for vehicle in vehicles:
                places_timed_out_aux = []  # Lista auxiliar para lugares com tempo esgotado neste veículo

                # Executa DFS para cada veículo e destino
                path, cost, visited, current_vehicle = self.procura_DFS(
                    initial_node, dest, vehicle
                )

                # Atualiza o melhor veículo e resultado se o custo for menor que o registrado
                if path is not None and cost < best_vehicle_cost:
                    places_timed_out = self.simulaTempo(vehicle, path)
                    
                    best_vehicle_cost = cost
                    best_vehicle_path = path
                    best_vehicle_visited = visited
                    best_vehicle = current_vehicle

                self.tempo = self.valor_base_tempo

            # Atualiza os resultados com os valores do melhor veículo
            if best_vehicle_path is not None:
                results[dest] = (best_vehicle_path, round(best_vehicle_cost, 2), best_vehicle_visited, best_vehicle)
                
            # Atualiza os bloqueios após encontrar o melhor caminho para este destino
            self.update_road_blockages()

            # Adiciona lugares com tempo esgotado à lista consolidada
            for place in places_timed_out:
                if place not in consolidated_places_timed_out:
                    consolidated_places_timed_out.append(place)

            # Atualiza o tempo com base no custo do melhor veículo
            self.valor_base_tempo += best_vehicle_cost
            self.tempo = self.valor_base_tempo

        self.tempo = 0
        self.valor_base_tempo = 0
        return results, consolidated_places_timed_out


    def procura_BFS(self, start, end, vehicle):
        """
        Procura um caminho usando BFS entre start e end, considerando o veículo.
        """

        # Inicializar a fila e as estruturas auxiliares
        queue = deque([(start, [start])])  # Cada elemento é (nó_atual, caminho_até_agora)
        visited = set()  # Conjunto para rastrear os nós visitados

        while queue:
            current_node, path = queue.popleft()  # Retira o primeiro elemento da fila

            # Verificar se chegamos ao destino
            if current_node == end:
                custo_total = self.calcula_custo(path, vehicle)# Calcular o custo do caminho encontrado
            
                if not self.get_node_by_name(current_node).ponto_reabastecimento:  # Só faz entrega se não for viagem de reabastecimento
                    self.simula_entrega(vehicle, self.get_node_by_name(end))
                    
                    # Se ainda precisa entregar mais
                    while self.get_node_by_name(end).obtained < self.get_node_by_name(end).getQuantity():
                        ponto_reabastecimento = self.encontra_ponto_reabastecimento(start)
                        if ponto_reabastecimento is None:
                            print("Erro: Não há pontos de reabastecimento disponíveis.")
                            return None, None, visited, vehicle
                        
                        # Vai para reabastecimento
                        caminho_reabastecimento, custo_reabastecimento, _, vehicle = self.procura_DFS(
                            current_node, ponto_reabastecimento, vehicle
                        )
                        if caminho_reabastecimento is None:
                            return None, None, visited, vehicle

                        path.extend(caminho_reabastecimento[1:] + list(reversed(caminho_reabastecimento))[1:])
                        custo_total += custo_reabastecimento*2
                        self.simula_entrega(vehicle, self.get_node_by_name(end))

                    vehicle.setQuantitySup(vehicle.getCapacity())
                    self.get_node_by_name(end).resetQuantity()                

                return path, round(custo_total, 2), visited, vehicle

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

                # Verificar se a estrada está bloqueada ou se o veículo pode passar
                if road.blocked and not road.canVehiclePass(vehicle.getType()):
                    continue  # Ignora a estrada se está bloqueada e o veículo não pode passar

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
            Dicionário com destino como chave e tupla (caminho, custo, ordem_expansão, veículo) como valor.
            Lista consolidada de todos os nós em que o tempo se esgotou.
        """
        results = {}
        consolidated_places_timed_out = []  # Lista consolidada de lugares com tempo esgotado

        for dest in destinations:
            # Inicializar com valores padrão
            results[dest] = (None, float('inf'), None, None)  # (caminho, custo, visitados, veículo)
            best_vehicle_cost = float('inf')  # Armazena o menor custo para o destino atual
            best_vehicle_path = None  # Caminho do melhor veículo para o destino
            best_vehicle_visited = None  # Conjunto de nós visitados pelo melhor veículo
            best_vehicle = None  # Veículo que obteve o melhor resultado

            for vehicle in vehicles:

                # Executa BFS para cada veículo e destino
                path, cost, visited, current_vehicle = self.procura_BFS(
                    initial_node, dest, vehicle
                )

                # Atualiza o melhor veículo e resultado se o custo for menor que o registrado
                if path is not None and cost < best_vehicle_cost:
                    places_timed_out = self.simulaTempo(vehicle, path)
                    best_vehicle_cost = cost
                    best_vehicle_path = path
                    best_vehicle_visited = visited
                    best_vehicle = current_vehicle

                self.tempo = self.valor_base_tempo

            # Atualiza os resultados com os valores do melhor veículo
            if best_vehicle_path is not None:
                results[dest] = (best_vehicle_path, round(best_vehicle_cost, 2), best_vehicle_visited, best_vehicle)

            # Adiciona lugares com tempo esgotado à lista consolidada
            for place in places_timed_out:
                if place not in consolidated_places_timed_out:
                    consolidated_places_timed_out.append(place)
                    
            # Atualiza os bloqueios após encontrar o melhor caminho para este destino
            self.update_road_blockages()

            # Atualiza o tempo com base no custo do melhor veículo
            self.valor_base_tempo += best_vehicle_cost
            self.tempo = self.valor_base_tempo

        self.tempo = 0
        self.valor_base_tempo = 0
        return results, consolidated_places_timed_out



    def uniform_cost_search(self, initial_node, goal, vehicle):
        """
        Realiza a busca de custo uniforme considerando bloqueios e compatibilidade do veículo.
        """
        import heapq  # Para a fila de prioridade

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

                if not self.get_node_by_name(goal).ponto_reabastecimento:
                    self.simula_entrega(vehicle, self.get_node_by_name(goal))

                    # Verifica se o destino ainda precisa de mais quantidade
                    while self.get_node_by_name(goal).obtained < self.get_node_by_name(goal).getQuantity():
                        # Buscar ponto de reabastecimento
                        ponto_reabastecimento = self.encontra_ponto_reabastecimento(current_node)
                        if ponto_reabastecimento is None:
                            print("Erro: Não há pontos de reabastecimento disponíveis.")
                            return None, 0, expansion_order, vehicle

                        # Busca o caminho até o ponto de reabastecimento
                        caminho_reabastecimento, custo_reabastecimento, _, vehicle = self.uniform_cost_search(
                            goal, ponto_reabastecimento, vehicle
                        )
                        if caminho_reabastecimento is None:
                            return None, 0, expansion_order, vehicle

                        # Atualiza o caminho com o reabastecimento
                        reconst_path.extend(caminho_reabastecimento[1:] + list(reversed(caminho_reabastecimento))[1:])
                        custo_total += custo_reabastecimento*2

                        # Simula o reabastecimento
                        vehicle.setQuantitySup(vehicle.getCapacity()) 

                        # Após o reabastecimento, simula a entrega novamente
                        self.simula_entrega(vehicle, self.get_node_by_name(goal))

                    vehicle.setQuantitySup(vehicle.getCapacity())
                    self.get_node_by_name(goal).resetQuantity() 
                    
                # Se as necessidades foram satisfeitas, retorna o caminho e o custo
                return reconst_path, round(custo_total, 2), expansion_order, vehicle

            # Explorar os vizinhos do nó atual
            for neighbour, weight in self.getNeighbours(current_node):
                can_pass = True  # Assume-se que a estrada está livre, até que se prove o contrário

                # Verifica se a estrada está bloqueada e se o veículo pode passar
                for road in self.roads:
                    if (road.origin == current_node and road.destination == neighbour) or \
                    (not self.directed and road.destination == current_node and road.origin == neighbour):
                        if road.blocked and not road.canVehiclePass(vehicle.getType()):
                            can_pass = False  # Se a estrada está bloqueada e o veículo não pode passar, ignora
                        break  # Não precisa verificar mais estradas para esse par origem-destino

                # Se a estrada não está bloqueada ou o veículo pode passar, podemos considerar o vizinho
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
            initial_node: Nó inicial.
            destinations: Lista de nós destino.
            vehicles: Lista de veículos.

        Returns:
            Dicionário com destino como chave e tupla (caminho, custo, ordem_expansão, veículo) como valor.
            Lista consolidada de todos os nós em que o tempo se esgotou.
        """
        results = {}
        consolidated_places_timed_out = []  # Lista consolidada de lugares com tempo esgotado

        for dest in destinations:
            # Inicializa os valores padrão para cada destino
            best_path = None
            best_cost = float('inf')
            best_expansion = None
            best_vehicle = None

            for vehicle in vehicles:
                # Executa UCS para cada veículo e destino
                path, cost, expansion, current_vehicle = self.uniform_cost_search(
                    initial_node, dest, vehicle
                )

                # Atualiza o melhor veículo e resultado se o custo for menor que o registrado
                if path is not None and cost < best_cost:
                    places_timed_out = self.simulaTempo(vehicle, path)
                    best_cost = cost
                    best_path = path
                    best_expansion = expansion
                    best_vehicle = current_vehicle

                self.tempo = self.valor_base_tempo

            # Atualiza os resultados com os valores do melhor veículo
            if best_path is not None:
                results[dest] = (best_path, round(best_cost, 2), best_expansion, best_vehicle)
                
            # Atualiza os bloqueios após encontrar o melhor caminho para este destino
            self.update_road_blockages()

            # Adiciona lugares com tempo esgotado à lista consolidada
            for place in places_timed_out:
                if place not in consolidated_places_timed_out:
                    consolidated_places_timed_out.append(place)

            # Atualiza o tempo com base no custo do melhor veículo
            self.valor_base_tempo += best_cost
            self.tempo = self.valor_base_tempo

        self.tempo = 0
        self.valor_base_tempo = 0
        return results, consolidated_places_timed_out

    
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
        """
        Implementação do algoritmo A* considerando a compatibilidade do veículo com os bloqueios nas estradas.
        """
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

                return None

            if n == end:
                reconst_path = []
                while parents[n] != n:
                    reconst_path.append(n)
                    n = parents[n]
                reconst_path.append(start)
                reconst_path.reverse()
                open_list.update(closed_list)
                custo_total = self.calcula_custo(reconst_path, vehicle)
                
                if not self.get_node_by_name(end).ponto_reabastecimento:
                    self.simula_entrega(vehicle, self.get_node_by_name(end))

                    # Verifica se o destino ainda precisa de mais quantidade
                    while self.get_node_by_name(end).obtained < self.get_node_by_name(end).getQuantity():
                        # Buscar ponto de reabastecimento
                        ponto_reabastecimento = self.encontra_ponto_reabastecimento(n)
                        if ponto_reabastecimento is None:
                            print("Erro: Não há pontos de reabastecimento disponíveis.")
                            return None, 0, open_list, vehicle

                        # Busca o caminho até o ponto de reabastecimento
                        caminho_reabastecimento, custo_reabastecimento, _, vehicle = self.procura_aStar(
                            end, ponto_reabastecimento, vehicle
                        )
                        if caminho_reabastecimento is None:
                            return None, 0, open_list, vehicle

                        # Atualiza o caminho com o reabastecimento
                        reconst_path.extend(caminho_reabastecimento[1:] + list(reversed(caminho_reabastecimento))[1:])
                        custo_total += custo_reabastecimento*2

                        # Simula o reabastecimento
                        vehicle.setQuantitySup(vehicle.getCapacity()) 

                        # Após o reabastecimento, simula a entrega novamente
                        self.simula_entrega(vehicle, self.get_node_by_name(end))

                    vehicle.setQuantitySup(vehicle.getCapacity())
                    self.get_node_by_name(end).resetQuantity() 
                return (reconst_path, round(custo_total, 2), open_list, vehicle)

            for road in self.roads:
                # Verifica se a estrada é relevante para o nó atual (origem ou destino é `n`)
                if road.origin == n or road.destination == n:
                    m = road.destination if road.origin == n else road.origin
                    weight = road.weight

                    # Verifica se a estrada está bloqueada e se o veículo pode passar
                    if road.blocked and not road.canVehiclePass(vehicle.getType()):
                        continue  # Pula este vizinho se a estrada não for transitável pelo veículo

                    # Processa o vizinho se não foi explorado
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
        consolidated_places_timed_out = []  # Lista consolidada de lugares com tempo esgotado

        for dest in destinations:
            results[dest] = (None, float('inf'), None, None)
            
            # Inicializa os valores padrão para cada destino
            best_path = None
            best_cost = float('inf')
            best_expansion = None
            best_vehicle = None

            for vehicle in vehicles:
                path, cost, expansion, vehicle = self.procura_aStar(initial_node, dest, vehicle)
                
                # Atualiza o melhor veículo e resultado se o custo for menor que o registrado
                if path is not None and cost < best_cost:
                    places_timed_out = self.simulaTempo(vehicle, path)
                    best_cost = cost
                    best_path = path
                    best_expansion = expansion
                    best_vehicle = vehicle

                self.tempo = self.valor_base_tempo

            # Atualiza os resultados com os valores do melhor veículo
            if best_path is not None:
                results[dest] = (best_path, round(best_cost, 2), best_expansion, best_vehicle)

            # Adiciona lugares com tempo esgotado à lista consolidada
            for place in places_timed_out:
                if place not in consolidated_places_timed_out:
                    consolidated_places_timed_out.append(place)

            # Atualiza o tempo com base no custo do melhor veículo
            self.valor_base_tempo += best_cost
            self.tempo = self.valor_base_tempo
            
            # Atualiza os bloqueios após encontrar o melhor caminho para este destino
            self.update_road_blockages()


        self.tempo = 0
        self.valor_base_tempo = 0
        return results, consolidated_places_timed_out



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
                return (None, float('inf'), open_list, vehicle)

            if n == end:
                reconst_path = []
                while parents[n] != n:
                    reconst_path.append(n)
                    n = parents[n]
                reconst_path.append(start)
                reconst_path.reverse()
                custo_total = self.calcula_custo(reconst_path, vehicle)
                
                if not self.get_node_by_name(end).ponto_reabastecimento:
                    self.simula_entrega(vehicle, self.get_node_by_name(end))

                    # Verifica se o destino ainda precisa de mais quantidade
                    while self.get_node_by_name(end).obtained < self.get_node_by_name(end).getQuantity():
                        # Buscar ponto de reabastecimento
                        ponto_reabastecimento = self.encontra_ponto_reabastecimento(n)
                        if ponto_reabastecimento is None:
                            print("Erro: Não há pontos de reabastecimento disponíveis.")
                            return None, 0, open_list, vehicle

                        # Busca o caminho até o ponto de reabastecimento
                        caminho_reabastecimento, custo_reabastecimento, _, vehicle = self.procura_gulosa(
                            end, ponto_reabastecimento, vehicle
                        )
                        if caminho_reabastecimento is None:
                            return None, 0, open_list, vehicle

                        # Atualiza o caminho com o reabastecimento
                        reconst_path.extend(caminho_reabastecimento[1:] + list(reversed(caminho_reabastecimento))[1:])
                        custo_total += custo_reabastecimento*2

                        # Simula o reabastecimento
                        vehicle.setQuantitySup(vehicle.getCapacity()) 

                        # Após o reabastecimento, simula a entrega novamente
                        self.simula_entrega(vehicle, self.get_node_by_name(end))

                    vehicle.setQuantitySup(vehicle.getCapacity())
                    self.get_node_by_name(end).resetQuantity() 
                
                return (reconst_path, round(custo_total, 2), open_list, vehicle)

            for road in self.roads:
                if (road.origin == n or road.destination == n):
                    can_pass = not road.blocked or (road.blocked and road.canVehiclePass(vehicle.getType()))
                    if can_pass:
                        m = road.destination if road.origin == n else road.origin
                        if m not in open_list and m not in closed_list:
                            open_list.add(m)
                            parents[m] = n

            open_list.remove(n)
            closed_list.add(n)

        return (None, float('inf'), open_list, vehicle)




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
        consolidated_places_timed_out = []  # Lista consolidada de lugares com tempo esgotado

        for dest in destinations:
            results[dest] = (None, float('inf'), None, None)
            
            # Inicializa os valores padrão para cada destino
            best_path = None
            best_cost = float('inf')
            best_expansion = None
            best_vehicle = None

            for vehicle in vehicles:
                path, cost, expansion, vehicle = self.procura_aStar(initial_node, dest, vehicle)
                
                # Atualiza o melhor veículo e resultado se o custo for menor que o registrado
                if path is not None and cost < best_cost:
                    places_timed_out = self.simulaTempo(vehicle, path)
                    best_cost = cost
                    best_path = path
                    best_expansion = expansion
                    best_vehicle = vehicle

                self.tempo = self.valor_base_tempo

            # Atualiza os resultados com os valores do melhor veículo
            if best_path is not None:
                results[dest] = (best_path, round(best_cost, 2), best_expansion, best_vehicle)

            # Adiciona lugares com tempo esgotado à lista consolidada
            for place in places_timed_out:
                if place not in consolidated_places_timed_out:
                    consolidated_places_timed_out.append(place)

            # Atualiza o tempo com base no custo do melhor veículo
            self.valor_base_tempo += best_cost
            self.tempo = self.valor_base_tempo
      
            # Atualiza os bloqueios após encontrar o melhor caminho para este destino
            self.update_road_blockages()

        self.tempo = 0
        self.valor_base_tempo = 0
        return results, consolidated_places_timed_out

    
    def procura_hill_climbing(self, start, end, vehicle):
        current_node = start
        closed_list = {start}
        parents = {start: start}

        while current_node != end:
            neighbors = []
            for road in self.roads:
                if (road.origin == current_node or road.destination == current_node):
                    neighbor = road.destination if road.origin == current_node else road.origin

                    if not road.blocked:
                        # Estrada não bloqueada, adiciona o vizinho normalmente
                        neighbors.append(neighbor)
                    elif road.canVehiclePass(vehicle.getType()):
                        # Estrada bloqueada, mas o veículo pode passar
                        neighbors.append(neighbor)
                    else:
                        # Estrada bloqueada e o veículo não pode passar
                        # Não adicionamos este vizinho à lista de neighbors
                        continue

            next_node = None
            lowest_heuristic = float('inf')
            for neighbor in neighbors:
                if neighbor not in closed_list:
                    heuristic_value = self.heuristics.getHeuristic(neighbor, end)
                    if heuristic_value < lowest_heuristic:
                        lowest_heuristic = heuristic_value
                        next_node = neighbor

            if next_node is None:
                print(f'Path does not exist for vehicle {vehicle.getType()}!')
                return (None, float('inf'), closed_list, vehicle)

            parents[next_node] = current_node
            closed_list.add(next_node)
            current_node = next_node

        reconst_path = []
        while parents[current_node] != current_node:
            reconst_path.append(current_node)
            current_node = parents[current_node]
        reconst_path.append(start)
        reconst_path.reverse()
        custo_total = self.calcula_custo(reconst_path, vehicle)
        
        if not self.get_node_by_name(end).ponto_reabastecimento:
                self.simula_entrega(vehicle, self.get_node_by_name(end))

                # Verifica se o destino ainda precisa de mais quantidade
                while self.get_node_by_name(end).obtained < self.get_node_by_name(end).getQuantity():
                    # Buscar ponto de reabastecimento
                    ponto_reabastecimento = self.encontra_ponto_reabastecimento(current_node)
                    if ponto_reabastecimento is None:
                        print("Erro: Não há pontos de reabastecimento disponíveis.")
                        return None, 0, closed_list, vehicle

                    # Busca o caminho até o ponto de reabastecimento
                    caminho_reabastecimento, custo_reabastecimento, _, vehicle = self.procura_hill_climbing(
                        end, ponto_reabastecimento, vehicle
                    )
                    if caminho_reabastecimento is None:
                        return None, 0, closed_list, vehicle
                    
                    # Atualiza o caminho com o reabastecimento
                    reconst_path.extend(caminho_reabastecimento[1:] + list(reversed(caminho_reabastecimento))[1:])
                    custo_total += custo_reabastecimento*2

                    # Simula o reabastecimento
                    vehicle.setQuantitySup(vehicle.getCapacity()) 
                    
                    # Após o reabastecimento, simula a entrega novamente
                    self.simula_entrega(vehicle, self.get_node_by_name(end))

                vehicle.setQuantitySup(vehicle.getCapacity())
                self.get_node_by_name(end).resetQuantity()     
        return (reconst_path, round(custo_total, 2), closed_list, vehicle)



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
        consolidated_places_timed_out = []  # Lista consolidada de lugares com tempo esgotado

        for dest in destinations:
            results[dest] = (None, float('inf'), None, None)
            
            # Inicializa os valores padrão para cada destino
            best_path = None
            best_cost = float('inf')
            best_expansion = None
            best_vehicle = None

            for vehicle in vehicles:
                path, cost, expansion, vehicle = self.procura_aStar(initial_node, dest, vehicle)
                
                # Atualiza o melhor veículo e resultado se o custo for menor que o registrado
                if path is not None and cost < best_cost:
                    places_timed_out = self.simulaTempo(vehicle, path)
                    best_cost = cost
                    best_path = path
                    best_expansion = expansion
                    best_vehicle = vehicle

                self.tempo = self.valor_base_tempo

            # Atualiza os resultados com os valores do melhor veículo
            if best_path is not None:
                results[dest] = (best_path, round(best_cost, 2), best_expansion, best_vehicle)

            # Adiciona lugares com tempo esgotado à lista consolidada
            for place in places_timed_out:
                if place not in consolidated_places_timed_out:
                    consolidated_places_timed_out.append(place)

            # Atualiza o tempo com base no custo do melhor veículo
            self.valor_base_tempo += best_cost
            self.tempo = self.valor_base_tempo
            
            # Atualiza os bloqueios após encontrar o melhor caminho para este destino
            self.update_road_blockages()

        self.tempo = 0
        self.valor_base_tempo = 0
        return results, consolidated_places_timed_out

    
    def desenha(self):
        g = nx.Graph()

        # Dicionário de cores para cada tipo de bloqueio
        blockage_colors = {
            "Cheias": "#4169E1",          # Azul Royal
            "Árvore Caída": "#228B22",    # Verde Floresta
            "Construção": "#FF8C00",      # Laranja Escuro
            "Acidente": "#DC143C",        # Vermelho Crimson
            "Pequenos detritos": "#BA55D3",# Roxo Orquídea
            "Tempestade": "#4B0082",       # Índigo
            "Estrada Restrita": "#8B4513"
        }

        # Cor padrão para estradas não bloqueadas e pontos de reabastecimento
        NORMAL_ROAD_COLOR = "#808080"  # Cinza
        REABASTECIMENTO_COLOR = "#87CEFA"  # Azul claro

        # Adiciona os nós
        for place in self.places:
            g.add_node(place.getName(), urgency_level=place.urgency_level, is_reabastecimento=place.ponto_reabastecimento)

        # Adiciona as arestas com cor como atributo
        for road in self.roads:
            if road.getBlocked():
                color = blockage_colors[road.getBlockageType()]
            else:
                color = NORMAL_ROAD_COLOR

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

        # Determina as cores dos nós com base nos níveis de urgência e pontos de reabastecimento
        node_colors = []
        for place in self.places:
            if place.ponto_reabastecimento:
                node_colors.append(REABASTECIMENTO_COLOR)
            else:
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

        # Criando três legendas separadas

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

        # Legenda para pontos de reabastecimento
        reabastecimento_patch = [plt.Line2D([0], [0], color=REABASTECIMENTO_COLOR, marker='o', 
                                        markersize=15, linestyle='', label='Ponto de Reabastecimento')]

        # Adicionando as três legendas em posições diferentes
        # Legenda de urgência na parte inferior
        first_legend = plt.legend(handles=urgency_patches, 
                                loc='lower center',
                                bbox_to_anchor=(0.5, -0.15),
                                ncol=6, 
                                fontsize=12,
                                frameon=True)

        # Ajusta o título da legenda
        first_legend.set_title("Níveis de Urgência", prop={'size': 12})
        title = first_legend.get_title()
        title.set_position((-0, 1.1))

        # Legenda de bloqueios no lado direito
        second_legend = plt.legend(handles=blockage_patches, 
                                loc='center left', 
                                bbox_to_anchor=(1.0, 0.5), 
                                fontsize=12, 
                                title="Tipos de Bloqueio", 
                                title_fontsize=12, 
                                frameon=True)

        # Legenda de reabastecimento no lado esquerdo
        third_legend = plt.legend(handles=reabastecimento_patch,
                                loc='center right',
                                bbox_to_anchor=(0, 0.5),
                                fontsize=12,
                                title="Reabastecimento",
                                title_fontsize=12,
                                frameon=True)

        # Adiciona as legendas de volta
        plt.gca().add_artist(first_legend)
        plt.gca().add_artist(second_legend)

        # Melhorando o layout visual
        plt.title("PathFinder", fontsize=16, fontweight='bold', color='#7D0DC3')
        plt.axis('on')

        # Ajustando as margens para acomodar todas as legendas
        plt.subplots_adjust(right=0.85, left=0.15)

        # Exibe o gráfico
        plt.show()
