# Sattorov Asilbek
# Python Jango, N48 - group


# 1.Postgresql bazaga python yordamida ulaning. Product nomli jadval yarating  (id,name,price, color,image).
"""
import psycopg2

database = 'homework3'
user = 'postgres'
host = 'localhost'
port = 5432
password = '0909'

conn = psycopg2.connect(database = database, user = user, host = host, port = port, password = password)
cur = conn.cursor()

create_table_query = ''' create table if not exists product(
                         id bigserial primary key,
                         name varchar(255) not null,
                         price int not null,
                         color varchar(255) not null,
                         image varchar(255) not null
);
'''

cur.execute(create_table_query)
conn.commit()
print("Table created successfully")

cur.close()
conn.close()
"""



####################################



# 2.Insert_product , select_all_products , update_product, delete_product nomli funksiyalar yarating.
"""
import psycopg2
def connect():

    conn = psycopg2.connect(database = 'homework3', user = 'postgres', host = 'localhost',
                             port = 5432, password = '0909')
    return conn


def insert_product():
    conn = connect()
    cur = conn.cursor()
    insert_into_query = (''' insert into product (name, price, color, image)
                     values (%s, %s, %s, %s)'''
                        )
    name = (input("Enter name : "))
    price = float(input("Enter price : "))
    color = (input("Enter color : "))
    image = (input("Enter image : "))

    data = (name, price, color, image)
    cur.execute(insert_into_query, data)
    conn.commit()
    print("Product inserted successfully")
    cur.close()
    conn.close()
insert_product()


def select_all_product():
     conn = connect()
     cur = conn.cursor()
     select_query = (''' select * from product ''')
     cur.execute(select_query)
     rows = cur.fetchall()
     cur.close()
     conn.close()
     return rows

select_all_product()


def update_product(product_id, name, price, color, image):
     conn = connect()
     cur = conn.cursor()
     update_query = ('''  update product set name = %s, price = %s, color = %s,
         image = %s where id = %s ''')
     cur.execute(update_query, (name, price, color, image, product_id))
     conn.commit()
     cur.close()
     conn.close()

update_product(1, name = 'Iphone 15', price = 1500, color = 'gold', image = "Iphone.jpg")



def delete_product(product_id):
     conn = connect()
     cur = conn.cursor()
     delete_query = (''' delete from product where id = %s ''')
     cur.execute(delete_query, (product_id,))
     conn.commit()
     cur.close()
     conn.close()

delete_product(1)
"""




######################################




"""
# 3.Alphabet nomli class yozing class obyektlarini  iteratsiya qilish imkoni bo’lsin (iterator).
# obyektni for sikli orqali iteratsiya qilinsa 26 ta alifbo xarflari chiqsin

class Alphabet:
     def __init__(self):
         self.letters = 'A B C D E F G H I J K L M N O P Q R S T U V W X Y Z'
         self.index = 0

     def __iter__(self):
         return self

     def __next__(self):
         if self.index < len(self.letters):
             result = self.letters[self.index]
             self.index += 1
             return result
         else:
             raise StopIteration

alphabet = Alphabet()

for letter in alphabet:
     print(letter)
"""



##########################################



# 4.print_numbers va print_leters nomli funksiyalar yarating.
# prit_numbers funksiyasi (1,5) gacha bo’lgan sonlarni , print_letters esa
# ‘’ABCDE” belgilarni loop da bitta dan time sleep(1) qo’yib ,parallel 2ta thread yarating.Ekranga parallel ravishda itemlar chiqsin.

"""
import threading
import time

def print_numbers():
    for i in range(1, 5):
        print(i)
        time.sleep(1.5)


def print_letters():
    for i in ['a', 'b', 'c', 'd', 'e']:
        print(i)
        time.sleep(1)


thread1 = threading.Thread(target = print_numbers)
thread2 = threading.Thread(target = print_letters)

thread1.start()
thread2.start()

thread1.join()
thread2.join()
"""


#####################################




# 5.Product nomli class yarating (1 – misoldagi Product ).
# Product classiga save() nomli object method yarating. Uni vazifasi object attributelari orqali bazaga saqlasin.

"""
import psycopg2

class Product:
    def __init__(self, name, price, color, image):
        self.name = name
        self.price = price
        self.color = color
        self.image = image

    def save(self):
        database = 'homework3'
        user = 'postgres'
        password = '0909'
        host = 'localhost'
        port = 5432
        conn = psycopg2.connect(database=database, user=user,
                 password=password, host=host, port=port)
        cur = conn.cursor()
        cur.execute('''
                 insert into product (name, price, color, image)
                 values (%s, %s, %s, %s);
             ''',
             (self.name, self.price, self.color, self.image))
        conn.commit()
        print("Succesfully saved")
        if conn is not None:
            cur.close()
            conn.close()

product = Product('Artel',1100,'Black','Artel.jpeg')
product = Product('Redmi Not 9',900,'Yellow','Redmi.jpeg')
product.save()
"""


##################################


# 6.DbConnect nomli ContextManager yarating. Va uning vazifasi python orqali PostGresqlga ulanish (conn,cur)



# 7.https://dummyjson.com/products/ urlga so’rov yuborib , kelgan ma’lumotlarni Product nomli tabelga saqlang
import requests
import json
import threading
import time
import psycopg2

database = 'homework3'
user = 'postgres'
host = 'localhost'
port = 5432
password = '0909'

conn = psycopg2.connect(database = database, user = user, host = host, port = port, password = password)
cursor = conn.cursor()

product_url = requests.get('https://dummyjson.com/products')
user_url = requests.get('https://dummyjson.com/users')

product_list = product_url.json()['products']
query = '''insert into product(name, price, color, image ) values(%s, %s, %s, %s);'''
for product in product_list:
    cursor.execute(query, (product['name'], product['price'], product['color'], product['image']))
conn.commit()

def download_file(url, filename):
    response = requests.get(url)
    with open(filename, 'w') as f:
        json.dump(response.json(), f, indent=4)
    print(response.status_code)



urls = [
     ('https://dummyjson.com/products', 'products.json'),
     ('https://dummyjson.com/users', 'users.json')
]

threads = [
     threading.Thread(target = download_file, args=(url, filename))
     for url, filename in urls]

for thread in threads:
     thread.start()

for thread in threads:
     thread.join()



# 8.Yechgan misollaringni git commandalari orqali githubga add qilinglar.



























