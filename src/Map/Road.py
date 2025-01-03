import random
from colorama import *

class Road:
    # Tipos de bloqueio e seus efeitos nos veículos
    VALID_BLOCKAGE_TYPES = {
        "Cheias": ["drone s", "drone m"],           # Inundação - apenas drones podem passar
        "Árvore Caída": ["drone m", "drone s"],     # Árvore caída - apenas drones podem passar
        "Construção": ["moto", "carrinha", "drone s", "drone m"],  # Construção - todos exceto caminhão
        "Acidente": ["drone m", "drone s"],        # Acidente - apenas drones podem passar
        "Pequenos detritos": ["drone s", "drone m", "carrinha", "caminhao"],  # Destroços leves - todos exceto moto
        "Tempestade" : ["caminhao","carrinha","moto"] # Tempestade - apenas veículos terrestres
    }

    # Lista de todos os tipos de veículos possíveis
    ALL_VEHICLES = ["caminhao", "moto", "carrinha", "drone s", "drone m"]

    def __init__(self, origin, destination, weight, blocked=None, blockage_type=None):
        # Validação dos parâmetros
        if not isinstance(origin, str) or not origin:
            raise ValueError("Origin must be a non-empty string")
        if not isinstance(destination, str) or not destination:
            raise ValueError("Destination must be a non-empty string")
        if weight <= 0:
            raise ValueError("Weight must be greater than 0")
    
        # Atribuição de valores aos atributos
        self.origin = origin
        self.destination = destination
        self.weight = weight
        self.blocked = blocked
    
        # Usa o tipo de bloqueio passado ou gera um novo aleatório
        self.blockage_type = blockage_type if blocked and blockage_type else (
            random.choice(list(self.VALID_BLOCKAGE_TYPES.keys())) if self.blocked else None
        )

    # Getters permanecem os mesmos
    def getOrigin(self):
        return self.origin

    def getDestination(self):
        return self.destination

    def getWeight(self):
        return self.weight

    def getBlocked(self):
        return self.blocked

    def getBlockageType(self):
        return self.blockage_type

    def getAllowedVehicles(self):
        # Se não está bloqueado, todos os veículos são permitidos
        if not self.blocked:
            return self.ALL_VEHICLES

        # Se está bloqueado, retorna apenas os veículos permitidos para aquele tipo de bloqueio
        return self.VALID_BLOCKAGE_TYPES[self.blockage_type]

    # Verificar se um veículo pode passar
    def canVehiclePass(self, vehicle_type):
        if not isinstance(vehicle_type, str):
            raise ValueError("Vehicle type must be a string")

        vehicle_type = vehicle_type.lower()
        
        # Verifica se é um tipo de veículo válido
        if vehicle_type not in self.ALL_VEHICLES:
            raise ValueError(f"Invalid vehicle type. Must be one of: {', '.join(self.ALL_VEHICLES)}")

        # Se não está bloqueado, todos os veículos podem passar
        if not self.blocked:
            return True

        # Se está bloqueado, o veículo só pode passar se estiver na lista de permitidos
        return vehicle_type in self.VALID_BLOCKAGE_TYPES[self.blockage_type]

    def __str__(self):
        label_color = Fore.CYAN
        value_color = Fore.WHITE
        blocked_color = Fore.RED if self.blocked else Fore.GREEN
        
        result = (f"\n{label_color}Origin: {value_color}{self.origin}{Style.RESET_ALL}\n"
                 f"{label_color}Destination: {value_color}{self.destination}{Style.RESET_ALL}\n"
                 f"{label_color}Weight (kg): {value_color}{self.weight}{Style.RESET_ALL}\n"
                 f"{label_color}Blocked: {blocked_color}{self.blocked}{Style.RESET_ALL}\n")
        
        if self.blocked and self.blockage_type:
            result += f"{label_color}Blockage Type: {value_color}{self.blockage_type}{Style.RESET_ALL}\n"
        
        result += f"{label_color}Allowed Vehicles: {value_color}{', '.join(self.getAllowedVehicles())}{Style.RESET_ALL}\n"
        return result

    def __eq__(self, other):
        if isinstance(other, Road):
            return (self.origin == other.origin and
                    self.destination == other.destination and
                    self.weight == other.weight and
                    self.blocked == other.blocked and
                    self.blockage_type == other.blockage_type)
        return False