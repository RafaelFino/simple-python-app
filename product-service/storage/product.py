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

        return id
    
    def LoadAll(self):
        self.Connect()

        cur = self.conn.cursor()

        cur.execute(f"SELECT id, name, price::money::numeric::float8 FROM product order by id;")
        
        data = cur.fetchall()
        ret = []

        for i in data:
            ret.append(Product(i[0], i[1], int64(i[2])))

        cur.close()

        return ret


    def LoadProduct(self, id):
        self.Connect()

        cur = self.conn.cursor()

        cur.execute(f"SELECT id, name, price::money::numeric::float8 FROM product WHERE id = {id}")
        
        data = cur.fetchall()
        ret = []

        for i in data:
            ret.append(Product(i[0], i[1], int64(i[2])))

        cur.close()            

        return ret
