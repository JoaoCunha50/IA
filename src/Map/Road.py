class Road:
    def __init__(self, origin, destination, weight):
        self.origin = origin
        self.destination = destination
        self.weight = weight

    def __str__(self):
        return f"{self.origin} -> {self.destination} (custo: {self.weight})"