import random

class Road:
    def __init__(self, origin, destination, weight, allowed, blocked=None):
        # Validação dos parâmetros
        if not isinstance(origin, str) or not origin:
            raise ValueError("Origin must be a non-empty string")
        if not isinstance(destination, str) or not destination:
            raise ValueError("Destination must be a non-empty string")
        if weight <= 0:
            raise ValueError("Weight must be greater than 0")
        if not isinstance(allowed, list) or not all(isinstance(v, str) for v in allowed):
            raise ValueError("Allowed must be a list of strings representing vehicle types")

        # Atribuição de valores aos atributos
        self.origin = origin
        self.destination = destination
        self.weight = weight
        
        # Se blocked for fornecido, usa o valor, caso contrário, atribui um valor aleatório
        self.blocked = blocked if blocked is not None else random.random() < 0.15
        
        self.allowedVehicles = [v.lower() for v in allowed]  # Garantir que todos os tipos de veículos estejam em minúsculas
        
    # Getters
    def getOrigin(self):
        return self.origin

    def getDestination(self):
        return self.destination

    def getWeight(self):
        return self.weight

    def getBlocked(self):
        return self.blocked

    def getAllowedVehicles(self):
        return self.allowedVehicles

    # Verificar se um veículo pode passar
    def canVehiclePass(self, vehicle_type):
        if not isinstance(vehicle_type, str):
            raise ValueError("Vehicle type must be a string")
        # Converter o tipo de veículo para minúsculas antes de comparar
        return not self.blocked and vehicle_type.lower() in self.allowedVehicles

    def __str__(self):
        return (f"{self.origin} -> {self.destination} (custo: {self.weight}, blocked: {self.blocked}, "
                f"allowed: {self.allowedVehicles})")

    def __eq__(self, other):
        if isinstance(other, Road):
            return (self.origin == other.origin and 
                    self.destination == other.destination and 
                    self.weight == other.weight and
                    self.blocked == other.blocked and
                    self.allowedVehicles == other.allowedVehicles)
        return False
