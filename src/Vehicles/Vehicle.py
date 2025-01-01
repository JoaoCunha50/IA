from Vehicles.Suplement import Suplement
from colorama import *

class Vehicle:
    def __init__(self, type, capacity, speed, autonomy, quantity=0, id=-1):
        if capacity <= 0:
            raise ValueError("Capacity must be greater than 0")
        if quantity < 0:
            raise ValueError("Quantity cannot be negative")
        if speed <= 0:
            raise ValueError("Speed must be greater than 0")
        
        self.id = id
        self.type = type
        self.capacity = capacity
        self.speed = speed
        self.autonomy = autonomy
        self.quantity_of_suplements = capacity # assumindo que esta no maximo
        self.suplements: list[Suplement] = []
    
    def getId(self):
        return self.id
    
    def getType(self):
        return self.type
    
    def getCapacity(self):
        return self.capacity
    
    def getQuantitySup(self):
        return self.quantity_of_suplements
    
    def getSpeed(self):
        return self.speed
    
    def getSuplements(self):
        return self.suplements
    
    def setId(self, id):
        if id >= 0:
            self.id = id
        else:
            raise ValueError("ID must be non-negative")
    
    def setType(self, type):
        if isinstance(type, str) and type:
            self.type = type
        else:
            raise ValueError("Type must be a non-empty string")
    
    def setCapacity(self, capacity):
        if capacity > 0:
            self.capacity = capacity
        else:
            raise ValueError("Capacity must be greater than 0")
    
    def setQuantitySup(self, quantity):
        if quantity >= 0:
            self.quantity_of_suplements = quantity
        else:
            raise ValueError("Quantity must be non-negative")
    
    def setSpeed(self, speed):
        if speed > 0:
            self.speed = speed
        else:
            raise ValueError("Speed must be greater than 0")
    
    def setSuplements(self, suplements):
        if isinstance(suplements, list) and all(isinstance(sup, Suplement) for sup in suplements):
            self.suplements = suplements
        else:
            raise ValueError("Suplements must be a list of Suplements objects")

    def addSupplement(self, supplement: Suplement):
        if isinstance(supplement, Suplement):
            self.suplements.append(supplement)
        else:
            raise TypeError("Supplement must be an instance of Suplements")

    def removeSupplement(self, supplement: Suplement):
        if supplement in self.suplements:
            self.suplements.remove(supplement)
        else:
            raise ValueError("The supplement is not in the vehicle's list")

    def findSupplement(self, supplement_id):
        for supplement in self.suplements:
            if supplement.getId() == supplement_id:
                return supplement
        raise ValueError(f"Supplement with ID {supplement_id} not found")

    def clearSupplements(self):
        self.suplements.clear()

    def __str__(self):
        label_color = Fore.CYAN
        value_color = Fore.WHITE

        return (
            f"\n{label_color}Vehicle ID: {value_color}{self.id}{Style.RESET_ALL}\n"
            f"{label_color}Type: {value_color}{self.type}{Style.RESET_ALL}\n"
            f"{label_color}Capacity (kg): {value_color}{self.capacity}{Style.RESET_ALL}\n"
            f"{label_color}Autonomy (km): {value_color}{self.autonomy}{Style.RESET_ALL}\n"
            f"{label_color}Speed (km/h): {value_color}{self.speed}{Style.RESET_ALL}\n"
            f"{label_color}Quantity of Supplements (kg): {value_color}{self.quantity_of_suplements}{Style.RESET_ALL}\n"
            f"{label_color}Supplements: {value_color}{'None' if not self.suplements else ', '.join([str(sup) for sup in self.suplements])}{Style.RESET_ALL}\n"
        )
