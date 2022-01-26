class Product:
    def __init__(self, id, name, price):
        self.ID = id
        self.Name = name
        self.Price = {}
        self.Price["BRL"] = float(price)

    def SetNewCurrency(self, code, value):
        self.Price[code] = round(float(self.Price["BRL"]) / float(value), 2)