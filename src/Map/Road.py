class Road:
    def __init__(self, origin, destination, weight):
        if not isinstance(origin, str) or not origin:
            raise ValueError("Origin must be a non-empty string")
        if not isinstance(destination, str) or not destination:
            raise ValueError("Destination must be a non-empty string")
        if weight <= 0:
            raise ValueError("Weight must be greater than 0")

        self.origin = origin
        self.destination = destination
        self.weight = weight

    # Getters
    def getOrigin(self):
        return self.origin

    def getDestination(self):
        return self.destination

    def getWeight(self):
        return self.weight

    # Setters
    def setOrigin(self, origin):
        if isinstance(origin, str) and origin:
            self.origin = origin
        else:
            raise ValueError("Origin must be a non-empty string")

    def setDestination(self, destination):
        if isinstance(destination, str) and destination:
            self.destination = destination
        else:
            raise ValueError("Destination must be a non-empty string")

    def setWeight(self, weight):
        if weight > 0:
            self.weight = weight
        else:
            raise ValueError("Weight must be greater than 0")

    def __str__(self):
        return f"{self.origin} -> {self.destination} (custo: {self.weight})"

    def __eq__(self, other):
        if isinstance(other, Road):
            return (self.origin == other.origin and 
                    self.destination == other.destination and 
                    self.weight == other.weight)
        return False