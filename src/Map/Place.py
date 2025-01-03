from colorama import Fore, Style

class Place:
    def __init__(self, name, sup=None, id=-1):
        self.m_id = id
        self.m_name = str(name).lower()  # Armazena o nome em minúsculas
        self.urgency_level = 0
        self.quantity = 0
        self.obtained = 0
        self.time_remaining = 0
        if name == 'Gondar' or name == 'Avidos':
            self.ponto_reabastecimento = True
        else:
            self.ponto_reabastecimento = False

        # Configura o supply se um suplemento foi passado
        if sup:
            self.setSupply(sup)

    def __str__(self):
        name_color = Fore.CYAN
        label_color = Fore.WHITE

        # Formatando a string com cores e espaçamento
        return (f"\n{name_color}Node: {label_color}{self.m_name.capitalize()}{Style.RESET_ALL}\n"
                f"    {name_color}Urgency Level: {label_color}{self.urgency_level if self.urgency_level is not None else 'None'}{Style.RESET_ALL}\n"
                f"    {name_color}Quantity (kg): {label_color}{self.quantity if self.quantity is not None else 'None'}{Style.RESET_ALL}\n"
                f"    {name_color}Obtained (kg): {label_color}{self.obtained if self.obtained is not None else 'None'}{Style.RESET_ALL}\n"
                f"    {name_color}Time Remaining (s): {label_color}{self.time_remaining if self.time_remaining is not None else 'None'}{Style.RESET_ALL}\n")

    def setId(self, id):
        self.m_id = id

    def getId(self):
        return self.m_id

    def resetQuantity(self):
        self.obtained = 0
    
    def setSupply(self, supply):
        # Verifica se o supply possui os métodos esperados
        if all(hasattr(supply, method) for method in ["getUrgency", "getQuantity", "getTimeRemaining"]):
            if self.urgency_level == 0 or self.quantity == 0 or self.time_remaining == 0:
                self.urgency_level = supply.getUrgency()
                self.quantity = supply.getQuantity()
                self.time_remaining = supply.getTimeRemaining()
        else:
            raise TypeError("Supply object must have 'getUrgency', 'getQuantity', and 'getTimeRemaining' methods.")

    def setName(self, name):
        if isinstance(name, str) and name.strip():  # Verifica se o nome é uma string não vazia
            self.m_name = name.lower()  # Converte para minúsculas
        else:
            raise ValueError("Name must be a non-empty string.")

    def getName(self):
        return self.m_name

    def getQuantity(self):
        return self.quantity

    def getUrgency(self):
        return self.urgency_level

    def setUrgency(self, urgency):
        self.urgency_level = urgency

    def setQuantity(self, value):
        self.quantity = value

    def getTimeRemaining(self):
        return self.time_remaining

    def setTimeRemaining(self, value):
        self.time_remaining = value

    def __eq__(self, other):
        if not isinstance(other, Place):
            return False
        return (self.m_name == other.m_name and
                self.m_id == other.m_id and
                self.urgency_level == other.urgency_level and
                self.quantity == other.quantity and
                self.obtained == other.obtained and
                self.time_remaining == other.time_remaining)

    def __hash__(self):
        return hash(self.m_name)
