from colorama import Fore, Back, Style, init
from Map.Map import Map
from Map.Heuristic import Heuristic
from utils.Json_Reader import Json_Reader
import copy

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

    suplements = Json_Reader.load_suplements_from_json("src/jsons/suplly_requests.json")

    heuristics = Heuristic()
    heuristics.createHeuristics()

    g = Map(heuristics)

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

    places = g.getPlaces()
    ordered_places = sorted(places, key=lambda place: place.urgency_level if place.urgency_level is not None else -1, reverse=True)
    ordered_names = [place.m_name for place in ordered_places if place.m_name.lower() != "pedome"]

    saida = -1
    while saida != 0:
        print("\n" + "="*30)
        print(Fore.CYAN + Style.BRIGHT + "          PathFinder")
        print("=" * 30)

        print(Fore.CYAN + "1-" + Fore.WHITE + " Desenhar Grafo")
        print(Fore.CYAN + "2-" + Fore.WHITE + " Imprimir nodos de Grafo")
        print(Fore.CYAN + "3-" + Fore.WHITE + " Imprimir arestas de Grafo")
        print(Fore.CYAN + "4-" + Fore.WHITE + " Imprimir veículos disponíveis")
        print(Fore.CYAN + "5-" + Fore.WHITE + " Realizar busca cega (DFS/BFS/UCS)")
        print(Fore.CYAN + "6-" + Fore.WHITE + " Realizar busca informada (A*/Greedy)")
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
            for vehicle in vehicles:
                print(str(vehicle))
            input("Prima Enter para continuar")
        elif saida == 5:
            print("\nEscolha o algoritmo de busca:")
            print(Fore.CYAN + "1-" + Fore.WHITE + " DFS")
            print(Fore.CYAN + "2-" + Fore.WHITE + " BFS")
            print(Fore.CYAN + "3-" + Fore.WHITE + " UCS")
            algoritmo = int(input(Fore.MAGENTA + "Introduza a sua opção -> " + Fore.WHITE))

            if algoritmo == 1:
                resultados = g.dfs_multiple_dest("pedome", ordered_names)
                nome_algoritmo = "DFS"
            elif algoritmo == 2:
                resultados = g.bfs_multiple_dest("pedome", ordered_names)
                nome_algoritmo = "BFS"
            elif algoritmo == 3:
                resultados = g.ucs_multiple_dest("pedome", ordered_names)
                nome_algoritmo = "UCS"
            else:
                print(Fore.RED + "Opção inválida!")
                continue
            
            print(f"\nPROCURA {nome_algoritmo}")

            for destino, (caminho, custo, visitados) in resultados.items():
                if caminho is None:
                    print()
                    print(Fore.RED + "Não foi possível encontrar um caminho para " + Fore.WHITE + f"{destino}")
                    print()
                else:
                    print()
                    print(Fore.GREEN + "Para destino " + Fore.WHITE + f"{destino}:")
                    print(Fore.GREEN + "Caminho: " + Fore.WHITE + f"{caminho}")
                    print(Fore.GREEN + "Custo: " + Fore.WHITE + f"{custo}")
                    print(Fore.GREEN + f"{'Visitados' if nome_algoritmo != 'UCS' else 'Ordem de expansão'}: " + Fore.WHITE + f"{visitados}")
                    print()
        elif saida == 6:
            print("\nEscolha o algoritmo de busca informada:")
            print(Fore.CYAN + "1-" + Fore.WHITE + " A*")
            algoritmo = int(input(Fore.MAGENTA + "Introduza a sua opção -> " + Fore.WHITE))

            if algoritmo == 1:
                resultados = g.aStar_multiple_dest("pedome", ordered_names)
                nome_algoritmo = "A*"
            else:
                print(Fore.RED + "Opção inválida!")
                continue
            
            print(f"\nPROCURA {nome_algoritmo}")
            for destino, (caminho,custo,visitados) in resultados.items():
               if caminho is None:
                    print()
                    print(Fore.RED + "Não foi possível encontrar um caminho para " + Fore.WHITE + f"{destino}")
                    print()
               else:
                    print()
                    print(Fore.GREEN + "Para destino " + Fore.WHITE + f"{destino}:")
                    print(Fore.GREEN + "Caminho: " + Fore.WHITE + f"{caminho}")
                    print(Fore.GREEN + "Custo: " + Fore.WHITE + f"{custo}")
                    print(Fore.GREEN + f"{'Visitados' if nome_algoritmo != 'UCS' else 'Ordem de expansão'}: " + Fore.WHITE + f"{visitados}")
                    print()
            input("Prima Enter para continuar")
        else:
            print(Fore.RED + "Opção inválida!")
            input("Prima Enter para continuar")

if __name__ == "__main__":
    main()
