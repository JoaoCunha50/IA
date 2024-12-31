from colorama import Fore, Back, Style, init
from Map.Map import Map
from utils.Json_Reader import Json_Reader

def get_valid_vehicle_id(vehicles):
    while True:
        try:
            vehicle_id = int(input("Introduza o ID do veículo: "))
            for vehicle in vehicles:
                if vehicle.getId() == vehicle_id:
                    return vehicle  # Retorna o objeto vehicle completo
            print(Fore.RED + "ID de veículo inválido! Tente novamente.")
        except ValueError:
            print(Fore.RED + "Por favor, insira um número válido.")


def main():
    init(autoreset=True)

    vehicles = Json_Reader.load_vehicles_from_file("src/jsons/vehicles.json")
    for vehicle in vehicles:
        print()
        print(str(vehicle))
        print()
            
    print(Fore.CYAN + "="*30 + Fore.WHITE)
    print()
        
    suplements = Json_Reader.load_suplements_from_json("src/jsons/suplly_requests.json")
    for suplement in suplements:
        print(str(suplement))
        print()
            
    g = Map()

    default_vehicles = ["caminhao", "moto", "carrinha", "drone s", "drone m"]
    
    # Road definitions remain the same...
    g.add_road("Pedome", "Gondar", 3, ["moto", "carrinha"],suplements)  
    g.add_road("Pedome", "Serzedelo", 5, default_vehicles,suplements)
    g.add_road("Pedome", "Mogege", 4, default_vehicles,suplements)
    g.add_road("Gondar", "Ronfe", 4, default_vehicles,suplements)
    g.add_road("Gondar", "S. Jorge de Selho", 4, default_vehicles,suplements)
    g.add_road("Gondar", "Selho (São Cristóvão)", 3, default_vehicles,suplements)
    g.add_road("Gondar", "Serzedelo", 2, default_vehicles,suplements)
    g.add_road("Ronfe", "Mogege", 4, default_vehicles,suplements)
    g.add_road("Ronfe", "S. Jorge de Selho", 5, default_vehicles,suplements)
    g.add_road("S. Jorge de Selho", "Selho (São Cristóvão)", 4, default_vehicles,suplements)
    g.add_road("Serzedelo", "Gandarela", 3, default_vehicles,suplements)
    g.add_road("Serzedelo", "Ruivães", 12, ["drone s", "moto", "drone m"],suplements)  
    g.add_road("Serzedelo", "Riba d'Ave", 3, default_vehicles,suplements)
    g.add_road("Riba d'Ave", "Ruivães", 7, default_vehicles,suplements)
    g.add_road("Riba d'Ave", "Carreira", 6, default_vehicles,suplements)
    g.add_road("Carreira", "Avidos", 4, default_vehicles,suplements)
    g.add_road("Avidos", "Vale (São Martinho)", 9, default_vehicles,suplements)
    g.add_road("Mogege", "Vale (São Martinho)", 10, default_vehicles,suplements)

    # Heuristics remain the same...
    g.add_heuristica("elvas", 270)
    # ... (rest of the heuristics)

    saida = -1
    while saida != 0:
        print("\n" + "="*30)
        print(Fore.CYAN + Style.BRIGHT + "          PathFinder")
        print("=" * 30)

        print(Fore.CYAN + "1-" + Fore.WHITE + " Desenhar Grafo")
        print(Fore.CYAN + "2-" + Fore.WHITE + " Imprimir nodos de Grafo")
        print(Fore.CYAN + "3-" + Fore.WHITE + " Imprimir arestas de Grafo")
        print(Fore.CYAN + "4-" + Fore.WHITE + " Realizar DFS")
        print(Fore.CYAN + "5-" + Fore.WHITE + " Realizar BFS")
        print(Fore.CYAN + "0-" + Fore.WHITE + " Sair")
        print()

        saida = int(input(Fore.MAGENTA + "Introduza a sua opção -> " + Fore.WHITE))
        if saida == 0:
            print(Fore.RED + "Saindo.......")
        elif saida == 1:
            g.desenha()
        elif saida == 2:
            for place in g.places:
                print(str(place))
            input("Prima Enter para continuar")
        elif saida == 3:
            for road in g.roads:
                print(str(road))
            input("Prima Enter para continuar")
        elif saida == 4:
            start = input("Introduza o ponto de partida: ").lower()
            goal = input("Introduza o objetivo: ").lower()

            best_path, best_time, best_vehicle, best_visited = g.dfs_search_for_all_vehicles(start, goal, vehicles)
            if best_path:
                print()
                print(Fore.GREEN + "CAMINHO ENCONTRADO"+ Fore.WHITE)
                print(f"Melhor caminho encontrado com o veículo: {best_vehicle.getType()}" )
                print(Fore.GREEN + "Caminho:" + Fore.WHITE + f"{best_path}\n" + Fore.GREEN + "Tempo: " + Fore.WHITE + f"{best_time} minutos")
                print(Fore.GREEN + "Visitados:" + Fore.WHITE + f"{best_visited}")
            else:
                print()
                print(Fore.RED + "Não foi possível encontrar um caminho.")
            input("Prima Enter para continuar")
            
        elif saida == 5:
            start = input("Introduza o ponto de partida: ").lower()
            goal = input("Introduza o objetivo: ").lower()

            best_path, best_time, best_vehicle, best_visited = g.bfs_search_for_all_vehicles(start, goal, vehicles)
            if best_path:
                print()
                print(Fore.GREEN + "CAMINHO ENCONTRADO"+ Fore.WHITE)
                print(Fore.GREEN + "Veículo: " + Fore.WHITE + f"{best_vehicle.getType()}" )
                print(Fore.GREEN + "Caminho:" + Fore.WHITE + f"{best_path}\n" + Fore.GREEN + "Tempo: " + Fore.WHITE + f"{best_time} minutos")
                print(Fore.GREEN + "Visitados:" + Fore.WHITE + f"{best_visited}")
            else:
                print()
                print(Fore.RED + "Não foi possível encontrar um caminho.")
            input("Prima Enter para continuar")
        else:
            print(Fore.RED + "Opção inválida!")
            input("Prima Enter para continuar")

if __name__ == "__main__":
    main()