class Suplement:
    def __init__(self, urgency, location, quantity, timeRemaining):
        # Validate the inputs
        if quantity < 0:
            raise ValueError("Quantity must be non-negative")
        if urgency < 0 or urgency > 5:
            raise ValueError("Urgency must be between 0 and 5")
        
        self.urgency = urgency
        self.quantity = quantity
        self.location = location
        self.timeRemaining = timeRemaining

    def getUrgency(self):
        return self.urgency

    def getQuantity(self):
        return self.quantity

    def getLocation(self):
        return self.location

    def getTimeRemaining(self):
        return self.timeRemaining

    def setUrgency(self, urgency):
        if urgency >= 0 and urgency <= 5:
            self.urgency = urgency
        else:
            raise ValueError("Urgency must be a value from 0 to 5")

    def setQuantity(self, quantity):
        if quantity >= 0:
            self.quantity = quantity
        else:
            raise ValueError("Quantity must be non-negative")

    def __str__(self):
        return f"Urgency: {self.urgency}, Quantity: {self.quantity}, Location: {self.location}, Time Remaining: {self.timeRemaining}"

    def __eq__(self, other):
        if isinstance(other, Suplement):
            return (self.urgency == other.urgency and 
                    self.quantity == other.quantity and 
                    self.location == other.location and 
                    self.timeRemaining == other.timeRemaining)
        return False
