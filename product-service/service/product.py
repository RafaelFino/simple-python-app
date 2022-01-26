from locale import currency
from entities.product import Product
from storage.product import ProductStorage
import requests

class ProductService:
    _storage = None
    _currencyServiceURL = None
    
    def __init__(self, config):
        self._storage = ProductStorage(config["DB-Host"], config["DB-Name"], config["DB-User"], config["DB-Pass"])
        self._currencyServiceURL = config["CurrencyServiceURL"]

    def Insert(self, name: str, price: float):
        return self._storage.Insert(Product("", name, price))

    def GetProducts(self):
        data = self._storage.LoadAll()
        return self.fillPrices(data)


    def GetProduct(self, id):
        return self.fillPrices(self._storage.LoadProduct(id))

    def getCurrencies(self):
        ret = {}

        r = requests.get(self._currencyServiceURL)
        data = r.json()

        for c in data["currencies"]:
              ret[c] = data["currencies"][c]["Bid"]

        return ret

    def fillPrices(self, products):
        currencies = self.getCurrencies()
        ret = []
        
        for p in products:
            for c in currencies:
                p.SetNewCurrency(c, currencies[c])
            
            ret.append(p)
    
        return ret

