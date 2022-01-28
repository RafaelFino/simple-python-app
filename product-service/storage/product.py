from unicodedata import decimal
from numpy import int64
from entities.product import Product
import psycopg2

class ProductStorage:
    conn = None
    DBHost = None
    DBName = None
    DBUser = None
    DBPass = None

    def __init__(self, dbhost, dbname, user, pw):
        self.DBHost = dbhost
        self.DBName = dbname
        self.DBUser = user
        self.DBPass = pw

    def Connect(self):
        if self.conn is None or self.conn.closed:
            self.conn = psycopg2.connect(
                host=self.DBHost, 
                database=self.DBName, 
                user=self.DBUser, 
                password=self.DBPass
            )

    def Insert(self, product: Product):
        self.Connect()

        cur = self.conn.cursor()

        cur.execute(f"INSERT INTO product (name, price) VALUES ('{product.Name}', {product.Price['BRL']}) RETURNING id")
        id = cur.fetchone()[0]

        self.conn.commit()
        cur.close()

        return id
    
    def LoadAll(self):
        return self.load(f"SELECT id, name, price::money::numeric::float8 FROM product ORDER BY id;")

    def LoadProduct(self, id):
        return self.load(f"SELECT id, name, price::money::numeric::float8 FROM product WHERE id = {id} ORDER BY id")

    def load(self, query:str):
        self.Connect()

        cur = self.conn.cursor()

        cur.execute(query)
        
        data = cur.fetchall()
        ret = []

        for i in data:
            ret.append(Product(i[0], i[1], int64(i[2])))

        cur.close()            

        return ret