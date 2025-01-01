import random
from colorama import *

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
        label_color = Fore.CYAN
        value_color = Fore.WHITE
        blocked_color = Fore.GREEN if self.blocked else Fore.RED

        return (f"\n{label_color}Origin: {value_color}{self.origin}{Style.RESET_ALL}\n"
                f"{label_color}Destination: {value_color}{self.destination}{Style.RESET_ALL}\n"
                f"{label_color}Weight (kg): {value_color}{self.weight}{Style.RESET_ALL}\n"
                f"{label_color}Blocked: {blocked_color}{self.blocked}{Style.RESET_ALL}\n"
                f"{label_color}Allowed Vehicles: {value_color}{', '.join(self.allowedVehicles)}{Style.RESET_ALL}\n")
        
    def __eq__(self, other):
        if isinstance(other, Road):
            return (self.origin == other.origin and 
                    self.destination == other.destination and 
                    self.weight == other.weight and
                    self.blocked == other.blocked and
                    self.allowedVehicles == other.allowedVehicles)
        return False
