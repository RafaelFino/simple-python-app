from locale import currency
from datetime import datetime as dt
from fastapi import FastAPI, Response, Request
from http import HTTPStatus
from service.product import ProductService
from entities.product import Product
import time
import configparser
from fastapi.logger import logger

config = configparser.ConfigParser()
config.read("etc/config.ini")

app = FastAPI()

service = ProductService(config["ProductService"])

def createResponseBody(start, args = None):
    ret = {
        "timestamp": dt.now().time()  
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

@app.put("/product", status_code=200)
async def InsertProduct(request: Request, response: Response):
    body = await request.json()

    newID = service.Insert(body["name"], body["price"])

    response.status_code = HTTPStatus.CREATED

    return createResponseBody(time.time(), 
    {
        "product-id": newID
    }) 

@app.get("/product")
async def LoadProduct():
    return createResponseBody(time.time(), 
    {
        "products": service.GetProducts()
    })

@app.get("/product/{id}")
async def LoadProducst(id : int):
    return createResponseBody(time.time(), 
    {
        "products": service.GetProduct(id)
    })    