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
    
    def setName(self, name):
        if isinstance(name, str) and name:
            self.name = name
        else:
            raise ValueError("Type must be a non-empty string")

    def getName(self):
        return self.m_name

    def __eq__(self, other):
        return (self.m_name == other.m_name and
                self.m_id == other.m_id and
                self.population == other.population)

    def __hash__(self):
        return hash(self.m_name)
