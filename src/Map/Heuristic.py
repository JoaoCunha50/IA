class Heuristic:
    def __init__(self):
        self.heuristics = list()

    def createHeuristics(self):
        pedomeHeuristics= {
            "Pedome":0,
            "Ronfe":6,
            "Mogege":3,
            "Gondar":2,
            "S. Jorge de Selho":6,
            "Selho (São Cristovão)":5,
            "Serzedelo":4,
            "Gandarela":7,
            "Riba d'Ave":7,
            "Ruivães":13, 
            "Carreira":12,
            "Avidos":15, 
            "Vale (São Martinho)":12
        }

        ronfeHeuristics= {
            "Ronfe":0,
            "Mogege":3,
            "Gondar":3,
            "S. Jorge de Selho":4,
            "Selho (São Cristovão)":6,
            "Serzedelo":5,
            "Gandarela":7,
            "Riba d'Ave":7,
            "Ruivães":14, 
            "Carreira":13,
            "Avidos":16, 
            "Vale (São Martinho)":12
        }
        mogegeHeuristics= {
            "Mogege":0,
            "Gondar":6,
            "S. Jorge de Selho":7,
            "Selho (São Cristovão)":9,
            "Serzedelo":8,
            "Gandarela":10,
            "Riba d'Ave":10,
            "Ruivães":15, 
            "Carreira":14,
            "Avidos":16, 
            "Vale (São Martinho)":8
        }
        gondarHeuristics= {
            "Gondar":0,
            "S. Jorge de Selho":3,
            "Selho (São Cristovão)":2,
            "Serzedelo":1,
            "Gandarela":4,
            "Riba d'Ave":4,
            "Ruivães":9, 
            "Carreira":8,
            "Avidos":11, 
            "Vale (São Martinho)":15
        }
        sJorgeDeSelhoHeuristics= {
            "S. Jorge de Selho":0,
            "Selho (São Cristovão)":3,
            "Serzedelo":5,
            "Gandarela":7,
            "Riba d'Ave":7,
            "Ruivães":12, 
            "Carreira":11,
            "Avidos":14, 
            "Vale (São Martinho)":17
        }
        selhoSaoCristovaoHeuristics= {
            "Selho (São Cristovão)":0,
            "Serzedelo":4,
            "Gandarela":6,
            "Riba d'Ave":6,
            "Ruivães":11, 
            "Carreira":10,
            "Avidos":13, 
            "Vale (São Martinho)":18
        }
        serzedeloHeuristics= {
            "Serzedelo":0,
            "Gandarela":2,
            "Riba d'Ave":2,
            "Ruivães":8, 
            "Carreira":7,
            "Avidos":10, 
            "Vale (São Martinho)":17
        }
        gandarelaHeuristics= {
            "Gandarela":0,
            "Riba d'Ave":5,
            "Ruivães":10, 
            "Carreira":9,
            "Avidos":12, 
            "Vale (São Martinho)":20
        }
        ribaDAveHeuristics= {
            "Riba d'Ave":0,
            "Ruivães":6, 
            "Carreira":5,
            "Avidos":8, 
            "Vale (São Martinho)":17
        }
        ruivaesHeuristics= {
            "Ruivães":0, 
            "Carreira":11,
            "Avidos":14, 
            "Vale (São Martinho)":23
        }
        carreiraHeuristics= {
            "Carreira":0,
            "Avidos":3, 
            "Vale (São Martinho)":11
        }
        avidosHeuristics= {
            "Avidos":0, 
            "Vale (São Martinho)":7
        }
        self.heuristics.append(pedomeHeuristics)
        self.heuristics.append(ronfeHeuristics)
        self.heuristics.append(mogegeHeuristics)
        self.heuristics.append(gondarHeuristics)
        self.heuristics.append(sJorgeDeSelhoHeuristics)
        self.heuristics.append(selhoSaoCristovaoHeuristics)
        self.heuristics.append(serzedeloHeuristics)
        self.heuristics.append(gandarelaHeuristics)
        self.heuristics.append(ribaDAveHeuristics)
        self.heuristics.append(ruivaesHeuristics)
        self.heuristics.append(carreiraHeuristics)
        self.heuristics.append(avidosHeuristics)

    def getHeuristic(self, start, dest):
        for h in self.heuristics:
            if h[start] == 0:
                return h[dest]
            elif h[dest] == 0:
                return h[start]
        return 0