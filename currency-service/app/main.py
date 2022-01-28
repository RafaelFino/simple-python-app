from locale import currency
from datetime import datetime as dt
from service.currency import CurrenciesService
from fastapi import FastAPI, Response
from http import HTTPStatus
import time
import configparser
from fastapi.logger import logger

config = configparser.ConfigParser()
config.read("etc/config.ini")

app = FastAPI()

service = CurrenciesService(config["CurrencyService"]["URL"], config["CurrencyService"]["TimeToExpire"])

def createResponseBody(start, args = None):
    ret = {
        "timestamp": dt.now().time(),
        "last-update": service.LastUpdate        
    }

    if args is not None:
        for i in args:
            ret[i] = args[i]

    ret["duration"] = round(time.time() - start, 3)    

    return ret

@app.get("/ping")
async def pong():
    return {
        "pong": dt.now().time()
    }

@app.get("/status")
async def GetCurrencies():  
    return createResponseBody(time.time()) 

#Service methods
@app.get("/")
async def GetCurrencies():
    start = time.time()
    data = service.Get()
    return createResponseBody(start, { 
        "count": len(data),
        "currencies": data  
        })      

@app.put("/load")
async def loadCurrencies():  
    start = time.time()
    service.Load()

    return createResponseBody(start)   

@app.get("/{code}", status_code=200)
async def GetCurrency(code: str, response: Response):
    start = time.time()

    data = service.GetByCode(code)

    if data is None:
        response.status_code = HTTPStatus.NOT_FOUND
        return createResponseBody(start)      

    response.status_code = HTTPStatus.OK

    return createResponseBody(start, { 
        "data": data
        })              


                 

