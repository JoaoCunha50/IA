class Place:
    def __init__(self, name, sup=None, id=-1): 
        self.m_id = id
        self.m_name = str(name).lower()
        self.urgency_level = None
        self.quantity = None
        self.time_remaining = None

        # Configura o supply se um suplemento foi passado
        if sup:
            self.setSupply(sup)

    def __str__(self):
        return f"node {self.m_name}, urgency level {self.urgency_level}, quantity {self.quantity}, time remaining {self.time_remaining}"

    def setId(self, id):
        self.m_id = id

    def getId(self):
        return self.m_id
    
    def setSupply(self, supply):
        if (self.urgency_level == None or self.quantity == None or self.time_remaining == None):
            self.urgency_level = supply.getUrgency()
            self.quantity = supply.getQuantity()
            self.time_remaining = supply.getTimeRemaining()
    
    def setName(self, name):
        if isinstance(name, str) and name:
            self.m_name = name.lower()  # Ensuring the name is stored in lowercase
        else:
            raise ValueError("Type must be a non-empty string")

    def getName(self):
        return self.m_name
    
    def getQuantity(self):
        return self.quantity
    
    def setQuantity(self,value):
        self.quantity = value

    def __eq__(self, other):
        return (self.m_name == other.m_name and
                self.m_id == other.m_id and
                self.urgency_level == other.urgency_level and
                self.quantity == other.quantity and
                self.time_remaining == other.time_remaining)

    def __hash__(self):
        return hash(self.m_name)
