class Suplement:
    def __init__(self, type, quantity=0):
        if not isinstance(type, str) or not type:
            raise ValueError("Type must be a non-empty string")
        if quantity < 0:
            raise ValueError("Quantity must be non-negative")
        
        self.type = type
        self.quantity = quantity

    def getType(self):
        return self.type

    def getQuantity(self):
        return self.quantity

    def setType(self, type):
        if isinstance(type, str) and type:
            self.type = type
        else:
            raise ValueError("Type must be a non-empty string")

    def setQuantity(self, quantity):
        if quantity >= 0:
            self.quantity = quantity
        else:
            raise ValueError("Quantity must be non-negative")

    def __str__(self):
        return f"type {self.type}, quantity {self.quantity}"

    def __eq__(self, other):
        if isinstance(other, Suplement):
            return self.type == other.type and self.quantity == other.quantity
        return False
