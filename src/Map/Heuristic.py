class Heuristic:
    def __init__(self):
        self.heuristics = list()

    def createHeuristics(self):
        pedomeHeuristics = {
            "pedome": 0,
            "ronfe": 6,
            "mogege": 3,
            "gondar": 2,
            "s. jorge de selho": 6,
            "selho (são cristovão)": 5,
            "serzedelo": 4,
            "gandarela": 7,
            "riba d'ave": 7,
            "ruivães": 13, 
            "carreira": 12,
            "avidos": 15, 
            "vale (são martinho)": 12
        }

        ronfeHeuristics = {
            "ronfe": 0,
            "mogege": 3,
            "gondar": 3,
            "s. jorge de selho": 4,
            "selho (são cristovão)": 6,
            "serzedelo": 5,
            "gandarela": 7,
            "riba d'ave": 7,
            "ruivães": 14, 
            "carreira": 13,
            "avidos": 16, 
            "vale (são martinho)": 12
        }

        mogegeHeuristics = {
            "mogege": 0,
            "gondar": 6,
            "s. jorge de selho": 7,
            "selho (são cristovão)": 9,
            "serzedelo": 8,
            "gandarela": 10,
            "riba d'ave": 10,
            "ruivães": 15, 
            "carreira": 14,
            "avidos": 16, 
            "vale (são martinho)": 8
        }

        gondarHeuristics = {
            "gondar": 0,
            "s. jorge de selho": 3,
            "selho (são cristovão)": 2,
            "serzedelo": 1,
            "gandarela": 4,
            "riba d'ave": 4,
            "ruivães": 9, 
            "carreira": 8,
            "avidos": 11, 
            "vale (são martinho)": 15
        }

        sJorgeDeSelhoHeuristics = {
            "s. jorge de selho": 0,
            "selho (são cristovão)": 3,
            "serzedelo": 5,
            "gandarela": 7,
            "riba d'ave": 7,
            "ruivães": 12, 
            "carreira": 11,
            "avidos": 14, 
            "vale (são martinho)": 17
        }

        selhoSaoCristovaoHeuristics = {
            "selho (são cristovão)": 0,
            "serzedelo": 4,
            "gandarela": 6,
            "riba d'ave": 6,
            "ruivães": 11, 
            "carreira": 10,
            "avidos": 13, 
            "vale (são martinho)": 18
        }

        serzedeloHeuristics = {
            "serzedelo": 0,
            "gandarela": 2,
            "riba d'ave": 2,
            "ruivães": 8, 
            "carreira": 7,
            "avidos": 10, 
            "vale (são martinho)": 17
        }

        gandarelaHeuristics = {
            "gandarela": 0,
            "riba d'ave": 5,
            "ruivães": 10, 
            "carreira": 9,
            "avidos": 12, 
            "vale (são martinho)": 20
        }

        ribaDAveHeuristics = {
            "riba d'ave": 0,
            "ruivães": 6, 
            "carreira": 5,
            "avidos": 8, 
            "vale (são martinho)": 17
        }

        ruivaesHeuristics = {
            "ruivães": 0, 
            "carreira": 11,
            "avidos": 14, 
            "vale (são martinho)": 23
        }

        carreiraHeuristics = {
            "carreira": 0,
            "avidos": 3, 
            "vale (são martinho)": 11
        }

        avidosHeuristics = {
            "avidos": 0, 
            "vale (são martinho)": 7
        }

        # Agora todas as chaves estão em minúsculas
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
        # Normalizando as chaves para evitar problemas com maiúsculas/minúsculas e espaços extras
        start = start.lower().strip()
        dest = dest.lower().strip()
    
        for h in self.heuristics:
            # Verificando se as chaves normalizadas existem no dicionário de heurísticas
            if start in h and dest in h:
                return h[dest]
        return 0  # Se não encontrar, retorna 0 por padrão
