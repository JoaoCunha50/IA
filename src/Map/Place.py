class Place:
    def __init__(self, name, population=0, id=-1):  # Construtor do nó
        self.m_id = id
        self.m_name = str(name)
        self.population = population

    def __str__(self):
        return f"node {self.m_name}, population {self.population}"

    def setId(self, id):
        self.m_id = id

    def getId(self):
        return self.m_id
    
    def setPopulation(self, population):
        self.population = population

    def getPopulation(self):
        return self.population

    def getName(self):
        return self.m_name

    def __eq__(self, other):
        return self.m_name == other.m_name  

    def __hash__(self):
        return hash(self.m_name)
