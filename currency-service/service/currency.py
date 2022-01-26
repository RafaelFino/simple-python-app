from datetime import datetime
from datetime import timedelta
import requests
from entities.currency import Currency

class CurrenciesService:
    _currencies = {}
    LastUpdate = None
    _url = None
    _timeToExpire = None

    def __init__(self, url, timeToExpire):
        self._url = url  
        self._timeToExpire = int(timeToExpire)

    def Load(self):        
        r = requests.get(self._url)
        data = r.json()

        for code in data:
            value = data[code]
            self._currencies[code.upper()] = Currency(code, value['name'], value['high'], value['low'], value['varBid'], value['bid'], value['ask'])
        
        self.LastUpdate = datetime.now() 

    def Get(self):
        if self.LastUpdate is None:
            self.Load()

        if datetime.now() - self.LastUpdate > timedelta(minutes=self._timeToExpire):
            self.Load()

        return self._currencies

