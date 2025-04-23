import psycopg2 #библиотека для работы с постгрес
import logging
from crypto_utils import key_load_from_flash

logger = logging.getLogger(__name__)


DB_CONFIG={
    "dbname":"users_data",
    "user":"app_user",
    "password":"secure_password",
    "host":"localhost",
    "port": "5432"
}


DB_ENCRYPTION_KEY = key_load_from_flash()



def init_db():
    conn = psycopg2.connect(**DB_CONFIG)#устанавливает соединение с бд с помощью словаря конфигурации
    c = conn.cursor() #создает объект курсора для выполнения sql-запросов
    c.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto;")#активирует модуль в пострес для шифрования
    c.execute('''CREATE TABLE IF NOT EXISTS users(
              id SERIAL PRIMARY KEY,
              last_name TEXT,
              number TEXT,
              address TEXT,
              password bytea,
              timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()#фиксация изменений
    conn.close()#закрывает подключение к базе
    logger.info("База данных инициализирована")


def save_to_db(data):
    conn = psycopg2.connect(**DB_CONFIG)
    c = conn.cursor()
    for entry in data:
        if entry:
            c.execute ("INSERT INTO users (last_name, number, address,password)VALUES(%s, %s,%s, encrypt(%s::bytea, %s, 'aes-cbc/pad:pkcs'))",
                      (entry.get("last_name"), entry.get("number"), entry.get("address"), entry.get("password"), DB_ENCRYPTION_KEY)
                      )
    conn.commit()
    conn.close()


def get_users():
    conn= psycopg2.connect(**DB_CONFIG)
    c = conn.cursor()
    c.execute("SELECT id, last_name, number, address, decrypt(password, %s, 'aes-cbc/pad:pkcs')::text,timestamp FROM users ORDER BY timestamp DESC",
              (DB_ENCRYPTION_KEY,)
             )#выполняет sql-запросы для выборки данных
    users = c.fetchall()#получает все записи как список кортежей
    conn.close()
    return users #возврат всех записей с расшифрованными паролями в виде списка кортежей




import psycopg2
import logging
from crypto_utils import key_load_from_flash


logger= logging.getLogger(__name__)

DB_CONFIG = {
    "dbname":"user3",
    "user":"user3",
    "host":"",
    "port":"5533",
    "password":"",
}

DB_ENCRYPTION_KEY = key_load_from_flash

def init_db():
    conn = psycopg2.connect(**DB_CONFIG)
    c = conn.cursor()
    c.execute('''CREATE EXTENTION IF NOT EXISTS pgcrypto;''')
    c.execute('''CREATE TABLE IF NOT EXISTS users(
              id SERIAL PRIMARY KEY,
              last_name TEXT,
              address TEXT,
              number TEXT,
              password bytea,
              timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()
    logger.info("База данных инициализирована")

def save_to_db(data):
    conn = psycopg2.connect(**DB_CONFIG)
    c = conn.cursor()
    for enrty in data:
        if enrty:
            c.execute('''INSERT INTO users (last_name, address, numder, password) VALUES (%s, %s, %s, encrypt(%s::bytea, %s, 'aes-cbc/pad:pkcs')),
                      (entry.get(last_name), entry.get(address), entry.get(number), entry.get(password), DB_ENCRYPTION_KEY)''')
            
    conn.commit()
    conn.close()

def get_users():
    conn = psycopg2.connect(**DB_CONFIG)
    c = conn.cursor()
    c.execute('''SELECT id, last_name, address, number, decrypt(password, %s, 'aes-cbc/pad:pkcs'),
              (DB_ENCRYPTION_KEY,)''')
    users = c.fetchall()
    conn.close()
    


