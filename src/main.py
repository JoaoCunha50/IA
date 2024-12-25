from Map.Map import Map
from utils.Json_Reader import Json_Reader

def main():

    vehicles = []
    vehicles = Json_Reader.load_vehicles_from_file("src/jsons/vehicles.json")
    for vehicle in vehicles:
        print(str(vehicle))
        print()

    g = Map()

    #Ficha2
    g.add_road("Pedome", "Gondar", 3)
    g.add_road("Pedome", "Serzedelo", 5)
    g.add_road("Pedome", "Mogege", 4)
    g.add_road("Gondar", "Ronfe", 4)
    g.add_road("Gondar", "S. Jorge de Selho", 4)
    g.add_road("Gondar", "Selho (São Cristóvão)", 3)
    g.add_road("Gondar", "Serzedelo", 2)
    g.add_road("Ronfe", "Mogege", 4)
    g.add_road("Ronfe", "S. Jorge de Selho", 5)
    g.add_road("S. Jorge de Selho", "Selho (São Cristóvão)", 4)
    g.add_road("Serzedelo", "Gandarela", 3)
    g.add_road("Serzedelo", "Ruivães", 12)
    g.add_road("Serzedelo", "Riba d'Ave", 3)
    g.add_road("Riba d'Ave", "Ruivães", 7)
    g.add_road("Riba d'Ave", "Carreira", 6)
    g.add_road("Carreira", "Avidos", 4)
    g.add_road("Avidos", "Vale (São Martinho)", 9)
    g.add_road("Mogege", "Vale (São Martinho)", 10)
    

    #Ficha2
    g.add_heuristica("elvas", 270)
    g.add_heuristica("borba", 250)
    g.add_heuristica("estremoz", 145)
    g.add_heuristica("evora", 95)
    g.add_heuristica("montemor", 70)
    g.add_heuristica("vendasnovas", 45)
    g.add_heuristica("arraiolos", 220)
    g.add_heuristica("alcacer", 140)
    g.add_heuristica("palmela", 85)
    g.add_heuristica("almada", 25)
    g.add_heuristica("alandroal", 180)
    g.add_heuristica("redondo", 170)
    g.add_heuristica("monsaraz", 120)
    g.add_heuristica("barreiro", 30)
    g.add_heuristica("baixadabanheira", 33)
    g.add_heuristica("moita", 35)
    g.add_heuristica("alcochete", 26)
    g.add_heuristica("lisboa", 0)

    saida = -1
    while saida != 0:
        print()
        print("1-Desenhar Grafo")
        print("2-Imprimir nodos de Grafo")
        print("3-Imprimir arestas de Grafo")
        print("0-Saír")

        saida = int(input("introduza a sua opcao-> "))
        if saida == 0:
            print("saindo.......")
        elif saida == 1:
            g.desenha()
        elif saida == 2:
            for place in g.places:
                print(str(place))
            input("Prima Enter para continuar")
        elif saida == 3:
            for road in g.roads:
                print(str(road))
            input("prima enter para continuar")
        else:
            print("you didn't add anything")
            input("prima enter para continuar")


if __name__ == "__main__":
    main()
