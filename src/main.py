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
    g.add_road("elvas", "borba", 15)
    g.add_road("borba", "estremoz", 15)
    g.add_road("estremoz", "evora", 40)
    g.add_road("evora", "montemor", 20)
    g.add_road("montemor", "vendasnovas", 15)
    g.add_road("vendasnovas", "lisboa", 50)
    g.add_road("elvas", "arraiolos", 50)
    g.add_road("arraiolos", "alcacer", 90)
    g.add_road("alcacer", "palmela", 35)
    g.add_road("palmela", "almada", 25)
    g.add_road("palmela", "barreiro", 25)
    g.add_road("barreiro", "palmela", 30)
    g.add_road("almada", "lisboa", 15)
    g.add_road("elvas", "alandroal", 40)
    g.add_road("alandroal", "redondo", 25)
    g.add_road("redondo", "monsaraz", 30)
    g.add_road("monsaraz", "barreiro", 120)
    g.add_road("barreiro", "baixadabanheira", 5)
    g.add_road("baixadabanheira", "moita", 7)
    g.add_road("moita", "alcochete", 20)
    g.add_road("alcochete", "lisboa", 20)
    

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
